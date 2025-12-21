# MBDIA25 CS - Strava Dashboard Project Presentation

## Slide 1: Title Slide
- **Project Title:** Strava Data Dashboard
- **Subtitle:** Personal Activity Analysis & Visualization Tool
- **Team Members:** Akshay & Siddhanth
- **Course/Context:** MBDIA25 CS

---

## Slide 2: Introduction & Problem Statement
- **The Problem:**
    - Strava's default interface offers limited free analysis.
    - Users want custom metrics and offline access to their data.
    - Need for a personalized view of fitness progress.
- **The Solution:**
    - A Python-based dashboard that connects to Strava.
    - Fetches, stores, and visualizes activity data.
    - Provides interactive insights (Global stats, Weekly trends, Detailed activity analysis).

---

## Slide 3: Analysis Phase (Requirements)
*Discussion on how we determined what to build.*

- **Functional Requirements:**
    1.  **Authentication:** Secure login using Strava OAuth 2.0.
    2.  **Data Retrieval:** Fetch activities (Run, Ride, Swim) and detailed streams (Heart Rate, Elevation, GPS).
    3.  **Data Persistence:** Cache data locally to avoid hitting API rate limits (100 req/15min).
    4.  **Visualization:** Interactive charts for trends and individual activity performance.
- **User Stories:**
    - "As an athlete, I want to see my total distance for the year."
    - "As a data lover, I want to download my raw data as CSV."
    - "As a runner, I want to analyze my pace distribution."

---

## Slide 4: Design Phase (System Architecture)
*High-level view of how the system works.*

- **System Flow:**
    1.  **Strava API (Cloud):** Source of truth.
    2.  **Auth Module (`src/auth.py`):** Handles token exchange and refreshing.
    3.  **Data Layer (`src/data_manager.py`):**
        -   Fetches JSON data.
        -   Saves/Loads from local `data/` folder (JSON & CSV).
        -   Acts as a buffer between API and App.
    4.  **Processing Layer (`src/data_processing.py`):**
        -   Pandas-based cleaning.
        -   Unit conversions (m/s to km/h).
        -   Metric calculation (Weekly aggregations).
    5.  **Presentation Layer (`dashboard.ipynb`):**
        -   Jupyter Notebook interface.
        -   Plotly for rendering interactive graphs.

---

## Slide 5: Design Decisions & Trade-offs
*Why we made specific technical choices.*

- **Local Caching vs. Live Fetching:**
    - *Decision:* Implemented local caching (JSON/CSV).
    - *Reason:* Strava has strict API limits. Caching allows rapid development and offline viewing.
- **Jupyter Notebook vs. Web App (Streamlit):**
    - *Decision:* Shifted from Streamlit to Jupyter Notebook + Plotly.
    - *Reason:* Simplified the workflow. Removes the need for a separate web server process; keeps data analysis and visualization in one integrated environment.
- **Pandas & Plotly:**
    - *Reason:* Pandas offers robust time-series manipulation. Plotly provides interactivity (zoom/hover) which static libraries (Matplotlib) lack.

---

## Slide 6: Implementation Details
- **Tech Stack:**
    - **Language:** Python 3.x
    - **Libraries:**
        - `requests`: HTTP calls.
        - `pandas`: Data manipulation.
        - `plotly`: Interactive visualization.
        - `python-dotenv`: Security (API credentials).
- **Key Modules:**
    - `strava_api.py`: The low-level wrapper handling endpoints and pagination.
    - `data_processing.py`: The business logic engine.

---

## Slide 7: Live Demonstration
*Walkthrough of `dashboard.ipynb`*

- **Demo Points:**
    1.  **Setup:** Showing the `.env` configuration (briefly).
    2.  **Data Fetch:** Running `data_manager.py` to see new activities appear.
    3.  **Dashboard:**
        -   **Global Stats Table:** Total activities, distance, elevation.
        -   **Activity Distribution:** Pie chart (Run vs. Ride).
        -   **Weekly Progress:** Bar chart showing consistency.
        -   **Recent Activities:** Sortable data frame.

---

## Slide 8: Future Scope
- **Advanced Metrics:** Fatigue prediction, Fitness vs. Freshness graphs.
- **Map Integration:** Visualizing GPS routes on interactive maps (Folium).
- **Social Features:** Comparing stats with friends.
- **Automated Reports:** Weekly email summaries.

---

## Slide 9: Conclusion
- Successfully built a robust, local data analysis tool.
- Mastered OAuth 2.0 flow and API integration.
- Created a scalable architecture separating data fetching from visualization.
- Empowered the user with ownership of their fitness data.

---
