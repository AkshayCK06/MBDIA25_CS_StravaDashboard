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
- **Smart Command Interface (`strava`):**
  - `strava.refresh()`: Pull the latest data from the Strava API and update the cache.
  - `strava.filter(sport="Run")`: Filter the dashboard for specific sports (e.g., Run, Ride, Walk). Use `reset=True` to clear.
  - `strava.show("summary")`: Get a high-level overview of all activities.
  - `strava.compare("month")`: Compare performance (Avg/Max/Min Speed) for Rides and Walks against the previous month.
  - `strava.plot("trend")`: View performance trends over time (Speed, Pace, or Distance).
  - `strava.plot("heatmap")`: A monthly bar chart showing daily activity levels.
  - `strava.plot("map", index=0)`: Interactive route map for your latest activities.
  - `strava.details(index)`: Detailed stats for a specific activity, including estimated calories and timing.
- **AI Integration (Ollama):** Local LLM support (`strava.ask(...)`) to answer natural language questions about your data, acting as a personal fitness coach while ensuring 100% privacy.
- **Advanced Data Enrichment:**
  - **Auto-Translation:** Automatically translates German activity names (e.g., "Morgenlauf") to English.
  - **Metric Calculation:** Automatic calculation of **Speed (km/h)** and **Pace (min/km)**.
  - **Estimated Steps:** Derived from cadence data for running and walking activities.
  - **Smart Calories:** Estimated metabolic burn for activities where Strava data is missing.
- **Interactive Visualizations:**
  - Route maps, trend lines, comparison bars, and activity-type donuts.
  - Intuitive graphs where "up" always means "better" (e.g., Pace charts are automatically inverted).

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
│   ├── ai_assistant.py     # Ollama AI integration logic
│   ├── analyst.py          # Intelligent Analyst Interface (Smart Commands)
│   ├── auth.py             # OAuth 2.0 authentication handler
│   ├── config.py           # Configuration and path management
│   ├── data_manager.py     # Data fetching and caching logic
│   ├── data_processing.py  # Pandas analysis and metrics enrichment
│   ├── strava_api.py       # Strava API wrapper
│   └── visualizations.py   # Plotly and Folium chart generators
├── docs/                   # Project documentation & requirements
├── scripts/                # Setup scripts (Mac/Linux/Windows)
├── data/                   # Cached activity data (Local only)
├── cache/                  # Auth tokens (Local only)
├── dashboard.ipynb         # Interactive Jupyter Notebook Dashboard
└── requirements.txt        # Python dependencies
```

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.9 or higher installed.
- A Strava account and [API Credentials](https://www.strava.com/settings/api).
- **For AI Features:** [Ollama](https://ollama.com/) installed and running.

### 2. Setup
Clone the repository and run the setup script for your OS.

**Mac/Linux:**
```bash
./scripts/setup.sh
```

**Windows:**
```bat
scripts\setup.bat
```

### 3. Configuration
Copy `.env.example` to `.env` and add your `STRAVA_CLIENT_ID` and `STRAVA_CLIENT_SECRET`.

### 4. Running the Dashboard
Activate your environment and start Jupyter:
```bash
# Mac/Linux
source venv/bin/activate
jupyter notebook dashboard.ipynb
```
Inside the notebook, select the **venv** kernel and run the initialization cells at the top.

---

## 🤖 Setting up the AI Assistant (`strava.ask`)

The dashboard includes a local AI coach that uses Ollama to analyze your data privately.

### 1. Install Ollama
Download and install Ollama from [ollama.com](https://ollama.com/).

### 2. Download the Model
Open your terminal and pull the Mistral Nemo model:
```bash
ollama pull mistral-nemo
```

### 3. Start the Ollama Server
Ensure Ollama is running in the background. Usually, it starts automatically, but you can force it with:
```bash
ollama serve
```

### ⚡ Lite Mode (Optional)
If `mistral-nemo` is too slow or you have limited RAM (under 8GB), you can use a lighter model like `llama3.2`.

1. **Pull the lighter model:**
   ```bash
   ollama pull llama3.2
   ```
2. **Configure `.env`:**
   Add or update this line in your `.env` file:
   ```env
   OLLAMA_MODEL=llama3.2
   ```

### 4. Talk to your Data
In the `dashboard.ipynb`, you can now use natural language:
```python
strava.ask("How has my running pace improved over the last 3 months?")
strava.ask("Give me a summary of my most active week.")
```

---

## 👥 Division of Work

### Backend Developer
- ✅ OAuth authentication & API integration
- ✅ Data caching & Lifecycle management
- ✅ Metric enrichment & Auto-translation logic
- ✅ Ollama AI Assistant integration

### Frontend Developer
- ✅ Interactive Notebook Dashboard UI
- ✅ Smart Command Interface (`analyst.py`)
- ✅ Plotly visualizations & Folium Map integration
- ✅ Comparative Performance Analysis

## 📚 Documentation
- [Smart Commands Guide](SMART_COMMANDS_GUIDE.md): Reference for all available dashboard commands.
- [Requirements](docs/reqdoc.md): Functional and technical requirements.
- [Presentation Notes](docs/pptnotes.md): Notes for the project presentation.

## 📄 License
This project is created for educational purposes as part of the MBDIA curriculum.