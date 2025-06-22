# Oura API Client

A comprehensive Python client library for the Oura Ring API v2 with full type annotations, automatic retry logic, and extensive endpoint coverage.

## Features

- ✅ **Complete API Coverage**: All 20+ Oura API v2 endpoints implemented
- 🔒 **Type Safety**: Full type annotations with Pydantic models
- 🔄 **Automatic Retry Logic**: Built-in exponential backoff for transient failures
- ⚡ **Modern Python**: Support for Python 3.7+
- 🎯 **Intuitive Interface**: Simple, consistent API across all endpoints
- 📊 **Comprehensive Error Handling**: Detailed error messages and proper exception hierarchy
- 🔧 **Flexible Configuration**: Customizable retry behavior and timeout settings

## Installation

### From PyPI (not yet available)

```bash
pip install oura-api-client
```

### From Source

```bash
git clone https://github.com/godely/ourapy.git
cd ourapy
pip install -e .
```

## Authentication

You'll need an API token to use the Oura API. You can get one from the [Oura Cloud Personal Access Tokens page](https://cloud.ouraring.com/personal-access-tokens).

## Quick Start

```python
from oura_api_client import OuraClient

# Initialize the client with your access token
client = OuraClient("your_access_token_here")

# Get sleep data for the past week
sleep_data = client.daily_sleep.get_daily_sleep_documents(
    start_date="2024-12-15",
    end_date="2024-12-22"
)

for sleep in sleep_data.data:
    print(f"Date: {sleep.day}")
    print(f"Sleep Score: {sleep.score}")
    print(f"Total Sleep: {sleep.total_sleep_duration / 3600:.1f} hours")
    print(f"REM Sleep: {sleep.rem_sleep_duration / 3600:.1f} hours")
    print("---")

# Get activity data with automatic retry on failure
activity = client.daily_activity.get_daily_activity_documents(
    start_date="2024-12-01"
)

for day in activity.data:
    print(f"Steps: {day.steps}, Calories: {day.active_calories}")
```

## Error Handling

The client includes comprehensive error handling with automatic retries:

```python
from oura_api_client import OuraClient, OuraAPIError
from oura_api_client.utils import RetryConfig

# Configure custom retry behavior
retry_config = RetryConfig(
    max_retries=5,
    base_delay=2.0,
    max_delay=60.0
)

client = OuraClient("your_token", retry_config=retry_config)

try:
    readiness = client.daily_readiness.get_daily_readiness_document("invalid_id")
except OuraAPIError as e:
    print(f"API Error: {e}")
    print(f"Status Code: {e.status_code}")
    print(f"Endpoint: {e.endpoint}")
```

The client automatically retries on:
- 429 (Rate Limited) - respects Retry-After header
- 500, 502, 503, 504 (Server Errors)
- Connection timeouts
- Network errors

## Available Endpoints

### Daily Summaries
- **Daily Activity**: `client.daily_activity` - Steps, calories, activity levels
- **Daily Readiness**: `client.daily_readiness` - Recovery and readiness scores
- **Daily Sleep**: `client.daily_sleep` - Sleep stages, duration, and quality
- **Daily Stress**: `client.daily_stress` - Stress levels and recovery metrics
- **Daily Resilience**: `client.daily_resilience` - Long-term stress resilience
- **Daily SpO2**: `client.daily_spo2` - Blood oxygen levels
- **Daily Cardiovascular Age**: `client.daily_cardiovascular_age` - Cardiovascular health metrics

### Detailed Data
- **Sleep Sessions**: `client.sleep` - Detailed sleep session data
- **Activity Sessions**: `client.session` - Workout and activity sessions
- **Heart Rate**: `client.heartrate` - Time-series heart rate data
- **HRV Data**: Available within sleep and session data
- **Workouts**: `client.workout` - Detailed workout metrics
- **VO2 Max**: `client.vo2_max` - Cardio fitness metrics

### User Data
- **Personal Info**: `client.personal` - User profile information
- **Ring Configuration**: `client.ring_configuration` - Ring settings and info
- **Rest Mode Periods**: `client.rest_mode_period` - Rest mode status
- **Tags**: `client.tag` - User-generated tags
- **Enhanced Tags**: `client.enhanced_tag` - AI-enhanced tag data
- **Sleep Time**: `client.sleep_time` - Recommended bedtime windows

### Each endpoint supports:
- `get_xxx_documents()` - Get multiple documents with pagination
- `get_xxx_document(document_id)` - Get a single document by ID
- Date filtering with `start_date` and `end_date` (accepts strings or date objects)
- Pagination with `next_token`

## Advanced Usage

### Pagination

```python
# Iterate through all sleep data using pagination
next_token = None
all_sleep_data = []

while True:
    response = client.daily_sleep.get_daily_sleep_documents(
        start_date="2024-01-01",
        next_token=next_token
    )
    all_sleep_data.extend(response.data)
    
    if not response.next_token:
        break
    next_token = response.next_token

print(f"Total sleep records: {len(all_sleep_data)}")
```

### Working with Time Series Data

```python
# Get detailed heart rate data
hr_data = client.heartrate.get_heartrate(start_date="2024-12-20")

for hr in hr_data.data:
    # hr.bpm is time-series data with interval and items
    print(f"Started at: {hr.bpm.timestamp}")
    print(f"Interval: {hr.bpm.interval} seconds")
    print(f"Heart rates: {hr.bpm.items[:10]}...")  # First 10 readings
```

### Date Flexibility

```python
from datetime import date, timedelta

# All of these work:
today = date.today()
yesterday = today - timedelta(days=1)

# Using date objects
data1 = client.daily_activity.get_daily_activity_documents(
    start_date=yesterday,
    end_date=today
)

# Using ISO format strings
data2 = client.daily_activity.get_daily_activity_documents(
    start_date="2024-12-01",
    end_date="2024-12-20"
)
```

## Development

### Setup

```bash
git clone https://github.com/godely/ourapy.git
cd ourapy
pip install -r requirements-dev.txt
pip install -e .
```

### Running Tests

```bash
# Run all tests with parallel execution
pytest -n auto

# Run with coverage
pytest --cov=oura_api_client

# Run specific test file
pytest tests/test_client.py -v
```

### Code Quality

```bash
# Linting
flake8 oura_api_client/ tests/

# Type checking (if mypy is installed)
mypy oura_api_client/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 