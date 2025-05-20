# Supabase-Logger

A Python package for logging AI bot responses to Supabase.

## Installation

There are several ways to install the package:

### Direct Installation from GitHub

```bash
# Install the latest version
pip install git+https://github.com/chylli-deriv/supabase-logger.git

# Install a specific tag/version
pip install git+https://github.com/chylli-deriv/supabase-logger.git@v0.1.0

# Install a specific branch
pip install git+https://github.com/chylli-deriv/supabase-logger.git@main
```

### Using requirements.txt

Create a `requirements.txt` file with:

```
git+https://github.com/chylli-deriv/supabase-logger.git@v0.1.0
```

Then install with:

```bash
pip install -r requirements.txt
```

### Using pyproject.toml (Poetry)

If you're using Poetry, add this to your `pyproject.toml`:

```toml
[tool.poetry.dependencies]
python = ">=3.11"
supabase-logger = {git = "https://github.com/chylli-deriv/supabase-logger.git", rev = "v0.1.0"}
```

Then install with:

```bash
poetry install
```

### Local Development Installation

If you've cloned the repository locally:

```bash
# Clone the repository
git clone https://github.com/chylli-deriv/supabase-logger.git

# Navigate to the directory
cd supabase-logger

# Install in development mode
pip install -e .
```

## Usage

### Basic Usage

```python
import os
import logging
from datetime import datetime, timezone, timedelta
from supabase_logger import SupabaseLogger

# Set up logging (optional but recommended)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a logger instance (Singleton pattern ensures only one instance exists)
logger = SupabaseLogger()

# Current time for request/response timestamps
request_time = datetime.now(timezone.utc) - timedelta(seconds=1)
response_time = datetime.now(timezone.utc)

# Log a successful bot response
logger.log_success(
    user_id="user123",                # ID of the user who sent the message
    channel_id="channel456",          # ID of the channel where the message was sent
    thread_id="thread789",            # ID of the thread if message was in thread
    user_message="Hello, bot!",       # Original message from user
    response_text="Hello, human!",    # Bot's response text
    request_time=request_time,        # When the request was received
    response_time=response_time,      # When the response was sent
    bot_id="bot001",                  # Bot's unique identifier
    bot_name="AI Assistant",          # Type/name of the bot
    system_prompt="You are a helpful assistant.",  # System prompt used
    chat_history_length=5,            # Optional: Length of chat history
    input_attachments={"has_image": False},  # Optional: Any attachments in user's message
    output_attachments={}             # Optional: Any attachments in bot's response
)
```

### Setting Credentials

You can provide Supabase credentials in two ways:

#### 1. Using Environment Variables

```python
import os

# Set environment variables (in a real application, these would be set in the environment)
os.environ['SUPABASE_URL'] = 'https://your-supabase-url.supabase.co'
os.environ['SUPABASE_API_KEY'] = 'your-supabase-api-key'
os.environ['SUPABASE_AUTH_EMAIL'] = 'your-auth-email@example.com'
os.environ['SUPABASE_AUTH_PASSWORD'] = 'your-auth-password'
os.environ['ENVIRONMENT'] = 'development'

# Create logger (will use environment variables)
logger = SupabaseLogger()
```

#### 2. Passing Parameters Directly

```python
# Create logger with explicit parameters
logger = SupabaseLogger(
    url='https://your-supabase-url.supabase.co',
    api_key='your-supabase-api-key',
    auth_email='your-auth-email@example.com',
    auth_password='your-auth-password',
    environment='development'
)
```

Parameters take precedence over environment variables if both are provided.

### Disabling Logging

You can disable logging for specific instances:

```python
# Create a logger instance
logger = SupabaseLogger()

# Disable logging
logger.enabled = False

# This log will not be sent to Supabase
logger.log_success(...)
```

### Error Handling

The logger includes built-in error handling and will not raise exceptions that could affect your application:

```python
try:
    logger.log_success(...)
    print("Logging successful")
except Exception as e:
    print(f"This will not be reached as exceptions are handled internally: {e}")
```

### Complete Example

```python
import os
import logging
from datetime import datetime, timezone, timedelta
from supabase_logger import SupabaseLogger

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set environment variables (or use a .env file with python-dotenv)
os.environ['SUPABASE_URL'] = 'https://your-supabase-url.supabase.co'
os.environ['SUPABASE_API_KEY'] = 'your-supabase-api-key'
os.environ['SUPABASE_AUTH_EMAIL'] = 'your-auth-email@example.com'
os.environ['SUPABASE_AUTH_PASSWORD'] = 'your-auth-password'
os.environ['ENVIRONMENT'] = 'development'

# Create a logger instance
logger = SupabaseLogger()

# Set channel-specific attributes (optional)
logger.channel_id = "default-channel"
logger.bot_id = "default-bot"
logger.bot_name = "Default Bot"

# Current time for request/response timestamps
request_time = datetime.now(timezone.utc) - timedelta(seconds=1)
response_time = datetime.now(timezone.utc)

# Log a successful bot response
logger.log_success(
    user_id="user123",
    channel_id="channel456",  # This will override the default channel_id
    thread_id="thread789",
    user_message="What's the weather like today?",
    response_text="I'm sorry, I don't have access to real-time weather data.",
    request_time=request_time,
    response_time=response_time,
    bot_id="bot001",
    bot_name="AI Assistant",
    system_prompt="You are a helpful assistant.",
    chat_history_length=5,
    input_attachments={"has_image": False},
    output_attachments={}
)

print("Logging example completed. Check your Supabase database for the log entry.")
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
