"""
Supabase Client Module

This module provides a base class for Supabase authentication and token management.
It is used by both the SupabaseLogger and the word frequency analyzer.
"""

import os
import requests
import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional

# Get logger
logger = logging.getLogger(__name__)

class SupabaseClient:
    """Base class for Supabase authentication and token management"""
    
    def __init__(self, url=None, api_key=None, auth_email=None, auth_password=None, environment=None):
        """
        Initialize Supabase client
        
        Args:
            url: Supabase URL
            api_key: Supabase API key
            auth_email: Supabase auth email
            auth_password: Supabase auth password
            environment: Environment name
        """
        # Instance attributes for token management
        self.access_token = None
        self.refresh_token = None
        self.expires_at = None
        
        # Set configuration from parameters or environment variables
        self.url = url or os.environ.get('SUPABASE_URL')
        self.api_key = api_key or os.environ.get('SUPABASE_API_KEY')
        self.auth_email = auth_email or os.environ.get('SUPABASE_AUTH_EMAIL')
        self.auth_password = auth_password or os.environ.get('SUPABASE_AUTH_PASSWORD')
        self.environment = environment or os.environ.get('ENVIRONMENT')
        
        # Log configuration status (without sensitive details)
        if self.url and self.api_key and self.auth_email and self.auth_password:
            logger.info("Supabase configuration loaded successfully")
        else:
            missing = []
            if not self.url: missing.append("URL")
            if not self.api_key: missing.append("API Key")
            if not self.auth_email: missing.append("Auth Email")
            if not self.auth_password: missing.append("Auth Password")
            
            if not self.url:
                logger.info("Supabase is disabled (URL not set)")
            else:
                logger.warning(f"Supabase configuration incomplete. Missing: {', '.join(missing)}")

    def _get_valid_token(self) -> str:
        """Get a valid access token, refreshing if needed

        Returns:
            str: Valid access token
        """
        # If no token exists, authenticate
        if not self.access_token:
            self._authenticate()
            return self.access_token

        # If token is expired and we have refresh token, try refresh
        current_time = int(datetime.now(timezone.utc).timestamp())
        if self.expires_at and current_time >= self.expires_at and self.refresh_token:
            try:
                self._refresh_token()
                return self.access_token
            except Exception as e:
                logger.warning(f"Token refresh failed, falling back to full auth: {str(e)}")
                self._authenticate()
                return self.access_token

        # If token is expired but no refresh token, authenticate
        if self.expires_at and current_time >= self.expires_at:
            self._authenticate()
            return self.access_token

        return self.access_token

    def _refresh_token(self) -> None:
        """Refresh access token using refresh token"""
        response = None
        try:
            response = requests.post(
                f"{self.url}/auth/v1/token?grant_type=refresh_token",
                headers={
                    "apikey": self.api_key,
                    "Content-Type": "application/json"
                },
                json={
                    "refresh_token": self.refresh_token
                },
                timeout=30  # Add a 30-second timeout
            )
            response.raise_for_status()
            
            data = response.json()
            self.access_token = data["access_token"]
            self.refresh_token = data["refresh_token"]
            self.expires_at = int(datetime.now(timezone.utc).timestamp()) + data.get("expires_in", 3600)
            logger.info("Successfully refreshed Supabase token")
            
        except Exception as e:
            logger.error(f"Supabase token refresh failed: {str(e)}")
            if hasattr(response, 'text'):
                logger.debug(f"Refresh response: {response.text}")
            raise

    def _authenticate(self) -> None:
        """Authenticate with Supabase using email/password"""
        response = None
        try:
            response = requests.post(
                f"{self.url}/auth/v1/token?grant_type=password",
                headers={
                    "apikey": self.api_key,
                    "Content-Type": "application/json"
                },
                json={
                    "email": self.auth_email,
                    "password": self.auth_password
                },
                timeout=30  # Add a 30-second timeout
            )
            response.raise_for_status()
            
            data = response.json()
            self.access_token = data["access_token"]
            self.refresh_token = data["refresh_token"]
            self.expires_at = int(datetime.now(timezone.utc).timestamp()) + data.get("expires_in", 3600)
            logger.info("Successfully authenticated with Supabase")
            
        except Exception as e:
            logger.error(f"Supabase authentication failed: {str(e)}")
            if hasattr(response, 'text'):
                logger.debug(f"Auth response: {response.text}")
            raise
    
    def get_headers(self) -> Dict[str, str]:
        """Get headers for Supabase API requests
        
        Returns:
            Dict[str, str]: Headers for Supabase API requests
        """
        # Get valid token
        token = self._get_valid_token()
        
        return {
            'apikey': self.api_key,
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'Prefer': 'return=minimal'
        }
