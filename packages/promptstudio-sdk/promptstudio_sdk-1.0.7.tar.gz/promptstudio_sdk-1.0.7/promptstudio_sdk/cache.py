from typing import Dict, Optional, List
from datetime import datetime
import uuid
import json


class CacheManager:
    _cache: Dict[str, Dict] = {}

    @classmethod
    def set_prompt_details(cls, prompt_id: str, details: Dict) -> None:
        cls._cache[prompt_id] = details

    @classmethod
    def get_prompt_details(cls, prompt_id: str) -> Optional[Dict]:
        return cls._cache.get(prompt_id)

    @classmethod
    def has_prompt_details(cls, prompt_id: str) -> bool:
        return prompt_id in cls._cache


class InteractionCacheManager:
    _interaction_cache: Dict[str, Dict] = {}
    _user_messages: Dict[str, Dict] = {}
    _prompt_access: Dict[str, Dict] = {}
    _prompt_version_messages: Dict[str, List] = {}

    @classmethod
    def save_user_messages(cls, prompt_id: str, messages: Dict) -> None:
        cls._user_messages[prompt_id] = messages

    @classmethod
    def get_user_messages(cls, prompt_id: str) -> Optional[Dict]:
        return cls._user_messages.get(prompt_id)

    @classmethod
    def save_interaction(cls, session_id: str, interaction_data: Dict) -> None:
        if session_id not in cls._interaction_cache:
            cls._interaction_cache[session_id] = {
                "messages": [],
                "lastResponseAt": None,
            }
        cls._interaction_cache[session_id]["messages"].extend(
            interaction_data["messages"]
        )
        cls._interaction_cache[session_id]["lastResponseAt"] = interaction_data[
            "lastResponseAt"
        ]

        prompt_version_key = (
            f"{interaction_data.get('prompt_id')}_{interaction_data.get('version')}"
        )
        if prompt_version_key not in cls._prompt_version_messages:
            cls._prompt_version_messages[prompt_version_key] = []
        cls._prompt_version_messages[prompt_version_key].extend(
            interaction_data["messages"]
        )

    @classmethod
    def get_interaction(cls, session_id: str) -> Optional[Dict]:
        return cls._interaction_cache.get(session_id)

    @classmethod
    def get_prompt_version_messages(cls, prompt_id: str, version: str) -> List:
        key = f"{prompt_id}_{version}"
        return cls._prompt_version_messages.get(key, [])

    @classmethod
    def clear_cache(cls) -> None:
        cls._interaction_cache.clear()
        cls._user_messages.clear()
        cls._prompt_access.clear()
        cls._prompt_version_messages.clear()
