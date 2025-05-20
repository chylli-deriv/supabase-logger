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
