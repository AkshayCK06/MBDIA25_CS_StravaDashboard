# Strava Dashboard Setup Guide

## Week 1 Setup - Getting Started

### Step 1: Install Dependencies

Using `uv` (recommended):
```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

Or using pip:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install streamlit pandas plotly requests folium python-dotenv stravalib
```

### Step 2: Register Your Strava Application

1. Go to https://www.strava.com/settings/api
2. Create a new application with these settings:
   - **Application Name**: "My Strava Dashboard" (or your choice)
   - **Category**: Choose appropriate category
   - **Club**: Leave blank
   - **Website**: http://localhost:8501
   - **Authorization Callback Domain**: localhost
3. After creation, note down:
   - **Client ID**
   - **Client Secret**

### Step 3: Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your credentials:
```
STRAVA_CLIENT_ID=your_actual_client_id
STRAVA_CLIENT_SECRET=your_actual_client_secret
```

### Step 4: Authenticate with Strava

Run the authentication script:
```bash
python auth.py
```

This will:
1. Open your browser to Strava authorization page
2. Ask you to authorize the application
3. Redirect you to a URL with an authorization code
4. Paste that URL back into the terminal
5. Exchange the code for access tokens
6. Save tokens to `cache/strava_token.json`

### Step 5: Test API Connection

Test that everything works:
```bash
python strava_api.py
```

This should display your athlete info and recent activities.

### Step 6: Fetch and Cache Your Data

Fetch all your activities:
```bash
python data_manager.py
```

This will:
- Fetch all activities from Strava API
- Save them to `data/activities.json` (raw data)
- Save them to `data/activities.csv` (tabular format)
- Save athlete info to `data/athlete_info.json`

### Step 7: Test Data Processing

Process and analyze the data:
```bash
python data_processing.py
```

This will display:
- Summary statistics
- Stats by activity type
- Personal records

## Project Structure

```
MBDIA25_CS_StravaDashboard/
├── .env                    # Your API credentials (DO NOT COMMIT)
├── .env.example           # Template for environment variables
├── .gitignore            # Git ignore file
├── pyproject.toml        # Project dependencies
├── config.py             # Configuration management
├── auth.py               # OAuth authentication
├── strava_api.py         # Strava API wrapper
├── data_manager.py       # Data fetching and caching
├── data_processing.py    # Data analysis with Pandas
├── data/                 # Cached activity data (gitignored)
│   ├── activities.json
│   ├── activities.csv
│   └── athlete_info.json
└── cache/                # OAuth tokens (gitignored)
    └── strava_token.json
```

## Troubleshooting

### "Missing Strava API credentials"
- Make sure you created `.env` file (not `.env.example`)
- Verify you copied the correct Client ID and Secret from Strava

### "No valid token found"
- Run `python auth.py` to authenticate first
- Check that `cache/strava_token.json` exists

### "Token expired"
- The script will automatically refresh expired tokens
- If it fails, delete `cache/strava_token.json` and re-authenticate

### Rate Limits
- Strava API has rate limits (100 requests per 15 minutes, 1000 per day)
- Use cached data during development to avoid hitting limits
- The data_manager uses local cache to reduce API calls

## Next Steps (Week 2)

Once you have data cached locally, you can:
1. Build the Streamlit dashboard UI
2. Add visualizations with Plotly
3. Implement interactive filtering
4. Add map visualizations with Folium

## Useful Commands

```bash
# Re-authenticate
python auth.py

# Refresh data from API
python -c "from data_manager import DataManager; DataManager().fetch_and_cache_activities(force_refresh=True)"

# Check what's cached
python -c "from data_manager import DataManager; print(DataManager().get_cache_info())"

# Test configuration
python config.py
```

## Division of Work

### Backend Developer (Person A)
- ✅ OAuth authentication (`auth.py`)
- ✅ API integration (`strava_api.py`)
- ✅ Data caching (`data_manager.py`)
- ✅ Data processing (`data_processing.py`)

### Frontend Developer (Person B)
- 🔜 Streamlit dashboard layout (Week 2)
- 🔜 Plotly visualizations (Week 2)
- 🔜 Map integration (Week 2)
- 🔜 UI/UX polish (Week 3)

### Shared Tasks
- ✅ Project setup and configuration
- 🔜 Testing and debugging
- 🔜 Documentation
- 🔜 Final presentation
