# Strava Dashboard Project - Setup Conversation Log

**Date**: December 5, 2024
**Participants**: Akshay & Siddhanth
**Project**: MBDIA25 CS - Strava Dashboard

---

## Initial Discussion

### Akshay's Question:
"Hi, I am working on this project. Can you give me recommendations on how to proceed further with my friend Siddhanth?"

### Project Context:
- **Goal**: Build an interactive Strava data dashboard using Python
- **Tech Stack**: Python, Streamlit, Pandas, Plotly, Folium
- **Scope**: OAuth authentication, fetch activity data, process with Pandas, visualize in web dashboard
- **Current Status**: Requirements document created, no implementation yet

---

## Recommendations Provided

### Project Status Analysis:
- Solid requirements document exists ([reqdoc.md](reqdoc.md))
- No implementation yet - still in planning phase
- Meeting notes show key decisions needed

### Week 1-4 Roadmap:

#### **Week 1: Foundation (Backend Focus)**
1. Set up Python virtual environment with `uv`
2. Implement Strava OAuth 2.0 authentication
3. Create API integration for data fetching
4. Implement data caching (JSON/CSV)
5. Build basic Pandas data processing

#### **Week 2: Basic Dashboard**
1. Create Streamlit app skeleton
2. Display global statistics
3. Show activity list in table
4. Basic filtering by sport type

#### **Week 3: Visualizations**
1. Add Plotly charts (elevation, speed, heart rate)
2. Time-series trend analysis
3. Interactive map visualization with routes
4. Detailed individual activity view

#### **Week 4: Polish & Presentation**
1. UI/UX improvements
2. Final testing
3. Documentation
4. Presentation preparation

### Key Decisions Made:
- **Individual vs Cumulative Data**: Implement BOTH (start with cumulative for MVP)
- **Local vs Online Dashboard**: Start LOCAL with Streamlit (faster development)
- **Division of Work**:
  - Person A: Backend (API, data processing, caching)
  - Person B: Frontend (Streamlit UI, visualizations, maps)
  - Together: OAuth setup, integration, presentation

---

## Week 1 Implementation Request

### Akshay's Request:
"Let's start with week 1 stuff, generate and write the code which is required in this directory"

### What Was Implemented:

#### 1. **Project Configuration Files**
- `.gitignore` - Protect sensitive data and cache files
- `pyproject.toml` - Modern Python project config for uv
- `requirements.txt` - Traditional pip dependencies
- `.env.example` - Template for API credentials
- `config.py` - Centralized configuration management

#### 2. **Authentication Module** ([auth.py](auth.py))
- Full OAuth 2.0 flow implementation
- Automatic token refresh
- Secure token storage in `cache/strava_token.json`
- Browser-based authorization
- Token expiration handling

#### 3. **Strava API Wrapper** ([strava_api.py](strava_api.py))
- Get athlete information
- Fetch all activities (with pagination)
- Get detailed activity data
- Get activity streams (GPS, heart rate, cadence, etc.)
- Activity zones
- Built-in error handling

#### 4. **Data Management** ([data_manager.py](data_manager.py))
- Fetch activities from API
- Cache to JSON (raw data)
- Cache to CSV (tabular format)
- Load cached data
- Convert to Pandas DataFrames
- Fetch individual activity streams
- Cache management utilities

#### 5. **Data Processing** ([data_processing.py](data_processing.py))
- ActivityProcessor class with Pandas
- Summary statistics calculation
- Activity type breakdown
- Weekly/monthly aggregates
- Personal records tracking
- Day-of-week analysis
- Date range filtering
- Computed metrics (pace, speed conversions, etc.)

#### 6. **Documentation**
- `setup_guide.md` - Detailed setup instructions
- `QUICK_START.md` - Simplified quick start guide
- `setup.sh` - Automated Mac/Linux setup script
- `setup.bat` - Automated Windows setup script

---

## Virtual Environment Setup Request

### Akshay's Request:
"I will run the setup and auth, fetching data and everything. Please guide me through it. Also I need you to implement everything in a python virtual environment because we both need to run the code without any external setup or any hassles."

### Additional Context:
- Both Akshay and Siddhanth are using MacBook Air
- Need isolated, self-contained environment
- No external dependencies or hassle

### Solution Implemented:

#### **Automated Setup Scripts**
Created `setup.sh` for Mac that:
1. Checks Python 3 installation
2. Creates virtual environment in `venv/` folder
3. Activates virtual environment
4. Upgrades pip
5. Installs all dependencies from `requirements.txt`
6. Shows next steps

Also created `setup.bat` for Windows (for portability).

#### **Quick Start Guide**
Created comprehensive `QUICK_START.md` with:
- 5-step setup process
- Screenshots/instructions for Strava API registration
- Troubleshooting section
- Commands reference
- Instructions for Siddhanth to set up on his MacBook Air

---

## Step-by-Step Setup Guide Provided

### **STEP 1: Virtual Environment Setup**
```bash
cd /Users/akshayckashyap/Documents/GitHub/MBDIA25_CS_StravaDashboard
./setup.sh
source venv/bin/activate
```

### **STEP 2: Strava API Registration**
1. Go to https://www.strava.com/settings/api
2. Create app with:
   - Name: "My Strava Dashboard"
   - Website: http://localhost:8501
   - Callback: localhost
3. Copy Client ID and Client Secret

### **STEP 3: Configure Credentials**
```bash
cp .env.example .env
nano .env  # Edit with your credentials
```

### **STEP 4: Authenticate**
```bash
python auth.py
```
- Browser opens
- Authorize app
- Copy redirect URL
- Paste in terminal

### **STEP 5: Fetch Data**
```bash
python data_manager.py
```

---

## For Siddhanth: How to Set Up on Your MacBook Air

### Prerequisites:
- Python 3.9+ installed on your Mac
- Strava account with some activities
- Git (to clone the repo)

### Setup Steps:

1. **Clone or Get the Repository**
   ```bash
   cd ~/Documents/GitHub
   git clone <repository-url>
   cd MBDIA25_CS_StravaDashboard
   ```

2. **Run Automated Setup**
   ```bash
   ./setup.sh
   ```
   This creates the virtual environment and installs everything.

3. **Activate Virtual Environment**
   ```bash
   source venv/bin/activate
   ```
   You should see `(venv)` in your terminal prompt.

4. **Get Credentials from Akshay**
   - Ask Akshay to share the `.env` file (contains Client ID and Secret)
   - Place it in the project root directory

   OR register your own app on Strava and create your own `.env` file.

5. **Authenticate with YOUR Strava Account**
   ```bash
   python auth.py
   ```
   - Each person needs to authenticate with their own Strava account
   - This generates YOUR personal access token

6. **Fetch YOUR Data**
   ```bash
   python data_manager.py
   ```
   This downloads all YOUR activities from Strava.

7. **Test Everything**
   ```bash
   python data_processing.py
   ```
   Should show your statistics and personal records.

### Important Notes:
- The `.env` file (API credentials) can be shared between you and Akshay
- The `cache/strava_token.json` file is PERSONAL - each person gets their own
- The `data/` folder is PERSONAL - contains your own activities
- Both of you can work on the same codebase but with your own data

---

## Project Structure Created

```
MBDIA25_CS_StravaDashboard/
├── README.md                 # Project description
├── reqdoc.md                # Official requirements
├── QUICK_START.md           # Quick setup guide
├── setup_guide.md           # Detailed setup guide
├── PROJECT_CONVERSATION.md  # This file
├── 23.10.25_Meeting.md      # Meeting notes
│
├── setup.sh                 # Mac/Linux setup script
├── setup.bat                # Windows setup script
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Project configuration
├── .gitignore              # Git ignore rules
├── .env.example            # Credential template
├── .env                    # Your credentials (NOT in git)
│
├── config.py               # Configuration manager
├── auth.py                 # OAuth authentication
├── strava_api.py           # API wrapper
├── data_manager.py         # Data fetching & caching
├── data_processing.py      # Pandas analysis
│
├── venv/                   # Virtual environment (NOT in git)
├── data/                   # Cached activities (NOT in git)
│   ├── activities.json
│   ├── activities.csv
│   └── athlete_info.json
└── cache/                  # OAuth tokens (NOT in git)
    └── strava_token.json
```

---

## Files to Share vs Keep Private

### ✅ **SHARE with Siddhanth** (via Git):
- All Python code files (.py)
- Documentation (.md files)
- Setup scripts (.sh, .bat)
- requirements.txt
- pyproject.toml
- .env.example (template)
- .gitignore

### ⚠️ **SHARE Securely** (NOT via Git):
- `.env` file (contains API credentials)
  - Send via secure message/email
  - OR Siddhanth can register his own Strava app

### ❌ **NEVER SHARE** (Personal):
- `cache/strava_token.json` (your personal access token)
- `data/` folder (your personal activities)
- `venv/` folder (virtual environment - each person creates their own)

---

## What Each Module Does

### **config.py**
- Loads environment variables from `.env`
- Defines API endpoints
- Creates data directories
- Validates credentials

### **auth.py**
- Handles OAuth 2.0 flow
- Opens browser for authorization
- Exchanges code for tokens
- Refreshes expired tokens
- Saves tokens securely

### **strava_api.py**
- Wraps Strava API v3
- Handles authentication headers
- Fetches athlete info
- Gets activities (with pagination)
- Gets detailed activity streams
- Error handling

### **data_manager.py**
- Orchestrates data fetching
- Caches to JSON and CSV
- Loads cached data
- Converts to Pandas DataFrames
- Manages activity streams
- Cache info utilities

### **data_processing.py**
- ActivityProcessor class
- Computes derived metrics
- Summary statistics
- Group by activity type
- Weekly/monthly aggregates
- Personal records
- Filtering utilities

---

## Next Steps (After Week 1 Setup)

### Week 2: Build Streamlit Dashboard
1. Create `app.py` - main Streamlit application
2. Layout: sidebar for filters, main area for content
3. Display global statistics (total distance, activities, elevation)
4. Show activities table with sorting/filtering
5. Basic activity selection

### Week 2: Add Visualizations
1. Install additional libraries if needed
2. Create Plotly charts:
   - Distance over time (line chart)
   - Activities by type (pie/bar chart)
   - Weekly distance (bar chart)
3. Add interactivity to charts

### Week 3: Individual Activity Details
1. Create activity detail page
2. Plot elevation profile
3. Plot speed/heart rate vs distance
4. Add map visualization with Folium
5. Show route on interactive map

### Week 3: Advanced Features
1. Date range picker
2. Activity type filter
3. Comparison views
4. Export functionality
5. UI improvements

### Week 4: Final Polish
1. Error handling
2. Loading states
3. Documentation
4. User guide
5. Presentation slides

---

## Division of Labor Recommendation

### Akshay (Backend Complete ✅):
- ✅ Project setup
- ✅ Virtual environment
- ✅ OAuth implementation
- ✅ API wrapper
- ✅ Data caching
- ✅ Data processing

### Siddhanth (Frontend - Week 2+):
- 🔜 Streamlit app structure
- 🔜 Layout and navigation
- 🔜 Plotly visualizations
- 🔜 Map integration
- 🔜 UI/UX design

### Together:
- 🔜 Integration testing
- 🔜 Bug fixes
- 🔜 Documentation
- 🔜 Presentation

---

## Troubleshooting Guide

### Issue: "Command not found: python"
**Solution**: Use `python3` instead
```bash
python3 auth.py
```

### Issue: "No module named 'requests'"
**Solution**: Activate virtual environment
```bash
source venv/bin/activate
pip list  # Check installed packages
```

### Issue: "Missing Strava API credentials"
**Solution**: Check .env file
```bash
cat .env  # Verify file exists and has correct values
python config.py  # Test configuration
```

### Issue: "Invalid redirect URL"
**Solution**: Make sure you copy the ENTIRE URL
- Should start with: `http://localhost:8501/?state=&code=`
- Include everything after that

### Issue: Token expired
**Solution**: Tokens auto-refresh, but if it fails:
```bash
rm cache/strava_token.json
python auth.py  # Re-authenticate
```

### Issue: Rate limit exceeded
**Solution**: Strava limits API calls
- 100 requests per 15 minutes
- 1000 requests per day
- Use cached data during development
- Wait and try again later

---

## Useful Commands Reference

```bash
# Activate virtual environment
source venv/bin/activate

# Deactivate virtual environment
deactivate

# Install/update dependencies
pip install -r requirements.txt

# Re-authenticate with Strava
python auth.py

# Fetch new data (force refresh)
python -c "from data_manager import DataManager; DataManager().fetch_and_cache_activities(force_refresh=True)"

# Check what's cached
python -c "from data_manager import DataManager; print(DataManager().get_cache_info())"

# Test configuration
python config.py

# Test API connection
python strava_api.py

# View statistics
python data_processing.py

# Check installed packages
pip list

# Check Python version
python --version
```

---

## Important Reminders

1. **Always activate virtual environment** before running any Python scripts
   ```bash
   source venv/bin/activate
   ```

2. **Never commit sensitive files**:
   - `.env` (has API credentials)
   - `cache/` (has access tokens)
   - `data/` (has personal activity data)
   - `venv/` (virtual environment)

3. **Each person authenticates individually**:
   - API credentials (.env) can be shared
   - But each person runs `python auth.py` with their own Strava account

4. **Use cached data during development**:
   - Avoids hitting API rate limits
   - Faster testing
   - Consistent data

5. **Virtual environment must be active**:
   - Look for `(venv)` in terminal prompt
   - If missing, run: `source venv/bin/activate`

---

## Questions for Consideration

1. **Data Privacy**: Will you show personal data in presentation?
2. **Data Range**: Fetch all activities or limit to recent (e.g., last year)?
3. **Activity Types**: Focus on specific sports or show all?
4. **Visualizations**: What charts are most important to you?
5. **Deployment**: Keep local or deploy online later?

---

## Resources

### Strava API Documentation:
- Main API: https://developers.strava.com/docs/reference/
- Getting Started: https://developers.strava.com/docs/getting-started/
- Authentication: https://developers.strava.com/docs/authentication/

### Python Libraries:
- Streamlit: https://docs.streamlit.io/
- Pandas: https://pandas.pydata.org/docs/
- Plotly: https://plotly.com/python/
- Folium: https://python-visualization.github.io/folium/

### Tools:
- UV (Package Manager): https://github.com/astral-sh/uv
- Git: https://git-scm.com/doc

---

## Summary

**What's Been Done (Week 1 - COMPLETE ✅)**:
- Project structure created
- Virtual environment setup automated
- OAuth 2.0 authentication implemented
- Strava API wrapper built
- Data fetching and caching working
- Pandas data processing complete
- Comprehensive documentation written
- Setup scripts for easy installation

**Current Status**:
- Backend foundation is 100% complete
- Ready to fetch data from Strava
- Ready for Siddhanth to clone and set up
- Ready to start Week 2 (Streamlit dashboard)

**Next Immediate Actions**:
1. Akshay: Run setup, authenticate, fetch data
2. Siddhanth: Clone repo, run setup on his MacBook Air
3. Both: Review the fetched data and plan Week 2 dashboard
4. Start building Streamlit UI

---

**Good luck with your project! 🚀**

---

*This conversation log was created on December 5, 2024, to help Siddhanth understand the complete context and setup process for the Strava Dashboard project.*
