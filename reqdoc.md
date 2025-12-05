# Project Requirements: Strava Data Dashboard

## 1. Project Overview
**Goal:** Build an interactive data dashboard using Python to visualize and analyze personal Strava activity data.
**Scope:** The application will authenticate with the Strava API, fetch user activity data, process it using Pandas, and display insights via a web-based dashboard.

## 2. Functional Requirements

### 2.1 Data Acquisition (Backend)
- **Authentication:** Implement OAuth 2.0 to securely authorize access to the user's Strava account.
- **API Integration:**
  - Fetch a summary list of all user activities (Rides, Runs, Swims).
  - Fetch detailed "streams" (time, lat/lng, altitude, heart rate, cadence, temp) for individual activities.
- **Data Storage:** (Optional) Cache data locally (CSV/JSON/SQLite) to reduce API calls during development.

### 2.2 Data Processing
- Use `pandas` to clean and structure the JSON responses.
- Calculate derived metrics if missing (e.g., moving time vs. elapsed time, average pace).

### 2.3 Dashboard Features (Frontend)
- **Global Statistics:** Display total distance, elevation gain, and count of activities.
- **Activity List:** A table view of recent activities with filtering options (e.g., by sport type).
- **Detailed Activity View:**
  - Select an activity to view its specific details.
  - **XY Diagrams:** Plot metrics like Elevation, Speed, and Heart Rate against Distance or Time.
  - **Map Visualization:** Display the route GPS data on an interactive map.
- **Trend Analysis:** Charts showing progress over time (e.g., Weekly Distance).

## 3. Technology Stack Selection
Based on the requirement to "Select one tool," we will proceed with **Streamlit** for its ease of use with data scripts, while using **Plotly** for the charting component.

- **Language:** Python
- **Web Framework:** Streamlit (or Plotly Dash)
- **Data Manipulation:** Pandas
- **Visualization:** Plotly (for graphs), Folium/PyDeck (for maps)
- **API Handling:** Requests

## 4. References & Resources
- **Login:** https://www.strava.com/login
- **API Reference:** https://developers.strava.com/docs/reference/
- **Getting Started:** https://developers.strava.com/docs/getting-started/
- **Authentication Docs:** https://developers.strava.com/docs/authentication/
