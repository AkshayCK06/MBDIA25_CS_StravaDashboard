# Strava Intelligent Analyst: Smart Commands Guide

This guide provides a comprehensive reference for the **Intelligent Analyst Interface** used in the Strava Dashboard. This system allows you to analyze your fitness data using simple, human-readable commands instead of writing complex Python code.

## 1. Initialization

Before running any commands, you must import the analyst module.

```python
import src.analyst as strava
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
| `"trend"` | Displays a Line Chart of a specific metric over time. | `metric` (str): 'distance', 'speed', 'pace', 'elevation'. | `strava.plot("trend", metric="pace")` |
| `"map"` | Renders an interactive GPS map of a specific activity. | `index` (int, default=0): 0 is the latest activity, 1 is the previous, etc. | `strava.plot("map", index=0)` |
| `"heatmap"` | Displays a heatmap of activity intensity (Month vs Day of Week). | `metric` (str, default='distance_km'): Metric to visualize intensity. | `strava.plot("heatmap", metric="distance_km")` |

---

## 4. Command: `compare()`
**Purpose:** Compare your performance between time periods.

### Syntax
```python
strava.compare(period="month")
```

### Options

| Period | Description | Example |
| :--- | :--- | :--- |
| `"month"` | Compares the current month vs. the previous month. | `strava.compare("month")` |
| `"year"` | Compares the current year vs. the previous year. | `strava.compare("year")` |

---

## 6. Command: `filter()`
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

# 2. See how your running pace is trending
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

# 3. See which days you are most active
strava.plot("heatmap")
```
