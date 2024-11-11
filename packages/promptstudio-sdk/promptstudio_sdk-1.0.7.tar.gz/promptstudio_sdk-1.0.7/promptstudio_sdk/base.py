from typing import Dict, Any, TypedDict, Optional
import requests


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

    def _request(self, endpoint: str, method: str = "GET", **kwargs) -> Dict[str, Any]:
        """
        Make HTTP requests to the API

        Args:
            endpoint: API endpoint
            method: HTTP method
            **kwargs: Additional arguments for the request

        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json", "x-api-key": self.api_key}

        response = requests.request(method=method, url=url, headers=headers, **kwargs)

        response.raise_for_status()
        return response.json()
