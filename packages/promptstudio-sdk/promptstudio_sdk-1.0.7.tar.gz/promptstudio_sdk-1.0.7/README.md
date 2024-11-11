# PromptStudio Python SDK

A Python SDK for interacting with PromptStudio API and AI platforms directly.

## Installation

### From PyPI (Coming Soon)

```bash
pip install promptstudio-sdk
```

### From Source

```bash
git clone https://github.com/your-repo/promptstudio-sdk.git
cd promptstudio-sdk
pip install -e .
```

## Development Setup

1. Create a virtual environment:

```bash
python -m venv venv
```

2. Activate the virtual environment:

```bash
# On Windows
venv\Scripts\activate

# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Initializing the SDK

```python
from promptstudio_sdk import PromptStudio

client = PromptStudio({
    'api_key': 'YOUR_API_KEY',
    'env': 'test'  # Use 'prod' for production environment
})
```

### Getting All Prompts

```python
# Get all prompts from a specific folder
prompts = client.get_all_prompts("your_folder_id")
print(prompts)
```

### Chatting with a Prompt

```python
response = client.chat_with_prompt(
    prompt_id="your_prompt_id",
    user_message=[
        {
            "type": "text",
            "text": "Hello, how are you?"
        }
    ],
    memory_type="fullMemory",
    window_size=10,
    session_id="test_session",
    variables={}
)

print(response)
```

### Complete Example

```python
from promptstudio_sdk import PromptStudio

def main():
    # Initialize the client
    client = PromptStudio({
        'api_key': 'YOUR_API_KEY',
        'env': 'test'
    })

    try:
        # Get all prompts
        prompts = client.get_all_prompts("your_folder_id")
        print("Available prompts:", prompts)

        # Chat with a specific prompt
        response = client.chat_with_prompt(
            prompt_id="your_prompt_id",
            user_message=[
                {
                    "type": "text",
                    "text": "Hello, how are you?"
                }
            ],
            memory_type="windowMemory",
            window_size=10,
            session_id="test_session",
            variables={}
        )
        print("Chat response:", response)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
```

## Testing

### Setting Up Tests

1. Install test dependencies:

```bash
pip install pytest pytest-cov
```

2. Create a `.env` file in the root directory with your test credentials:

```env
PROMPTSTUDIO_API_KEY=your_test_api_key
PROMPTSTUDIO_ENV=test
```

### Running Tests

Run all tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=promptstudio_sdk
```

### Writing Tests

Create test files in the `tests` directory. Here's an example test:

```python
import pytest
from promptstudio_sdk import PromptStudio

def test_chat_with_prompt():
    client = PromptStudio({
        'api_key': 'test_api_key',
        'env': 'test'
    })

    response = client.chat_with_prompt(
        prompt_id="test_prompt",
        user_message=[{"type": "text", "text": "Hello"}],
        memory_type="fullMemory",
        window_size=10,
        session_id="test_session",
        variables={}
    )

    assert isinstance(response, dict)
    assert 'response' in response

```

## Type Hints

The SDK uses Python type hints for better IDE support and code documentation. Here are some key types:

```python
from typing import Dict, List, Union, Optional

# Message types
ImageMessage = Dict[str, Union[str, Dict[str, str]]]  # {"type": "image_url", "image_url": {"url": "..."}}
TextMessage = Dict[str, str]  # {"type": "text", "text": "..."}
UserMessage = List[Union[ImageMessage, TextMessage]]

# Memory types
Memory = Literal["fullMemory", "windowMemory", "summarizedMemory"]

# Request payload
RequestPayload = Dict[str, Union[UserMessage, Memory, int, str, Dict[str, str], Optional[int]]]
```

## Error Handling

The SDK raises exceptions for various error cases:

```python
from promptstudio_sdk import PromptStudio

try:
    client = PromptStudio({
        'api_key': 'YOUR_API_KEY',
        'env': 'test'
    })
    response = client.chat_with_prompt(...)
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except requests.exceptions.RequestException as e:
    print(f"Network error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Run the tests to ensure everything works
5. Submit a pull request

## License

This SDK is released under the MIT License.
