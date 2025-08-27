# Webdock API Python SDK

A type-safe Python wrapper for the Webdock.io API.

## Documentation

Full API documentation is available at [api.webdock.io](https://api.webdock.io)

## Installation

```bash
pip install webdock
```

## Quick Start

Each operation returns both body and headers that you can access using the `get()` method:

```python
import time
from webdock import webdock
from requests import RequestException

def main():
    # Initialize client with your API token
    client = webdock.Webdock("your_api_token_here")
    
    try:
        # Create a new server
        server = client.servers.create(
            imageSlug="ubuntu-20-04-x64",
            locationId="pl-waw",
            name="test-server",
            profileSlug="s-1vcpu-1gb",
        )
        
        # Access server data from response body
        aliases = server.get("body").get("aliases")
        print(f"Server aliases: {aliases}")
        
        # Access callback ID from headers to track provision operation state
        callback_id = server.get("headers").get("x_callback_id")
        print(f"Callback ID: {callback_id}")
        
    except RequestException as e:
        print(f"API request failed: {e}")

if __name__ == "__main__":
    main()
```

## Response Structure

All API operations return a response object with two main components:

- **`body`**: Contains the actual API response data
- **`headers`**: Contains HTTP headers, including tracking information like `x_callback_id`

### Example Usage

```python
# Get server information
server_info = server.get("body")
server_name = server_info.get("name")
server_status = server_info.get("status")

# Track operations using headers
callback_id = server.get("headers").get("x_callback_id")
```

## Backward Compatibility

The legacy package is still available but deprecated. You can import it for existing projects:

```python
import time
from oldwebdock.webdock import Webdock
from requests import RequestException

def main():
    client = Webdock("your_api_token_here")
    
    try:
        # Create webhook (legacy syntax)
        webhook = client.create_hook(
            hookType="foo",
            hookValue="https://your-webhook-url.com"
        )
        
        # Access response data (same pattern as new SDK)
        webhook_id = webhook.get("body").get("id")
        callback_id = webhook.get("headers").get("x_callback_id")
        
    except RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    main()
```

> **⚠️ Deprecation Notice**: legacy package is now deprecated. Please migrate to the new SDK for continued support and updates.

## Features

- **Type-safe**: Full type hints for better IDE support and error catching
- **Easy to use**: Simple, intuitive API interface
- **Error handling**: Built-in exception handling with detailed error messages
- **Async support**: Non-blocking operations for better performance
- **Comprehensive**: Full coverage of Webdock API endpoints

## Support

- [API Documentation](https://api.webdock.io)
- [GitHub Issues](https://github.com/webdock-io/python-sdk/issues)
- [Webdock Support](https://webdock.io/support)
