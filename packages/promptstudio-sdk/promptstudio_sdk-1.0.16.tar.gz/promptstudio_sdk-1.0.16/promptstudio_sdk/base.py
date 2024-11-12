from typing import Dict, Any, TypedDict, Optional
import aiohttp
import logging

logger = logging.getLogger(__name__)


class ConfigDict(TypedDict):
    api_key: str
    env: str
    bypass: Optional[bool]


class Base:
    def __init__(self, config: ConfigDict):
        """
        Initialize the base class with configuration

        Args:
            config: Dictionary containing:
                - 'api_key': API key
                - 'env': Environment ('test' or 'prod')
                - 'bypass': Optional boolean to bypass PromptStudio server
        """
        self.api_key = config["api_key"]
        self.env = config["env"]
        self.bypass = config.get("bypass", False)

        self.base_url = (
            "https://api.promptstudio.dev/api/v1"
            if self.env == "prod"
            else "https://api.playground.promptstudio.dev/api/v1"
        )

    async def _request(
        self, endpoint: str, method: str = "GET", **kwargs
    ) -> Dict[str, Any]:
        """
        Make async HTTP requests to the API
        """
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json", "x-api-key": self.api_key}

        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method, url=url, headers=headers, **kwargs
            ) as response:
                response.raise_for_status()
                return await response.json()
