"""
Example script demonstrating how to use the supabase-logger package.
"""

import os
import logging
from datetime import datetime, timezone, timedelta

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Import the SupabaseLogger class
from supabase_logger import SupabaseLogger

def main():
    """Main function demonstrating the use of SupabaseLogger."""
    
    # Set environment variables (in a real application, these would be set in the environment)
    # os.environ['SUPABASE_URL'] = 'https://your-supabase-url.supabase.co'
    # os.environ['SUPABASE_API_KEY'] = 'your-supabase-api-key'
    # os.environ['SUPABASE_AUTH_EMAIL'] = 'your-auth-email@example.com'
    # os.environ['SUPABASE_AUTH_PASSWORD'] = 'your-auth-password'
    # os.environ['ENVIRONMENT'] = 'development'
    
    # Create a logger instance
    logger = SupabaseLogger()
    
    # Current time for request/response timestamps
    request_time = datetime.now(timezone.utc) - timedelta(seconds=1)
    response_time = datetime.now(timezone.utc)
    
    # Log a successful bot response
    logger.log_success(
        user_id="user123",
        channel_id="channel456",
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

if __name__ == "__main__":
    main()
