# Supabase-Logger

A Python package for logging AI bot responses to Supabase.

## Installation

You can install the package directly from the repository:

```bash
pip install -e .
```

## Usage

### Basic Usage

```python
from supabase_logger import SupabaseLogger

# Create a logger instance
logger = SupabaseLogger()

# Log a successful bot response
logger.log_success(
    user_id="user123",
    channel_id="channel456",
    thread_id="thread789",
    user_message="Hello, bot!",
    response_text="Hello, human!",
    request_time=datetime.now(timezone.utc) - timedelta(seconds=1),
    response_time=datetime.now(timezone.utc),
    bot_id="bot001",
    bot_name="AI Assistant",
    system_prompt="You are a helpful assistant."
)
```

### Environment Variables

The package uses the following environment variables:

- `SUPABASE_URL`: The URL of your Supabase instance
- `SUPABASE_API_KEY`: Your Supabase API key
- `SUPABASE_AUTH_EMAIL`: Email for Supabase authentication
- `SUPABASE_AUTH_PASSWORD`: Password for Supabase authentication
- `ENVIRONMENT`: Environment name (e.g., "development", "production")

## Features

- Singleton pattern ensures only one logger instance exists
- Automatic token management (authentication and refresh)
- Error handling with retry mechanism
- Configurable through environment variables
