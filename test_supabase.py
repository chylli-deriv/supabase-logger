"""
Test script for the supabase-logger package.

This script tests the basic functionality of the SupabaseLogger class.
"""

import unittest
import os
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone, timedelta

# Import the classes to test
from supabase_logger import SupabaseLogger, SupabaseClient

class TestSupabaseClient(unittest.TestCase):
    """Test cases for the SupabaseClient class."""
    
    def setUp(self):
        """Set up test environment."""
        # Set test environment variables
        os.environ['SUPABASE_URL'] = 'https://test-url.supabase.co'
        os.environ['SUPABASE_API_KEY'] = 'test-api-key'
        os.environ['SUPABASE_AUTH_EMAIL'] = 'test@example.com'
        os.environ['SUPABASE_AUTH_PASSWORD'] = 'test-password'
        os.environ['ENVIRONMENT'] = 'test'
    
    @patch('requests.post')
    def test_authenticate(self, mock_post):
        """Test authentication process."""
        # Mock the response from Supabase
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'test-access-token',
            'refresh_token': 'test-refresh-token',
            'expires_in': 3600
        }
        mock_post.return_value = mock_response
        
        # Create client and trigger authentication
        client = SupabaseClient()
        token = client._get_valid_token()
        
        # Verify the token is correct
        self.assertEqual(token, 'test-access-token')
        
        # Verify the request was made correctly
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], 'https://test-url.supabase.co/auth/v1/token?grant_type=password')
        self.assertEqual(kwargs['headers']['apikey'], 'test-api-key')
        self.assertEqual(kwargs['json']['email'], 'test@example.com')
        self.assertEqual(kwargs['json']['password'], 'test-password')

class TestSupabaseLogger(unittest.TestCase):
    """Test cases for the SupabaseLogger class."""
    
    def setUp(self):
        """Set up test environment."""
        # Set test environment variables
        os.environ['SUPABASE_URL'] = 'https://test-url.supabase.co'
        os.environ['SUPABASE_API_KEY'] = 'test-api-key'
        os.environ['SUPABASE_AUTH_EMAIL'] = 'test@example.com'
        os.environ['SUPABASE_AUTH_PASSWORD'] = 'test-password'
        os.environ['ENVIRONMENT'] = 'test'
    
    def test_singleton(self):
        """Test that SupabaseLogger implements the Singleton pattern."""
        logger1 = SupabaseLogger()
        logger2 = SupabaseLogger()
        
        # Verify that both instances are the same object
        self.assertIs(logger1, logger2)
    
    @patch('requests.post')
    def test_log_success(self, mock_post):
        """Test logging a successful bot response."""
        # Mock the authentication response
        auth_response = MagicMock()
        auth_response.status_code = 200
        auth_response.json.return_value = {
            'access_token': 'test-access-token',
            'refresh_token': 'test-refresh-token',
            'expires_in': 3600
        }
        
        # Mock the log insertion response
        log_response = MagicMock()
        log_response.status_code = 201
        log_response.text = ''
        
        # Set up the mock to return different responses for different calls
        mock_post.side_effect = [auth_response, log_response]
        
        # Create logger
        logger = SupabaseLogger()
        
        # Test times
        request_time = datetime.now(timezone.utc) - timedelta(seconds=1)
        response_time = datetime.now(timezone.utc)
        
        # Log a successful bot response
        logger.log_success(
            user_id="test-user",
            channel_id="test-channel",
            thread_id="test-thread",
            user_message="test message",
            response_text="test response",
            request_time=request_time,
            response_time=response_time,
            bot_id="test-bot",
            bot_name="Test Bot",
            system_prompt="test prompt"
        )
        
        # Verify the log insertion request was made correctly
        self.assertEqual(mock_post.call_count, 2)  # Auth + Log insertion
        
        # Check the second call (log insertion)
        args, kwargs = mock_post.call_args_list[1]
        self.assertEqual(args[0], 'https://test-url.supabase.co/rest/v1/ai_bot_logs')
        self.assertEqual(kwargs['headers']['apikey'], 'test-api-key')
        self.assertEqual(kwargs['headers']['Authorization'], 'Bearer test-access-token')
        
        # Check the log entry data
        log_entry = kwargs['json']
        self.assertEqual(log_entry['user_id'], 'test-user')
        self.assertEqual(log_entry['channel_id'], 'test-channel')
        self.assertEqual(log_entry['thread_id'], 'test-thread')
        self.assertEqual(log_entry['user_message'], 'test message')
        self.assertEqual(log_entry['response_text'], 'test response')
        self.assertEqual(log_entry['ai_bot_id'], 'test-bot')
        self.assertEqual(log_entry['system_prompt'], 'test prompt')
        self.assertEqual(log_entry['environment'], 'test')

if __name__ == '__main__':
    unittest.main()
