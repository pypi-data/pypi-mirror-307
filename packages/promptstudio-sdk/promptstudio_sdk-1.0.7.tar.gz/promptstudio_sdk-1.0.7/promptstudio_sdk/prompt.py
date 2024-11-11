from typing import Dict, List, Union, Optional
import requests
import logging
import uuid
import json
from datetime import datetime
from .base import Base
from .cache import CacheManager, InteractionCacheManager


from openai import OpenAI
import openai

import anthropic
import google.generativeai as genai

from google.ai.generativelanguage_v1beta.types import content


# import openai

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class PromptManager(Base):
    def get_all_prompts(self, folder_id: str) -> Dict:
        """
        Get all prompts for a given folder

        Args:
            folder_id: ID of the folder

        Returns:
            Dictionary containing prompt versions
        """
        logger.info(f"Fetching all prompts for folder: {folder_id}")
        response = self._request(f"/{folder_id}")
        logger.info(f"Successfully retrieved prompts for folder: {folder_id}")
        return response

    async def fullmemory_save_log_ai_interaction_prompt(
        self,
        user_id: str,
        user_prompt_id: str,
        user_prompt: dict,
        interaction_request: Dict,
    ) -> Dict:
        """
        Process and save AI interaction using cache memory
        """
        try:
            logger.info(f"Processing AI interaction for user_id: {user_id}")

            # Get version (either from request or fetch latest)
            version = interaction_request.get("version")
            if not version:
                latest_version_response = await self._request(
                    f"/fetch/prompt/latest_version/{user_prompt_id}"
                )
                version = str(latest_version_response["data"]["latest_version"])

            # Get previous messages for this prompt version
            previous_messages = InteractionCacheManager.get_prompt_version_messages(
                user_prompt_id, version
            )
            logger.info(
                f"Retrieved {len(previous_messages)} previous messages for prompt version {version}"
            )

            # Generate session_id if not present
            session_id = interaction_request.get("session_id") or str(uuid.uuid4())
            logger.info(f"Using session_id: {session_id}")

            # Get user messages from cache, default to empty if not found
            user_messages = InteractionCacheManager.get_user_messages(
                user_prompt_id
            ) or {"systemMessage": "", "variable": {}, "messages": []}
            logger.info(f"Retrieved user messages for prompt_id: {user_prompt_id}")

            # Extract system message and variables
            system_message = user_messages.get("systemMessage", "")
            default_variables = user_messages.get("variable", {})

            # Process variables
            variables = default_variables.copy()
            if interaction_request.get("variables"):
                for key, value in interaction_request["variables"].items():
                    if key in default_variables:
                        variables[key] = value

            # Build message collection
            prompt_collection_msg = []

            # Add system message if platform is not Claude
            if user_prompt["platform"] != "claude":
                prompt_collection_msg.append(
                    {
                        "role": "system",
                        "content": [{"type": "text", "text": system_message}],
                    }
                )

            # Add previous messages
            prompt_collection_msg.extend(previous_messages)

            # Add new user message
            prompt_collection_msg.append(
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": interaction_request["user_message"]}
                    ],
                }
            )

            # Process messages (convert JSON content in assistant messages to string)
            for msg in prompt_collection_msg:
                if msg["role"] == "assistant" and isinstance(msg["content"], dict):
                    msg["content"] = json.dumps(msg["content"])

            # Make AI platform request
            platform_name = user_prompt["platform"]
            response = await self._make_ai_platform_request(
                platform_name=platform_name,
                prompt_details=user_prompt,
                messages=prompt_collection_msg,
                system_message=system_message,
            )

            assistant_reply = response["response"]

            # Create new messages to save
            current_time = datetime.now().isoformat()
            new_messages = [
                {
                    "id": str(uuid.uuid4()),
                    "role": "user",
                    "content": interaction_request["user_message"],
                    "env": interaction_request.get("env", "test"),
                    "requestFrom": interaction_request.get("request_from", "sdk"),
                    "initiatedAt": current_time,
                },
                {
                    "id": str(uuid.uuid4()),
                    "role": "assistant",
                    "content": assistant_reply,
                    "env": interaction_request.get("env", "test"),
                    "requestFrom": interaction_request.get("request_from", "sdk"),
                    "initiatedAt": current_time,
                },
            ]

            # Save to cache
            InteractionCacheManager.save_interaction(
                session_id,
                {
                    "messages": new_messages,
                    "lastResponseAt": current_time,
                    "memory_type": interaction_request.get("memory_type", "fullMemory"),
                    "window_size": interaction_request.get("window_size", 10),
                    "prompt_id": user_prompt_id,
                    "version": version,
                },
            )

            return {
                "message": "AI interaction saved successfully for memory type: full memory",
                "user_prompt_id": user_prompt_id,
                "response": assistant_reply,
                "session_id": session_id,
            }

        except Exception as e:
            error_message = (
                f"An error occurred while processing AI interaction: {str(e)}"
            )
            logger.error(error_message)
            raise ValueError(error_message)

    async def _fetch_and_cache_prompt_details(
        self, prompt_id: str, version: Optional[str] = None
    ) -> Dict:
        """
        Fetch prompt details from PromptStudio and cache them

        Args:
            prompt_id: ID of the prompt
            version: Version number of the prompt (if None, latest version will be used)

        Returns:
            Dictionary containing prompt details
        """
        try:
            if version is None:
                # First fetch the latest version
                logger.info(f"Fetching latest version for prompt_id: {prompt_id}")
                latest_version_response = await self._request(
                    f"/fetch/prompt/latest_version/{prompt_id}"
                )

                # Updated to match new response format
                if (
                    not latest_version_response.get("data")
                    or "latest_version" not in latest_version_response["data"]
                ):
                    logger.error(
                        f"Could not fetch latest version for prompt_id: {prompt_id}"
                    )
                    raise ValueError("Could not fetch latest version")

                version = str(latest_version_response["data"]["latest_version"])
                logger.info(f"Latest version for prompt_id {prompt_id} is {version}")

            logger.info(
                f"Fetching prompt details for prompt_id: {prompt_id}, version: {version}"
            )
            response = await self._request(
                f"/fetch/prompt/version_data/{prompt_id}/{version}"
            )

            if not response.get("data") or not response["data"].get("result"):
                logger.error(f"Invalid response format for prompt_id: {prompt_id}")
                raise ValueError("Invalid response format from API")

            prompt_data = response["data"]["result"]
            ai_platform = prompt_data["prompt"]["aiPlatform"]
            messages = prompt_data["messages"]

            # Extract and format the prompt details
            prompt_details = {
                "ai_platform": ai_platform["platform"],
                "model": ai_platform["model"],
                "system_prompt": messages["systemMessage"],
                "temperature": ai_platform["temp"],
                "max_tokens": ai_platform["max_tokens"],
                # Additional parameters from the API
                "top_p": ai_platform["top_p"],
                "frequency_penalty": ai_platform["frequency_penalty"],
                "presence_penalty": ai_platform["presence_penalty"],
                "response_format": ai_platform["response_format"],
                "version": version,  # Include version in prompt details
            }

            logger.info(
                f"Successfully fetched details for prompt_id: {prompt_id}, version: {version}"
            )
            logger.debug(f"Prompt details: {prompt_details}")

            # Cache the prompt details
            cache_key = f"{prompt_id}_v{version}"
            logger.info(f"Caching details with key: {cache_key}")
            CacheManager.set_prompt_details(cache_key, prompt_details)

            return prompt_details

        except Exception as e:
            logger.error(f"Error fetching prompt details: {str(e)}")
            raise

    async def _make_openai_request(self, prompt_details: Dict, payload: Dict) -> Dict:
        """Make a direct request to OpenAI"""
        logger.info("Preparing OpenAI API request")

        # Extract the user message text from the messages array
        messages = payload.get("user_message", [])

        # Handle both message formats
        user_messages = []
        for msg in messages:
            if "role" in msg:
                if msg["role"] == "user":
                    user_messages.append(msg)
            elif "type" in msg:
                # Convert old format to new format
                user_messages.append({"role": "user", "content": [msg]})

        if not user_messages:
            logger.error("No user message found in payload")
            raise ValueError("User message is required for OpenAI requests")

        # Format messages for OpenAI
        formatted_messages = []
        for msg in messages:
            if "role" in msg:
                if msg["role"] == "system":
                    content = next(
                        (
                            item["text"]
                            for item in msg["content"]
                            if item.get("type") == "text"
                        ),
                        "",
                    )
                    formatted_messages.append({"role": "system", "content": content})
                elif msg["role"] == "user":
                    content = next(
                        (
                            item["text"]
                            for item in msg["content"]
                            if item.get("type") == "text"
                        ),
                        "",
                    )
                    formatted_messages.append({"role": "user", "content": content})
                elif msg["role"] == "assistant":
                    content = (
                        msg["content"]
                        if isinstance(msg["content"], str)
                        else json.dumps(msg["content"])
                    )
                    formatted_messages.append({"role": "assistant", "content": content})
            elif "type" in msg:
                # Handle old format
                formatted_messages.append({"role": "user", "content": msg["text"]})

        try:
            logger.info("Making request to OpenAI API")
            response = openai_interaction(
                secret_key=self.api_key,
                model=prompt_details["model"],
                messages=formatted_messages,
                temperature=prompt_details.get("temp", 0.7),
                max_tokens=prompt_details["max_tokens"],
                top_p=prompt_details.get("top_p", 0.5),
                frequency_penalty=prompt_details.get("frequency_penalty", 0.7),
                presence_penalty=prompt_details.get("presence_penalty", 0.3),
                response_format={"type": "text"},
            )
            logger.info("Successfully received response from OpenAI")
            return response
        except Exception as e:
            logger.error(f"Error making OpenAI request: {str(e)}")
            raise

    async def _make_anthropic_request(
        self, prompt_details: Dict, payload: Dict
    ) -> Dict:
        """Make a direct request to Anthropic"""
        logger.info("Preparing Anthropic API request")
        user_message = next(
            (msg for msg in payload["user_message"] if msg["type"] == "text"), None
        )
        if not user_message:
            logger.error("No text message found in payload")
            raise ValueError("Text message is required for Anthropic requests")

        try:
            logger.info("Making request to Anthropic API")
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": self.api_key,
                    "Content-Type": "application/json",
                },
                json={
                    "model": prompt_details["model"],
                    "messages": [
                        {"role": "system", "content": prompt_details["system_prompt"]},
                        {"role": "user", "content": user_message["text"]},
                    ],
                    "max_tokens": prompt_details["max_tokens"],
                },
            )
            response.raise_for_status()
            data = response.json()
            logger.info("Successfully received response from Anthropic")
            return {"response": data["content"][0]["text"]}
        except Exception as e:
            logger.error(f"Error making Anthropic request: {str(e)}")
            raise

    async def _direct_ai_request(self, prompt_id: str, payload: Dict) -> Dict:
        """Handle direct AI platform requests"""
        logger.info(f"Processing direct AI request for prompt_id: {prompt_id}")

        # Get version from payload
        version = (
            str(payload.get("version")) if payload.get("version") is not None else None
        )

        if version:
            cache_key = f"{prompt_id}_v{version}"
            prompt_details = CacheManager.get_prompt_details(cache_key)
        else:
            # Try to find latest version in cache
            prompt_details = None
            logger.info("No version specified, will fetch latest version")

        if not prompt_details:
            logger.info(f"Prompt details not found in cache, fetching from server")
            prompt_details = await self._fetch_and_cache_prompt_details(
                prompt_id, version
            )
            version = prompt_details[
                "version"
            ]  # Get the version (might be latest if none was specified)

        logger.info(
            f"Making request to AI platform: {prompt_details['ai_platform']} with version {version}"
        )
        try:
            if prompt_details["ai_platform"] == "openai":
                return await self._make_openai_request(prompt_details, payload)
            elif prompt_details["ai_platform"] == "anthropic":
                return await self._make_anthropic_request(prompt_details, payload)
            else:
                logger.error(
                    f"Unsupported AI platform: {prompt_details['ai_platform']}"
                )
                raise ValueError(
                    f"Unsupported AI platform: {prompt_details['ai_platform']}"
                )
        except Exception as e:
            logger.error(f"Error in direct AI request: {str(e)}")
            raise

    async def chat_with_prompt(
        self,
        prompt_id: str,
        user_message: List[Dict[str, Union[str, Dict[str, str]]]],
        memory_type: str,
        window_size: int,
        session_id: str,
        variables: Dict[str, str],
        version: Optional[int] = None,
    ) -> Dict[str, str]:
        """
        Chat with a specific prompt

        Args:
            prompt_id: ID of the prompt
            user_message: List of message dictionaries
            memory_type: Type of memory ('fullMemory', 'windowMemory', or 'summarizedMemory')
            window_size: Size of the memory window
            session_id: Session identifier
            variables: Dictionary of variables
            version: Optional version number

        Returns:
            Dictionary containing the response
        """
        logger.info(f"Starting chat with prompt_id: {prompt_id}")
        payload = {
            "user_message": user_message,
            "memory_type": memory_type,
            "window_size": window_size,
            "session_id": session_id,
            "variables": variables,
            "request_from": "python_sdk",
            "env": self.env,
        }

        if version is not None:
            logger.info(f"Using prompt version: {version}")
            payload["version"] = version

        try:
            if self.bypass:
                logger.info("Bypass mode enabled, making direct AI request")
                return await self._direct_ai_request(prompt_id, payload)
            else:
                logger.info("Making request to PromptStudio API")
                return self._request(
                    f"/chat_with_prompt_version/{prompt_id}",
                    method="POST",
                    json=payload,
                )
        except Exception as e:
            logger.error(f"Error in chat_with_prompt: {str(e)}")
            raise

    async def _make_ai_platform_request(
        self,
        platform_name: str,
        prompt_details: Dict,
        messages: List[Dict],
        system_message: str,
    ) -> Dict:
        """
        Make request to the appropriate AI platform

        Args:
            platform_name: Name of the AI platform (openai, anthropic, etc.)
            prompt_details: Dictionary containing prompt configuration
            messages: List of messages to send
            system_message: System message to use

        Returns:
            Dictionary containing the response
        """
        logger.info(f"Making request to AI platform: {platform_name}")

        try:
            if platform_name.lower() == "openai":
                return await self._make_openai_request(
                    prompt_details, {"user_message": messages}
                )
            elif platform_name.lower() == "anthropic":
                return await self._make_anthropic_request(
                    prompt_details, {"user_message": messages}
                )
            elif platform_name.lower() == "gemini":

                # Format messages for Gemini
                formatted_messages = format_messages_for_gemini(
                    messages, system_message
                )

                # Extract user message from the last message
                last_message = messages[-1]
                user_message = next(
                    (
                        item["text"]
                        for item in last_message["content"]
                        if item["type"] == "text"
                    ),
                    "",
                )

                return gemini_interaction_chat_with_prompt(
                    secret_key=self.api_key,
                    model=prompt_details["model"],
                    messages=formatted_messages,
                    system_message=system_message,
                    temperature=prompt_details.get("temp", 0.7),
                    max_output_tokens=prompt_details.get("max_tokens", 1000),
                    top_p=prompt_details.get("top_p", 0.8),
                    top_k=prompt_details.get("top_k", 40),
                    user_message=user_message,
                    response_format=prompt_details.get(
                        "response_format", {"type": "text"}
                    ),
                )
            else:
                error_msg = f"Unsupported AI platform: {platform_name}"
                logger.error(error_msg)
                raise ValueError(error_msg)

        except Exception as e:
            logger.error(f"Error in _make_ai_platform_request: {str(e)}")
            raise


def openai_interaction(
    secret_key,
    model,
    messages,
    temperature,
    max_tokens,
    top_p,
    frequency_penalty,
    presence_penalty,
    response_format,
):
    """
    Make a request to OpenAI API
    """
    # Set the OpenAI API key
    openai.api_key = secret_key

    # Call the OpenAI API
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        response_format=response_format,
    )

    assistant_reply = response.choices[0].message["content"].strip()

    if response_format["type"] == "text":
        # For text responses, try to parse JSON if it's in that format
        try:
            parsed_reply = json.loads(assistant_reply)
            if (
                isinstance(parsed_reply, list)
                and len(parsed_reply) > 0
                and "text" in parsed_reply[0]
            ):
                assistant_reply = parsed_reply[0]["text"]
            elif isinstance(parsed_reply, str):
                assistant_reply = parsed_reply
        except json.JSONDecodeError:
            # If it's not valid JSON, keep the original string
            pass

        # Remove surrounding quotes if present, handling both single and double quotes
        assistant_reply = assistant_reply.strip('"')

        # If it's still a valid JSON string, parse it one more time
        try:
            parsed_reply = json.loads(assistant_reply)
            if isinstance(parsed_reply, str):
                assistant_reply = parsed_reply
        except json.JSONDecodeError:
            pass
    else:
        # For JSON responses, parse the JSON string
        assistant_reply = json.loads(assistant_reply)

    return {
        "response": assistant_reply,
    }


def format_messages_for_gemini(messages, system_message=None):
    formatted_messages = []

    for i, msg in enumerate(messages):
        role = msg.get("role")
        content = msg.get("content")

        if isinstance(content, list):
            text_content = " ".join(
                [
                    (
                        part.get("text", "")
                        if isinstance(part.get("text"), str)
                        else json.dumps(part.get("text", ""))
                    )
                    for part in content
                    if part.get("type") == "text"
                ]
            )
        elif isinstance(content, str):
            text_content = content
        else:
            text_content = json.dumps(content)

        if i == 0 and system_message:
            text_content = f"{system_message}\n\n{text_content}"

        formatted_messages.append(
            {
                "role": "user" if role in ["user", "system"] else "model",
                "parts": [{"text": text_content}],
            }
        )

    return formatted_messages


def create_response_schema(payload: dict) -> content.Schema:
    def create_property_schema(prop):
        if isinstance(prop["type"], list):
            # Handle multiple types
            return content.Schema(
                type=content.Type.UNION,
                items=[
                    create_property_schema({"type": t})
                    for t in prop["type"]
                    if t != "null"
                ],
            )
        elif prop["type"] == "string":
            return content.Schema(type=content.Type.STRING)
        elif prop["type"] == "integer":
            return content.Schema(type=content.Type.INTEGER)
        elif prop["type"] == "number":
            return content.Schema(type=content.Type.NUMBER)
        elif prop["type"] == "boolean":
            return content.Schema(type=content.Type.BOOLEAN)
        elif prop["type"] == "array":
            if "items" in prop:
                return content.Schema(
                    type=content.Type.ARRAY, items=create_property_schema(prop["items"])
                )
            return content.Schema(type=content.Type.ARRAY)
        elif prop["type"] == "object":
            return create_response_schema(prop)
        else:
            return content.Schema(
                type=content.Type.STRING
            )  # Default to string for unknown types

    properties = {}
    for key, value in payload["properties"].items():
        properties[key] = create_property_schema(value)

    required = payload.get("required", [])
    return content.Schema(
        type=content.Type.OBJECT, properties=properties, required=required
    )


def gemini_interaction_chat_with_prompt(
    secret_key,
    model,
    messages,
    system_message,
    temperature,
    max_output_tokens,
    top_p,
    top_k,
    user_message,
    response_format,
):
    genai.configure(api_key=secret_key)

    if system_message and system_message.strip():
        gemini_model = genai.GenerativeModel(
            model_name=model, system_instruction=system_message
        )
    else:
        gemini_model = genai.GenerativeModel(model_name=model)

    if response_format["type"] == "text":
        response_schema = content.Schema(type=content.Type.STRING)
        response_mime_type = "text/plain"
    else:
        response_schema = create_response_schema(response_format)
        response_mime_type = "application/json"

    try:
        complete_history = messages.copy()
        complete_history.append({"role": "user", "parts": [{"text": user_message}]})

        response = gemini_model.generate_content(
            complete_history,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=max_output_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                response_schema=response_schema,
                response_mime_type=response_mime_type,
            ),
        )

        if response.candidates:
            if response_mime_type == "text/plain":
                assistant_reply = response.candidates[0].content.parts[0].text
                assistant_reply = assistant_reply.lstrip("Assistant:").strip()
            else:
                assistant_reply = response.candidates[0].content.parts[0].text
                assistant_reply = json.loads(assistant_reply)
        else:
            logger.warning("No candidates in the response")
            assistant_reply = (
                "I'm sorry, but I couldn't generate a response. Please try again."
            )

        return {
            "response": assistant_reply,
        }
    except generation_types.BlockedPromptException as e:
        raise ValueError(f"Gemini API error: The prompt was blocked. Reason: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error occurred: {str(e)}")
