# Strava Data Dashboard 

**Course:** Computer Science (CS)  
**Program:** Master of Business Development, Innovation and Administration (MBDIA WS25)  
**Institution:** Hochschule Emden/Leer  
**Authors:** Siddhanth Sharma & Akshay CK

---

## 📖 Project Overview

This project is an interactive data dashboard designed to visualize and analyze personal activity data from [Strava](https://www.strava.com/). Built using Python, it leverages the Strava API to fetch athlete activities, processes the data using Pandas, and presents insights through an interactive Jupyter Notebook.

**Goal:** To demonstrate the end-to-end process of consuming a REST API, managing authentication (OAuth 2.0), processing complex datasets, and building a data visualization dashboard.

## ✨ Key Features

- **Secure Authentication:** Implements Strava's OAuth 2.0 flow with automatic token refreshing.
- **Data Management:** 
  - Fetches detailed activity lists and specific streams (GPS, Heart Rate, Elevation).
  - Smart caching system (JSON/CSV) to minimize API usage and rate limiting.
- **Data Analysis:**
  - Automated summary statistics (Total Distance, Elevation Gain, Moving Time).
  - Activity type breakdown (Run, Ride, Swim, etc.).
  - Weekly and monthly aggregations.
  - Identification of personal records.
- **Interactive Dashboard:**
  - Built with **Jupyter Notebook**.
  - **Intelligent Analyst Interface (Smart Commands):** Simple commands to query and visualize data.
  - **Interactive Maps:** Route visualization with Folium.
  - **Smart Trends:** Pace analysis and heatmaps using Plotly.

## 🛠️ Technology Stack

- **Language:** Python 3.9+
- **Data Processing:** Pandas, NumPy
- **API Interaction:** Requests
- **Visualization:** Plotly, Folium
- **Dashboard Framework:** Jupyter Notebook
- **Project Management:** UV (optional), standard pip requirements

## 📂 Project Structure

```
MBDIA25_CS_StravaDashboard/
├── src/                    # Source code package
│   ├── auth.py             # OAuth 2.0 authentication handler
│   ├── config.py           # Configuration and path management
│   ├── data_manager.py     # Data fetching and caching logic
│   ├── data_processing.py  # Pandas analysis and metrics
│   └── strava_api.py       # Strava API wrapper
├── docs/                   # Project documentation & requirements
├── scripts/                # Setup scripts (Mac/Linux/Windows)
├── data/                   # Cached activity data (Local only, ignored by Git)
├── cache/                  # Auth tokens (Local only, ignored by Git)
├── dashboard.ipynb         # Interactive Jupyter Notebook Dashboard
└── requirements.txt        # Python dependencies
```

## 🚀 Quick Start Guide

For a fast setup, refer to [docs/QUICK_START.md](docs/QUICK_START.md).

### 1. Prerequisites
- Python 3.9 or higher installed.
- A Strava account.
- API Credentials (Client ID & Secret) from [Strava API Settings](https://www.strava.com/settings/api).

### 2. Setup
Clone the repository and run the automated setup script for your OS.

**Mac/Linux:**
```bash
./scripts/setup.sh
```

**Windows:**
```bat
scripts\setup.bat
```

### 3. Configuration
Copy the example environment file and add your Strava credentials.
```bash
cp .env.example .env
# Edit .env and paste your STRAVA_CLIENT_ID and STRAVA_CLIENT_SECRET
```

### 4. Running the Project
Always ensure your virtual environment is activated (`source venv/bin/activate` or `venv\Scripts\activate`).

**Step 1: Authenticate**
This will open your browser to authorize the app.
```bash
python -m src.auth
```

**Step 2: Fetch Data**
Downloads your activities and saves them locally.
```bash
python -m src.data_manager
```

**Step 3: Analyze & Visualize**
You can run the analysis and view dashboards in two ways:

*   **Terminal:** View summary statistics in the console.
    ```bash
    python -m src.data_processing
    ```
*   **Jupyter Notebook:** Open the interactive dashboard.
    ```bash
    jupyter notebook dashboard.ipynb
    ```
    *Make sure to select the `Python (venv)` kernel inside the notebook.*

## ❓ Troubleshooting

### "Missing Strava API credentials"
- Ensure you created the `.env` file (not just `.env.example`).
- Verify you copied the correct Client ID and Secret from Strava.

### "No valid token found"
- Run `python -m src.auth` to authenticate first.
- Check that `cache/strava_token.json` exists.

### "Token expired"
- The script will automatically refresh expired tokens.
- If it fails, delete `cache/strava_token.json` and re-authenticate.

### Rate Limits
- Strava API has rate limits (100 requests per 15 minutes, 1000 per day).
- Use cached data during development to avoid hitting limits.
- The `data_manager` uses local cache to reduce API calls.

### "No module named pandas" (or similar in Jupyter Notebook)
- Ensure you have selected the `Python (venv)` kernel in your Jupyter Notebook.

## 👥 Division of Work

### Backend Developer
- ✅ OAuth authentication (`auth.py`)
- ✅ API integration (`strava_api.py`)
- ✅ Data caching (`data_manager.py`)
- ✅ Data processing (`data_processing.py`)

### Frontend Developer
- ✅ Interactive Notebook Dashboard (`dashboard.ipynb`)
- ✅ Advanced Plotly visualizations
- ✅ Map integration with Folium
- ✅ Intelligent Analyst Interface (Smart Commands)

## 📚 Documentation
- [Requirements](docs/reqdoc.md): Functional and technical requirements.
- [Project Log](docs/PROJECT_CONVERSATION.md): Development history and decisions.
- [Smart Commands Guide](docs/SMART_COMMANDS_GUIDE.md): Reference for all available dashboard commands.

## 📄 License
This project is created for educational purposes as part of the MBDIA curriculum.