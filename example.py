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

def example_with_env_vars():
    """Example using environment variables for credentials."""
    
    print("\n=== Example using environment variables ===\n")
    
    # Set environment variables (in a real application, these would be set in the environment)
    # os.environ['SUPABASE_URL'] = 'https://your-supabase-url.supabase.co'
    # os.environ['SUPABASE_API_KEY'] = 'your-supabase-api-key'
    # os.environ['SUPABASE_AUTH_EMAIL'] = 'your-auth-email@example.com'
    # os.environ['SUPABASE_AUTH_PASSWORD'] = 'your-auth-password'
    # os.environ['ENVIRONMENT'] = 'development'
    
    # Create a logger instance (will use environment variables)
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
    
    print("Logging example with environment variables completed.")

def example_with_parameters():
    """Example using direct parameters for credentials."""
    
    print("\n=== Example using direct parameters ===\n")
    
    # Create a logger instance with explicit parameters
    logger = SupabaseLogger(
        url='https://your-supabase-url.supabase.co',
        api_key='your-supabase-api-key',
        auth_email='your-auth-email@example.com',
        auth_password='your-auth-password',
        environment='development'
    )
    
    # Current time for request/response timestamps
    request_time = datetime.now(timezone.utc) - timedelta(seconds=1)
    response_time = datetime.now(timezone.utc)
    
    # Log a successful bot response
    logger.log_success(
        user_id="user456",
        channel_id="channel789",
        thread_id="thread123",
        user_message="Tell me a joke.",
        response_text="Why did the chicken cross the road? To get to the other side!",
        request_time=request_time,
        response_time=response_time,
        bot_id="bot002",
        bot_name="Joke Bot",
        system_prompt="You are a funny assistant that tells jokes.",
        chat_history_length=3,
        input_attachments={},
        output_attachments={}
    )
    
    print("Logging example with direct parameters completed.")

def main():
    """Main function demonstrating the use of SupabaseLogger."""
    
    # Example using environment variables
    example_with_env_vars()
    
    # Example using direct parameters
    example_with_parameters()
    
    print("\nBoth examples completed. Check your Supabase database for the log entries.")

if __name__ == "__main__":
    main()
