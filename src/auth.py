"""
Strava OAuth Authentication Handler
===================================

This module handles the secure OAuth 2.0 authentication process with Strava.

What this file does:
1. Generates the authorization URL for you to log in to Strava.
2. Exchanges the authorization code for access and refresh tokens.
3. Automatically refreshes the access token when it expires.
4. Securely saves and loads tokens from a local JSON file (cache/strava_token.json).

Usage:
    Run this file directly to start the initial authentication flow:
    python -m src.auth
"""

import requests
import webbrowser
from urllib.parse import urlencode
import time
from pathlib import Path
import json
from .config import (
    STRAVA_CLIENT_ID,
    STRAVA_CLIENT_SECRET,
    STRAVA_AUTH_URL,
    STRAVA_TOKEN_URL,
    REDIRECT_URI,
    SCOPE,
    CACHE_DIR
)

class StravaAuth:
    """Handle Strava OAuth 2.0 authentication flow"""

    def __init__(self):
        self.client_id = STRAVA_CLIENT_ID
        self.client_secret = STRAVA_CLIENT_SECRET
        self.token_file = CACHE_DIR / 'strava_token.json'
        self.access_token = None
        self.refresh_token = None
        self.expires_at = None

    def get_authorization_url(self):
        """Generate the authorization URL for user to grant access"""
        params = {
            'client_id': self.client_id,
            'redirect_uri': REDIRECT_URI,
            'response_type': 'code',
            'scope': SCOPE,
            'approval_prompt': 'auto'
        }
        return f"{STRAVA_AUTH_URL}?{urlencode(params)}"

    def exchange_code_for_token(self, authorization_code):
        """Exchange authorization code for access token"""
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': authorization_code,
            'grant_type': 'authorization_code'
        }

        response = requests.post(STRAVA_TOKEN_URL, data=payload)
        response.raise_for_status()

        token_data = response.json()
        self._save_token(token_data)
        return token_data

    def refresh_access_token(self, refresh_token=None):
        """Refresh the access token using refresh token"""
        if refresh_token is None:
            refresh_token = self.refresh_token

        if not refresh_token:
            raise ValueError("No refresh token available. Please re-authenticate.")

        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }

        response = requests.post(STRAVA_TOKEN_URL, data=payload)
        response.raise_for_status()

        token_data = response.json()
        self._save_token(token_data)
        return token_data

    def _save_token(self, token_data):
        """Save token data to file"""
        self.access_token = token_data['access_token']
        self.refresh_token = token_data['refresh_token']
        self.expires_at = token_data['expires_at']

        with open(self.token_file, 'w') as f:
            json.dump(token_data, f, indent=2)

        print(f"Token saved to {self.token_file}")

    def load_token(self):
        """Load token from file if it exists"""
        if not self.token_file.exists():
            return None

        with open(self.token_file, 'r') as f:
            token_data = json.load(f)

        self.access_token = token_data['access_token']
        self.refresh_token = token_data['refresh_token']
        self.expires_at = token_data['expires_at']

        return token_data

    def is_token_valid(self):
        """Check if current token is still valid"""
        if not self.expires_at:
            return False
        return time.time() < self.expires_at

    def get_valid_token(self):
        """Get a valid access token, refreshing if necessary"""
        # Try to load existing token
        self.load_token()

        # Check if token is valid
        if self.is_token_valid():
            return self.access_token

        # Token expired or doesn't exist, need to refresh
        if self.refresh_token:
            print("Token expired, refreshing...")
            token_data = self.refresh_access_token()
            return token_data['access_token']

        # No valid token, need full authentication
        raise ValueError(
            "No valid token found. Please run the authentication flow first. "
            "Use: python -m src.auth"
        )

    def authenticate(self):
        """Start the OAuth authentication flow"""
        auth_url = self.get_authorization_url()

        print("\n=== Strava Authentication ===")
        print("\nOpening browser for authentication...")
        print("If the browser doesn't open, visit this URL manually:")
        print(f"\n{auth_url}\n")

        webbrowser.open(auth_url)

        print("After authorizing, you'll be redirected to a URL like:")
        print("http://localhost:8501/?state=&code=XXXXX&scope=read,activity:read_all")
        print("\nCopy the ENTIRE URL and paste it here:")

        redirect_response = input("\nPaste the redirect URL: ").strip()

        # Extract authorization code from URL
        if 'code=' in redirect_response:
            code = redirect_response.split('code=')[1].split('&')[0]
            print(f"\nAuthorization code received: {code[:10]}...")

            # Exchange code for token
            print("Exchanging code for access token...")
            token_data = self.exchange_code_for_token(code)

            print("\nAuthentication successful!")
            print(f"Access token expires at: {time.ctime(token_data['expires_at'])}")
            return token_data
        else:
            raise ValueError("Invalid redirect URL. No authorization code found.")


if __name__ == "__main__":
    # Command-line authentication script
    auth = StravaAuth()
    try:
        token_data = auth.authenticate()
        print("\nYou can now use the Strava API!")
        print(f"Athlete: {token_data.get('athlete', {}).get('firstname', 'Unknown')}")
    except Exception as e:
        print(f"\nError during authentication: {e}")
