# 🎙️ Strava Dashboard Presentation Notes

**Project**: Intelligent Strava Analyst
**Presenters**: Akshay & Siddhanth
**Goal**: Demonstrate a flexible, user-friendly tool for Strava data analysis using an Intelligent Analyst Interface.

---

## 1. The Narrative (Storyline)

**The Problem:**
*   Most fitness dashboards are "Static." They show you what *they* want (generic charts), not what *you* want.
*   Users suffer from "Dashboard Fatigue"—too many numbers, hard to find specific answers.
*   "I just want to know if I'm running faster than last month."

**The Solution:**
*   We built the **"Intelligent Analyst."**
*   It's not just a dashboard; it's a **Command Line Interface for your Fitness.**
*   We used a **Smart Commands** approach: Simple, human-readable commands to generate complex insights instantly.

---

## 2. Division of Presentation

### **Part 1: The Engine (Akshay)**
*   **Focus:** Backend, Architecture, Data.
*   **Key Points:**
    *   **OAuth 2.0:** "Securely connecting to Strava (Token management)."
    *   **Data Manager:** "Smart caching system. We fetch raw JSON, process it, and store it locally so it works offline."
    *   **Data Processing:** "We calculate metrics Strava doesn't give you directly, like 'Pace (min/km)' and 'Weekly Aggregates'."
    *   **Architecture:** "Modular design. `src/visualizations.py` handles the math, `src/analyst.py` handles the user commands."

### **Part 2: The Experience (Siddhanth)**
*   **Focus:** Smart Commands, Visualizations, Demo.
*   **Key Points:**
    *   "We moved away from a cluttered web app."
    *   "We built a Smart Interface inside Jupyter Notebook."
    *   **Live Demo:** (Run the `dashboard.ipynb` cells one by one).

---

## 3. The Live Demo Flow (Siddhanth)

*Open `dashboard.ipynb` and run these cells live.*

1.  **Initialization:** "We import our tool as `strava`."
2.  **Global Stats:** `strava.show("summary")`
    *   *Say:* "Instantly, I get a snapshot of my entire history."
3.  **The "Wow" Moment:** `strava.plot("map", index=0)`
    *   *Say:* "Here is where it gets cool. We decode GPS polylines to show interactive maps right in the notebook."
4.  **Comparison:** `strava.compare("month")`
    *   *Say:* "Am I improving? This command instantly compares this month vs. last month."
5.  **The Power of Filters:** `strava.filter(sport="Walk")`
    *   *Say:* "Most dashboards mix everything. We can focus. Let's look ONLY at walks."
6.  **Trend Analysis:** `strava.plot("trend", metric="pace")`
    *   *Say:* "Now that we filtered for walks, this chart shows my Walking Pace trends over time."

---

## 4. Future Improvements (The "Roadmap")

*Mention these at the end to show you have a vision.*

1.  **AI Narrator:**
    *   "Integrate an LLM to read the data and write a text summary: 'Good job Sid, you ran 10% more this week!'"
2.  **Natural Language Processing (NLP):**
    *   "Instead of `strava.plot('map')`, allow typing: 'Show me the map of my longest run'."
3.  **Goal Tracking:**
    *   "Add a command like `strava.set_goal('100km')` and a progress bar."
4.  **Social Comparison:**
    *   "Since our Auth module handles tokens, we could compare stats with a friend."

---

## 5. Technical Highlights (If Asked)

*   **Polylines:** "We use the Google Polyline algorithm to decode compressed strings into lat/long coordinates."
*   **Pandas:** "All filtering and aggregation happens in memory using Pandas for speed."
*   **Plotly:** "We chose Plotly over Matplotlib for interactivity (zooming, hovering)."