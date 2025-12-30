# Strava Data Dashboard 

**Course:** Computer Science (CS)  
**Program:** Master of Business Development, Innovation and Administration (MBDIA WS25)  
**Institution:** Hochschule Emden/Leer  
**Authors:** Siddhanth Sharma & Akshay CK

---

## 📖 Project Overview

This project is an interactive data dashboard designed to visualize and analyze personal activity data from [Strava](https://www.strava.com/). Built using Python, it leverages the Strava API to fetch athlete activities, processes the data using Pandas, and presents insights through an interactive Jupyter Notebook.

**Goal:** To provide a powerful, private, and user-friendly interface for athletes to "talk" to their data using simple commands and local AI.

## ✨ Key Features

- **Secure, In-Notebook Authentication:** A simplified OAuth 2.0 flow that runs entirely within the Jupyter Notebook.
- **Smart Command Interface:**
  - `strava.refresh()`: Pull the latest data from the Strava API.
  - `strava.show("summary")`: Get a high-level overview of all activities.
  - `strava.compare("month")`: Compare performance (Avg/Max/Min Speed) for Rides and Walks against the previous month.
  - `strava.plot("trend")`: View your performance trends over time (defaults to Speed in km/h).
  - `strava.plot("heatmap")`: A monthly bar chart showing daily activity (e.g., distance or steps).
  - `strava.details(index)`: Get detailed stats for a specific activity.
- **AI Integration (Ollama):** Local LLM support (`strava.ask(...)`) to answer natural language questions about your data, ensuring 100% privacy.
- **Enriched Data Metrics:**
  - Automatic calculation of **Speed (km/h)** and **Pace (min/km)**.
  - **Estimated Steps** for running and walking activities.
  - **Estimated Calories** when data is missing from Strava.
- **Interactive Visualizations:**
  - Route maps, trend lines, comparison bars, and activity-type donuts.
  - Intuitive graphs where "up" always means "better" (e.g., Pace charts are inverted).

## 🛠️ Technology Stack

- **Language:** Python 3.9+
- **Data Processing:** Pandas, NumPy
- **API Interaction:** Requests
- **Visualization:** Plotly, Folium
- **Dashboard Framework:** Jupyter Notebook
- **Local AI:** Ollama with `mistral-nemo`
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

This project is now designed to be run entirely from the Jupyter Notebook.

### 1. Prerequisites
- Python 3.9 or higher installed.
- A Strava account.
- **API Credentials:** Get your `Client ID` and `Secret` from [Strava API Settings](https://www.strava.com/settings/api).
- **(Optional for AI features)** [Ollama](https://ollama.com/) installed and running with the `mistral-nemo` model (`ollama run mistral-nemo`).

### 2. Setup
Clone the repository and run the setup script for your OS to create the virtual environment and install dependencies.

**Mac/Linux:**
```bash
./scripts/setup.sh
```

**Windows:**
```bat
scripts\setup.bat
```

### 3. Configuration
Copy the `.env.example` file to `.env` and add your Strava credentials.
```bash
cp .env.example .env
# Now, edit the .env file and paste your STRAVA_CLIENT_ID and STRAVA_CLIENT_SECRET
```

### 4. Running the Project
Activate your virtual environment, then start Jupyter.

**Activate Environment:**
- Mac/Linux: `source venv/bin/activate`
- Windows: `venv\Scripts\activate`

**Start Jupyter:**
```bash
jupyter notebook dashboard.ipynb
```
Inside the notebook, **make sure to select the `venv` kernel**. You will find cells at the top for a one-time setup (Authentication and Data Fetching). Run them, and your dashboard will be ready to use.

## ❓ Troubleshooting

### "Missing Strava API credentials"
- Ensure you created the `.env` file from the `.env.example` template.
- Verify you copied the correct Client ID and Secret from your Strava settings.

### "No valid token found" or Authentication Errors
- Run the Authentication cell at the top of the `dashboard.ipynb` notebook.
- Ensure you copy the full URL from your browser after authorizing, including the `&code=...` part.

### "No module named pandas" (or similar in Jupyter Notebook)
- Ensure you have selected the correct Jupyter kernel. It should be named `venv` or point to the Python interpreter inside the `venv` folder.

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
- [Presentation Notes](docs/pptnotes.md): Notes for the project presentation.
- [Smart Commands Guide](SMART_COMMANDS_GUIDE.md): Reference for all available dashboard commands.

## 📄 License
This project is created for educational purposes as part of the MBDIA curriculum.