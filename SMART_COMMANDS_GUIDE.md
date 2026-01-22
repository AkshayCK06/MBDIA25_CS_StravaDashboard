# Smart Commands Guide

This system allows you to analyze your fitness data using simple, human-readable commands instead of writing complex Python code.

## 1. Initialization

Before running any commands, you must import the analyst module.

```python
import src.analyst as strava
```

To refresh your data from Strava:
```python
strava.refresh()
```

---

## 2. Command: `show()`
**Purpose:** Display lists, tables, and summary statistics.

### Syntax
```python
strava.show(command, **kwargs)
```

### Options

| Command | Description | Arguments | Example |
| :--- | :--- | :--- | :--- |
| `"summary"` | Shows global statistics (Total Distance, Avg Speed, etc.) in a formatted table. | None | `strava.show("summary")` |
| `"recent"` | Lists your most recent activities. | `limit` (int, default=10): Number of activities to show. | `strava.show("recent", limit=5)` |
| `"types"` | Visualizes the breakdown of activity types (Run, Ride, Walk) using a Donut Chart. | None | `strava.show("types")` |

---

## 3. Command: `plot()`
**Purpose:** Generate interactive visualizations and charts.

### Syntax
```python
strava.plot(what, **kwargs)
```

### Options

| What | Description | Arguments | Example |
| :--- | :--- | :--- | :--- |
| `"progress"` | Displays a Bar Chart of distance covered per week. | None | `strava.plot("progress")` |
| `"trend"` | Displays a Line Chart of a specific metric over time. Default is **Speed (km/h)**. | `metric` (str): 'speed' (default), 'pace', 'distance', 'elevation'. | `strava.plot("trend", metric="pace")` |
| `"map"` | Renders an interactive GPS map of a specific activity. | `index` (int, default=0): 0 is the latest activity, 1 is the previous, etc. | `strava.plot("map", index=0)` |
| `"heatmap"` | Displays a **Daily Activity Bar Chart** for a specific month (default: current). | `metric`: 'distance_km'/'steps'. `date`: 'YYYY-MM' (e.g. '2024-01'). | `strava.plot("heatmap", date="2024-01")` |

---

## 4. Command: `details()`
**Purpose:** Drill down into the specific statistics of a single activity.

### Syntax
```python
strava.details(index=0)
```

### Options

| Argument | Description | Example |
| :--- | :--- | :--- |
| `index` | The index of the activity (0 = latest, 1 = second latest, etc.). | `strava.details(0)` |

*Displays: Workout Type, Date, Time, Duration, Distance, Calories (Estimated if missing), Avg Pace, Avg HR.*

---

## 5. Command: `compare()`
**Purpose:** Compare your performance between time periods.

### Syntax
```python
strava.compare(period="month")
```

### Options

| Period | Description | Example |
| :--- | :--- | :--- |
| `"month"` | Compares the **Current Month vs. Previous Month**. Shows separate charts for **Rides** and **Walks**, comparing Avg/Max/Min Speed. | `strava.compare("month")` |

---

## 6. Command: `ask()`
**Purpose:** Interact with the Local AI Assistant (Ollama) to get natural language insights.

### Syntax
```python
strava.ask(question)
```

### Options

| Question | Description | Example |
| :--- | :--- | :--- |
| Any text | The AI analyzes your data summary and answers your question. | `strava.ask("Am I training too hard?")` |

*Note: Requires Ollama to be running (`ollama serve`).*

---

## 7. Command: `filter()`
**Purpose:** Apply a global filter to the dataset. All subsequent `show()` and `plot()` commands will only use the filtered data.

### Syntax
```python
strava.filter(sport=None, reset=False)
```

### Options

| Argument | Description | Example |
| :--- | :--- | :--- |
| `sport` | Filter by activity type(s). Can be a string or a list. | `strava.filter(sport="Walk")` or `strava.filter(sport=["Run", "Ride"])` |
| `reset` | Clears all active filters and restores the full dataset. | `strava.filter(reset=True)` |

---

## 📘 Common Workflows

### Scenario 1: Analyzing Running Performance
```python
# 1. Focus only on runs
strava.filter(sport="Run")

# 2. See how your running pace is trending (Lower is Faster!)
strava.plot("trend", metric="pace")

# 3. Check your weekly running distance
strava.plot("progress")
```

### Scenario 2: Checking Monthly Improvement
```python
# 1. Reset any filters
strava.filter(reset=True)

# 2. Compare this month against last month
strava.compare("month")

# 3. See which days you are most active this month
strava.plot("heatmap")
```
