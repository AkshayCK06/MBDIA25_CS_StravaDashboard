import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Strava API Configuration
STRAVA_CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
STRAVA_CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
STRAVA_REFRESH_TOKEN = os.getenv('STRAVA_REFRESH_TOKEN')

# API Endpoints
STRAVA_AUTH_URL = "https://www.strava.com/oauth/authorize"
STRAVA_TOKEN_URL = "https://www.strava.com/oauth/token"
STRAVA_API_BASE = "https://www.strava.com/api/v3"

# OAuth Settings
REDIRECT_URI = "http://localhost:8501"
SCOPE = "read,activity:read_all"

# Data Directories
BASE_DIR = Path(__file__).parent
DATA_DIR = Path(os.getenv('DATA_DIR', BASE_DIR / 'data'))
CACHE_DIR = Path(os.getenv('CACHE_DIR', BASE_DIR / 'cache'))

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)

# Validate required credentials
def validate_credentials():
    if not STRAVA_CLIENT_ID or not STRAVA_CLIENT_SECRET:
        raise ValueError(
            "Missing Strava API credentials. "
            "Please set STRAVA_CLIENT_ID and STRAVA_CLIENT_SECRET in .env file. "
            "Get them from: https://www.strava.com/settings/api"
        )

if __name__ == "__main__":
    validate_credentials()
    print("Configuration loaded successfully!")
    print(f"Data directory: {DATA_DIR}")
    print(f"Cache directory: {CACHE_DIR}")
