# 🎙️ Strava Dashboard Presentation Notes

**Project**: Intelligent Strava Analyst
**Presenters**: Akshay & Siddhanth
**Goal**: Demonstrate a flexible, user-friendly tool for Strava data analysis using an Intelligent Analyst Interface.

---

## 1. The Narrative (Storyline)

**The Problem:**
*   Most fitness dashboards are "Static." They show you what *they* want (generic charts), not what *you* want.
*   Users suffer from "Dashboard Fatigue"—too many numbers, hard to find specific answers.
*   "I just want to know if I'm running faster than last month." "How many steps did I take?" "What were the details of that one long ride?"

**The Solution:**
*   We built the **"Intelligent Analyst."**
*   It's not just a dashboard; it's a **Command Line Interface for your Fitness.**
*   We used a **Smart Commands** approach combined with **Local AI (Ollama)** for privacy-first, powerful analysis.

---

## 2. Division of Presentation

### **Part 1: The Engine (Akshay)**
*   **Focus:** Backend, Architecture, Data.
*   **Key Points:**
    *   **OAuth 2.0:** "Securely connecting to Strava (Token management)."
    *   **Data Manager:** "Smart caching system. We fetch raw JSON, process it, and store it locally so it works offline and is fast."
    *   **Data Processing:** "This is where we add value. We enrich the data with metrics Strava doesn't give you directly:
        *   **Speed in km/h & Pace in min/km** for all activities.
        *   **Unified Kilocalories**, combining `calories` and `kilojoules` data.
        *   **Estimated Steps** calculated from cadence data.
        *   **Auto-translation** of common German activity names to English."
    *   **Architecture:** "Modular design. `data_manager` fetches, `data_processing` enriches, `visualizations` plots, and `analyst.py` provides the simple commands for the user."

### **Part 2: The Experience (Siddhanth)**
*   **Focus:** Smart Commands, Visualizations, Demo.
*   **Key Points:**
    *   "We moved away from a cluttered web app."
    *   "We built a Smart Interface inside Jupyter Notebook, where you can talk to your data."
    *   **Live Demo:** (Run the `dashboard.ipynb` cells one by one).

---

## 3. The Live Demo Flow (Siddhanth)

*Open `dashboard.ipynb` and run these cells live.*

1.  **First-Time Setup (In-Notebook):**
    *   *Say:* "We've made the setup incredibly simple. For a first-time user, you just run two cells directly in the notebook to authenticate and fetch your data. No more terminal commands needed."
    *   *(Show the `StravaAuth` and `DataManager` cells)."
2.  **Refresh Data:** `strava.refresh()`
    *   *Say:* "Once set up, keeping your data current is as easy as running `strava.refresh()`."
3.  **Global Stats:** `strava.show("summary")`
    *   *Say:* "Instantly, I get a snapshot of my entire history, with key metrics like total distance and average speed."
4.  **Monthly Breakdown:** `strava.plot("heatmap", metric="steps")`
    *   *Say:* "We replaced the old heatmap with a **Daily Activity Chart**. I can see my total steps for each day of this month."
5.  **Improved Comparison:** `strava.compare("month")`
    *   *Say:* "Am I getting faster? Our `compare` command now shows separate graphs for **Rides** and **Walks**, comparing key speed metrics against last month."
6.  **Intuitive Trend Analysis:** `strava.plot("trend")`
    *   *Say:* "Let's check my performance over time. The trend graph defaults to **Speed in km/h**. You can see rides are correctly shown as faster than walks. If you prefer `pace`, the graph automatically inverts so 'up' is always 'faster'."
7.  **Drill-Down with Details:** `strava.details(index=0)`
    *   *Say:* "After seeing a spike on the trend, I can use our new `details` command to get a clean summary of any activity, including estimated calories if they were missing."
8.  **AI Assistant:** `strava.ask("Give me a summary of my performance last month")`
    *   *Say:* "Finally, for open-ended questions, our local AI (running on Ollama) gives a private, conversational summary of my performance."

---

## 4. Future Improvements (The "Roadmap")

*Mention these at the end to show you have a vision.*

1.  **Voice Interface:**
    *   "Connect the AI to a Speech-to-Text engine so you can talk to your data."
2.  **Goal Tracking:**
    *   "Add a command like `strava.set_goal('100km')` and a progress bar."
3.  **Social Comparison:**
    *   "Since our Auth module handles tokens, we could compare stats with a friend."

---

## 5. Technical Highlights (If Asked)

*   **Polylines:** "We use the Google Polyline algorithm to decode compressed strings into lat/long coordinates for maps."
*   **Pandas:** "All filtering and aggregation happens in memory using Pandas for speed."
*   **Plotly:** "We chose Plotly over Matplotlib for interactivity (zooming, hovering)."
*   **Calorie Estimation:** "When calorie data is missing, we use metabolic formulas (METs) with a default weight to provide an estimate, marked as `(est.)`."
*   **Ollama & Local AI:** "We use Ollama to run the Mistral-Nemo model locally, ensuring user data remains 100% private."