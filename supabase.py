"""
Supabase Logger Module

This module provides functionality to log successful bot responses to Supabase
using direct API calls instead of the Supabase SDK.
"""

import os
import requests
import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional

from .supabase_client import SupabaseClient

# Get logger
logger = logging.getLogger(__name__)

class SupabaseLogger(SupabaseClient):
    """Logger class for sending successful bot responses to Supabase
    
    This class implements the Singleton pattern to ensure only one instance
    exists throughout the application lifecycle.
    """
    
    # Singleton instance
    _instance = None
    
    def __new__(cls):
        """Ensure only one instance of SupabaseLogger exists"""
        if cls._instance is None:
            # Create a new instance if one doesn't exist yet
            cls._instance = super(SupabaseLogger, cls).__new__(cls)
            # Set _initialized flag to False for the new instance
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize Supabase logger with context information
        
        This method will only perform initialization once for the singleton instance,
        even if called multiple times.
        """
        # Only initialize once to avoid re-establishing connections
        if not getattr(self, '_initialized', False):
            # Initialize the base class with Supabase logger specific environment variables
            super().__init__(
                url=os.environ.get('SUPABASE_URL'),
                api_key=os.environ.get('SUPABASE_API_KEY'),
                auth_email=os.environ.get('SUPABASE_AUTH_EMAIL'),
                auth_password=os.environ.get('SUPABASE_AUTH_PASSWORD'),
                environment=os.environ.get('ENVIRONMENT')
            )
            
            # Set instance-specific attributes
            self.user_id = None
            self.channel_id = None
            self.thread_id = None
            self.bot_id = None
            self.bot_name = None
            self.enabled = True  # By default, logging is enabled
            
            # Mark as initialized to prevent re-initialization
            self._initialized = True

    def log_success(self, 
                   user_id: str,
                   channel_id: str,
                   thread_id: str,
                   user_message: str,
                   response_text: str,
                   request_time: datetime,
                   response_time: datetime,
                   bot_id: str,
                   bot_name: str,
                   system_prompt: str,
                   input_attachments: Optional[Dict] = None,
                   chat_history_length: Optional[int] = None,
                   output_attachments: Optional[Dict] = None) -> None:
        """Log successful bot response to Supabase
        
        Args:
            user_id: ID of the user who sent the message
            channel_id: ID of the channel where the message was sent
            thread_id: ID of the thread if message was in thread
            user_message: Original message from user
            response_text: Bot's response text
            request_time: When the request was received
            response_time: When the response was sent
            bot_id: Bot's unique identifier
            bot_name: Type/name of the bot
            system_prompt: System prompt used
            input_attachments: Any attachments in user's message
            chat_history_length: Length of chat history
            output_attachments: Any attachments in bot's response
        """
        # Prepare log entry
        log_entry = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "request_timestamp": request_time.isoformat(),
            "response_timestamp": response_time.isoformat(),
            "ai_bot_id": bot_id,
            "user_id": user_id,
            "channel_id": channel_id,
            "thread_id": thread_id,
            "user_message": user_message,
            "input_attachments": input_attachments or {},
            "system_prompt": system_prompt,
            "chat_history_length": chat_history_length or 0,
            "response_text": response_text,
            "duration": (response_time - request_time).total_seconds(),
            "output_attachments": output_attachments or {},
            "environment": self.environment
        }
        
        # Log the entry for debugging - do this before any checks so we always see what would be logged
        logger.debug(f"Supabase log entry: {log_entry}")
        
        # Check if Supabase URL is configured
        if not self.url:
            logger.info("Supabase logging is disabled (SUPABASE_URL not set)")
            return
            
        # Check if logging is enabled for this instance
        if not self.enabled:
            logger.info(f"Supabase logging is disabled for channel: {self.channel_id}")
            return

        try:
            # Try to insert log entry
            self._insert_log(log_entry)
            
        except Exception as e:
            # If first attempt fails, try to get a new valid token once
            logger.info("Log insert failed, attempting to get new token")
            try:
                # Force new token
                self.access_token = None
                self._insert_log(log_entry)
                
            except Exception as e:
                # Log error but don't raise - we don't want logging failures to affect the bot
                logger.error(f"Failed to log to Supabase after token refresh: {str(e)}")
                logger.debug("Failed log entry: %s", log_entry)

    def _insert_log(self, log_entry: Dict[str, Any]) -> None:
        """Insert a log entry into Supabase
        
        Args:
            log_entry: The log entry to insert
        """
        # Get valid token
        token = self._get_valid_token()
            
        # Log the request details
        logger.debug(f"Sending log to Supabase URL: {self.url}/rest/v1/ai_bot_logs")
        
        response = requests.post(
            f"{self.url}/rest/v1/ai_bot_logs",
            headers={
                "apikey": self.api_key,
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json=log_entry,
            timeout=30  # Add a 30-second timeout
        )
        
        # Log the response
        logger.debug(f"Supabase response status: {response.status_code}")
        logger.debug(f"Supabase response body: {response.text}")
        
        response.raise_for_status()
        logger.info("Successfully logged bot response to Supabase")
