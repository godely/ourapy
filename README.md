# Oura API Client

A Python client library for interacting with the Oura Ring API v2.

## Features

- Type-annotated API client for Python 3.7+
- Support for Oura API v2 endpoints
- Data models for API responses
- Simple and intuitive interface

## Installation

### From PyPI (not yet available)

```bash
pip install oura-api-client
```

### From Source

```bash
git clone https://github.com/yourusername/oura-api-client.git
cd oura-api-client
pip install -e .
```

## Authentication

You'll need an API token to use the Oura API. You can get one from the [Oura Cloud Personal Access Tokens page](https://cloud.ouraring.com/personal-access-tokens).

## Usage

```python
from oura_api_client.api.client import OuraClient

# Initialize the client with your access token
client = OuraClient("your_access_token_here")

# Get heart rate data for a specific date range
heart_rate = client.heartrate.get_heartrate(
    start_date="2024-03-01",
    end_date="2024-03-15"
)

# Access the data using the model
for sample in heart_rate.data:
    print(f"Time: {sample.timestamp}, BPM: {sample.bpm}")

# Get personal information
personal_info = client.personal.get_personal_info()
print(f"User ID: {personal_info.id}")
print(f"Email: {personal_info.email}")
```

### Using Raw Responses

If you prefer to work with the raw API responses:

```python
# Get the raw JSON response
heart_rate_raw = client.heartrate.get_heartrate(
    start_date="2024-03-01",
    end_date="2024-03-15",
    return_model=False
)

# Now you have the raw dictionary
print(heart_rate_raw)
```

## Available Endpoints

### Heart Rate

- `client.heartrate.get_heartrate(start_date=None, end_date=None, return_model=True)`

### Personal Info

- `client.personal.get_personal_info(return_model=True)`

## Development

### Setup

```bash
git clone https://github.com/yourusername/oura-api-client.git
cd oura-api-client
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 