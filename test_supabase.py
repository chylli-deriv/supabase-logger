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
        
        # Reset the singleton instance before each test
        SupabaseLogger._instance = None
    
    def test_singleton(self):
        """Test that SupabaseLogger implements the Singleton pattern."""
        logger1 = SupabaseLogger()
        logger2 = SupabaseLogger()
        
        # Verify that both instances are the same object
        self.assertIs(logger1, logger2)
    
    def test_parameters_precedence(self):
        """Test that constructor parameters take precedence over environment variables."""
        # Create logger with explicit parameters
        logger = SupabaseLogger(
            url='https://param-url.supabase.co',
            api_key='param-api-key',
            auth_email='param@example.com',
            auth_password='param-password',
            environment='param-env'
        )
        
        # Verify that the parameters were used instead of environment variables
        self.assertEqual(logger.url, 'https://param-url.supabase.co')
        self.assertEqual(logger.api_key, 'param-api-key')
        self.assertEqual(logger.auth_email, 'param@example.com')
        self.assertEqual(logger.auth_password, 'param-password')
        self.assertEqual(logger.environment, 'param-env')
    
    def test_partial_parameters(self):
        """Test that constructor can handle partial parameters, falling back to environment variables."""
        # Create logger with only some parameters
        logger = SupabaseLogger(
            url='https://param-url.supabase.co',
            api_key='param-api-key'
            # Other parameters not provided, should fall back to environment variables
        )
        
        # Verify that provided parameters were used
        self.assertEqual(logger.url, 'https://param-url.supabase.co')
        self.assertEqual(logger.api_key, 'param-api-key')
        
        # Verify that missing parameters fell back to environment variables
        self.assertEqual(logger.auth_email, 'test@example.com')
        self.assertEqual(logger.auth_password, 'test-password')
        self.assertEqual(logger.environment, 'test')
        
        # Verify that logging is enabled since all required parameters are set
        self.assertTrue(logger.enabled)
    
    def test_missing_parameters(self):
        """Test that logger disables logging when required parameters are missing."""
        # Clear environment variables
        for var in ['SUPABASE_URL', 'SUPABASE_API_KEY', 'SUPABASE_AUTH_EMAIL', 'SUPABASE_AUTH_PASSWORD']:
            if var in os.environ:
                del os.environ[var]
        
        # Create logger with missing parameters
        logger = SupabaseLogger()
        
        # Verify that logging is disabled
        self.assertFalse(logger.enabled)
        
        # Verify that url, api_key, auth_email, and auth_password are None
        self.assertIsNone(logger.url)
        self.assertIsNone(logger.api_key)
        self.assertIsNone(logger.auth_email)
        self.assertIsNone(logger.auth_password)
    
    @patch('requests.post')
    def test_disabled_logging(self, mock_post):
        """Test that log_success doesn't make API calls when logging is disabled."""
        # Create logger with missing parameters (which will disable logging)
        for var in ['SUPABASE_URL', 'SUPABASE_API_KEY', 'SUPABASE_AUTH_EMAIL', 'SUPABASE_AUTH_PASSWORD']:
            if var in os.environ:
                del os.environ[var]
        
        logger = SupabaseLogger()
        self.assertFalse(logger.enabled)
        
        # Test times
        request_time = datetime.now(timezone.utc) - timedelta(seconds=1)
        response_time = datetime.now(timezone.utc)
        
        # Log a bot response (should not make any API calls)
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
        
        # Verify that no API calls were made
        mock_post.assert_not_called()
    
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
