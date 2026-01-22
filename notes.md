# Strava Analytics Dashboard — Live Demo Speaking Notes

These notes are aligned with the **current dashboard.ipynb structure**, organized by
**Initialization → Smart Commands**, and intended to be used while showing
`dashboard.ipynb` side-by-side with `SMART_COMMANDS_GUIDE.md`.

---

## Title: Strava Analytics Dashboard

**What to say (5–7 sec):**
- This notebook represents the interactive dashboard layer of our project.
- All heavy logic such as API calls, processing, and analytics lives in backend Python modules.
- The notebook only exposes clean, high-level commands for the user.

---

## Initialization

### Markdown Cell — Initialization Overview

**What to say (10–15 sec):**
- We start by loading our custom `analyst` module.
- This module acts as a controller and connects all backend components.
- Every smart command you see later comes from this single interface.

---

### Code Cell — Import & Setup

**What to say (15–20 sec):**
- In this step, we import the analyst interface and initialize the system.
- Authentication, API handling, and data loading are already managed internally.
- The notebook intentionally avoids low-level code to keep it readable and user-friendly.

---

## Smart Commands (Transition)

### Markdown Cell — Smart Commands Introduction

**What to say (10 sec):**
- Now we move to the smart-command interface.
- On the right, we have the documentation explaining each command.
- On the left, we’ll execute those commands live in the notebook.

---

## Command: strava.show()

### Markdown Cell — Purpose

**What to say (10 sec):**
- The `show()` command is used for quick summaries and tabular insights.
- It helps us understand the data before moving to visualizations.

---

### Code Cell(s) — Examples

**Typical commands:**
- `strava.show("summary")`
- `strava.show("types")`
- `strava.show("recent", limit=5)`

**What to say (20–30 sec):**
- Here we see global summary metrics such as total distance and average speed.
- Activity type distribution gives an overview of how workouts are split.
- Recent activities help quickly inspect the latest workouts.
- Behind the scenes, this data is already cleaned and aggregated in the analytics layer.

---

## Command: strava.plot()

### Markdown Cell — Purpose

**What to say (10 sec):**
- The `plot()` command generates interactive visualizations.
- We use Plotly for charts and Folium for maps.

---

### Code Cell(s) — Examples

**Typical commands:**
- `strava.plot("trend")`
- `strava.plot("trend", metric="pace")`
- `strava.plot("heatmap")`
- `strava.plot("map", index=0)`

**What to say (30–40 sec):**
- These charts are fully interactive: we can zoom, hover, and explore trends.
- Trend plots show how metrics evolve over time.
- The map visualization uses GPS data from Strava and renders the actual activity route.
- The notebook itself does not process raw GPS data — this is handled in backend modules.

---

## Command: strava.details()

### Markdown Cell — Purpose

**What to say (10 sec):**
- The `details()` command drills down into a single activity.

---

### Code Cell — Example

**Typical command:**
- `strava.details(1)`

**What to say (20–25 sec):**
- This provides a clean summary of one workout, including distance, pace, and calories.
- If calories are missing from Strava, they are estimated automatically.
- This logic is implemented in the data processing layer, not in the notebook.

---

## Command: strava.filter()

### Markdown Cell — Purpose

**What to say (10 sec):**
- The `filter()` command applies a global filter to the dataset.

---

### Code Cell — Example

**Typical commands:**
- `strava.filter(sport="Walk")`
- `strava.show("summary")`
- `strava.filter(reset=True)`

**What to say (25–30 sec):**
- Once a filter is applied, all subsequent commands work on the filtered data.
- This allows fast exploration without repeatedly passing filter arguments.
- Resetting the filter restores the full dataset.

---

## Command: strava.compare()

### Markdown Cell — Purpose

**What to say (10 sec):**
- The `compare()` command is used to compare performance between time periods.

---

### Code Cell — Example

**Typical command:**
- `strava.compare("month")`

**What to say (20–25 sec):**
- Here we compare the current month against the previous month.
- Metrics like average speed and total distance are aggregated automatically.
- These comparisons are computed in the analytics layer, not hardcoded.

---

## Command: strava.ask() — AI Assistant

### Markdown Cell — Purpose

**What to say (15 sec):**
- This command enables natural-language interaction with the data.
- It uses a local LLM, so all data stays on the user’s machine.

---

### Code Cell — Example

**Typical command:**
- `strava.ask("What should I improve based on my recent activity?")`

**What to say (30–40 sec):**
- The model receives a structured summary of the activity data, not raw tables.
- This keeps the interaction efficient and privacy-friendly.
- This turns analytics into a conversational interface instead of just charts.

---

## Feedback Section

### Markdown / QR Code Cell

**What to say (10 sec):**
- Before we conclude, we’d appreciate your feedback.
- The QR code links to a short form where you can suggest features or improvements.
- This helps guide future iterations of the project.

---

## Closing (Optional)

**What to say (5–10 sec):**
- The same backend can easily support a web or mobile application.
- The notebook is just one interface on top of a reusable analytics pipeline.