# Tailli API Client

A high-performance Python client for Tailli API key management and usage tracking. This client provides easy-to-use async interfaces with built-in caching and background usage recording for optimal performance - track consumption accurately without adding latency to your APIs.

## Features

- 🚀 Asynchronous API with proper connection management
- 💾 Local caching of API key validation
- 🔄 Background usage recording with automatic retries
- ⚡ Low-latency operations prioritizing your application's performance
- 🛡️ Type-safe with full typing support

## Installation

```bash
pip install tailli
```

## Quick Start

```python
from tailli import TailliClient

async def main():
    async with TailliClient() as client:
        # Validate an API key and use it in a session
        api_key = "your-api-key"
        try:
            async with client.validated_session(api_key):
                # Your API calls here
                await client.record_usage(api_key, 5)
        except InvalidApiKeyError:
            print("Invalid API key")

if __name__ == "__main__":
    asyncio.run(main())
```

For more examples, check out the [examples directory](examples/basic_usage.py).


## Building and Publishing

1. Install build tools:
   ```bash
   pip install build twine
   ```

2. Build the package:
   ```bash
   python -m build
   ```

3. Test the build locally:
   ```bash
   pip install dist/tailli-0.1.0.tar.gz
   ```

4. Upload to PyPI:
   ```bash
   python -m twine upload dist/*
   ```

## Project Structure

```
tailli/
├── pyproject.toml      # Project configuration and dependencies
├── setup.cfg           # Additional build configuration
├── README.md           # This file
├── LICENSE             # MIT License
├── requirements.txt    # Python dependencies
├── src/
│   └── tailli/         # Main package code
│       ├── __init__.py
│       ├── client.py   # Core client implementation
│       ├── models.py   # Pydantic models
│       └── utils.py    # Utility functions
├── tests/              # Test suite
└── examples/           # Example code
```

## Sample Implementation

The reference implementation can be found in the [examples directory](examples/basic_usage.py). This shows the recommended way to use the client, including:

- API key validation
- Usage recording
- Error handling
- Async context management


## License

The Tailli Client (but not the Tailli backend) is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.