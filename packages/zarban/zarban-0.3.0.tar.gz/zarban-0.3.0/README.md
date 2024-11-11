# Zarban

![Logo](assets/zarban.ico)
[![PyPI version](https://badge.fury.io/py/zarban.svg)](https://badge.fury.io/py/zarban)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/zarban.svg)](https://pypi.org/project/zarban/)

Zarban SDK is a Python interface for interacting with the Zarban DeFi protocol, enabling developers to seamlessly integrate lending and borrowing functionalities into their applications. This SDK simplifies complex DeFi operations by providing easy-to-use methods for lending assets, managing collateral, borrowing funds, and monitoring positions in the Zarban protocol.

## Features

- **Automated API Client Generation**: Built using OpenAPI specification, ensuring type safety and up-to-date API compatibility
- **Lending Operations**: Easily deposit assets, view lending rates, and manage lending positions
- **Borrowing Management**: Streamlined methods for borrowing assets, managing collateral, and monitoring loan health
- **Position Tracking**: Real-time access to user positions, including borrowed amounts, collateral ratios, and liquidation thresholds
- **Market Data**: Simple methods to fetch current interest rates, available liquidity, and market statistics
- **Type Safety**: Full type hints support for Python static type checking
- **Error Handling**: Comprehensive error handling with detailed exceptions for DeFi operations
- **Async Support**: Asynchronous methods for improved performance in high-throughput applications

## Installation

```bash
pip install zarban
```

For development installation:

```bash
git https://github.com/zarbanio/zarban-py.git
cd zarban-py
pip install -e ".[dev]"
```

## Quick Start

Zarban SDK provides access to two distinct APIs:

### 1. Wallet API (`zarban.wallet`)

The Wallet API handles user authentication and wallet management operations.

### 2. Service API(`zarban.service`)

The Zarban Service API provides access to core DeFi protocol operations.

```python
from zarban.wallet.openapi_client import DefaultApi, ApiClient, Configuration

# Initialize the client
configuration = Configuration()
api_client = ApiClient(configuration)
api_instance = DefaultApi(api_client)

# Make a simple API call
response = api_instance.some_method()
print(response)
```

## Usage Examples

### Advanced Usage

Here's a simple example to sign up and get started with Zarban:

```python
from zarban.wallet.openapi_client import Configuration, ApiClient
from zarban.wallet.openapi_client.api.default_api import DefaultApi
from zarban.wallet.openapi_client.models.sign_up_request import SignUpRequest

# Initialize the API client
config = Configuration(host="https://wapi.zarban.io")
client = DefaultApi(ApiClient(config))

# Sign up a new user
signup_data = SignUpRequest(
    email="user@example.com",
    password="securepassword123"
)

try:
    # Perform signup
    response = client.auth_signup_post(signup_data)
    print(f"Signup successful! Token: {response.token}")

    # Set token for future authenticated requests
    config.access_token = response.token

except Exception as e:
    print(f"Error during signup: {e}")
```

## Configuration

The SDK can be configured with various options to customize its behavior and authentication methods.

### Basic Configuration

```python
from zarban.wallet.openapi_client import Configuration

# Basic configuration with just the host URL
config = Configuration(host="https://wapi.zarban.io")
```

### Authentication Options

The SDK supports multiple authentication methods:

1. API Key Authentication:

```python
config = Configuration(
    host="https://wapi.zarban.io",
    api_key={"APIKeyAuth": "your-api-key-here"},
    # Optional: Add prefix like 'Bearer' for the API key
    api_key_prefix={"APIKeyAuth": "Bearer"}
)
```

2. Basic Authentication:

```python
config = Configuration(
    host="https://wapi.zarban.io",
    username="your-username",
    password="your-password"
)
```

### Advanced Configuration

```python
config = Configuration(
    host="https://wapi.zarban.io",
    api_key={"APIKeyAuth": "your-api-key-here"},
    # Discard unknown properties from server responses
    discard_unknown_keys=True
)
```

### Configuration Parameters

| Parameter              | Type | Description                                                                           |
| ---------------------- | ---- | ------------------------------------------------------------------------------------- |
| `host`                 | str  | Base URL for the API endpoints                                                        |
| `api_key`              | dict | Dictionary of API keys where key is the security scheme name and value is the API key |
| `api_key_prefix`       | dict | Dictionary of API key prefixes (e.g., "Bearer")                                       |
| `username`             | str  | Username for HTTP basic authentication                                                |
| `password`             | str  | Password for HTTP basic authentication                                                |
| `discard_unknown_keys` | bool | Whether to discard unknown properties from server responses                           |

## Error Handling

```python
from zarban.service.openapi_client import StableCoinSystemApi, ApiClient, Configuration
from zarban.wallet.openapi_client.exceptions import ApiException

try:
    configuration = Configuration(host="https://api.zarban.io/v2")
    api_client = ApiClient(configuration)
    stable_coin_system_api = StableCoinSystemApi(api_client)
    response = StableCoinSystemApi.some_method()
except ApiException as e:
    print(f"An error occurred: {e}")
```

## Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/zarbanio/zarban-py.git
cd zarban-py

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- Create an issue on GitHub
- Email: info@zarban.io
- Documentation: [https://docs.zarban.io](https://docs.zarban.io)
