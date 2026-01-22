"""
Strava Smart Analyst Interface
==============================

This module provides the high-level 'Intelligent Analyst Interface' (Smart Commands) for the 
Strava Dashboard. It simplifies complex data fetching and plotting into 
single, readable commands.

What this file does:
1. Orchestrates DataManager, ActivityProcessor, and Visualizations.
2. Provides the 'show()', 'plot()', 'compare()', and 'filter()' functions.
3. Manages a global state including active filters.

Usage:
    import src.analyst as analyst
    analyst.filter(sport="Run")
    analyst.show("summary")
    analyst.plot("map", index=0)
"""

from .data_manager import DataManager
from .data_processing import ActivityProcessor
from .ai_assistant import AIAssistant
from . import visualizations as viz
import pandas as pd
from IPython.display import display, Markdown

# Global state
_dm = None
_processor = None
_ai = None
_df = None        # The full, original dataframe
_active_df = None # The filtered dataframe used for analysis

def _ensure_initialized():
    """Lazy initialization of data components"""
    global _dm, _processor, _ai, _df, _active_df
    if _dm is None:
        _dm = DataManager()
        try:
            # Load raw data
            raw_df = _dm.load_activities_as_dataframe()
            
            # Enrich data using ActivityProcessor
            _processor = ActivityProcessor(raw_df)
            _df = _processor.df  # Store the ENRICHED dataframe
            
            # Initialize filtered state with enriched data
            if _active_df is None:
                _active_df = _df.copy()
            
            _ai = AIAssistant(_active_df)
        except Exception as e:
            print(f"⚠️ Error initializing data: {e}")
            print("Please ensure you have run 'python -m src.data_manager' first.")

def _update_processor():
    """Update the processor when the active dataframe changes"""
    global _processor, _ai, _active_df
    if _active_df is not None:
        # Re-enrich just in case or just update dependencies
        _processor = ActivityProcessor(_active_df)
        _active_df = _processor.df # Ensure active_df has latest computed metrics
        _ai = AIAssistant(_active_df)

def filter(sport=None, reset=False):
    """
    Filter the dataset for subsequent analysis.
    
    Args:
        sport (str): 'Run', 'Ride', 'Walk', etc.
        reset (bool): If True, clears all filters.
    """
    global _df, _active_df
    _ensure_initialized()
    
    if reset:
        _active_df = _df.copy()
        print("✅ Filters cleared. Using all data.")
    elif sport:
        if isinstance(sport, list):
            _active_df = _df[_df['type'].isin(sport)].copy()
            print(f"✅ Filter applied: Activity Types = {sport} ({len(_active_df)} activities)")
        else:
            _active_df = _df[_df['type'] == sport].copy()
            print(f"✅ Filter applied: Activity Type = '{sport}' ({len(_active_df)} activities)")
    
    _update_processor()

def refresh():
    """
    Force a refresh of data from Strava API and reload.
    """
    _ensure_initialized()
    if _dm is None: return
    
    print("🔄 Refreshing data from Strava...")
    _dm.fetch_and_cache_activities(force_refresh=True)
    _dm.fetch_and_cache_athlete_info(force_refresh=True)
    
    # Reload data into memory
    global _df, _active_df
    _df = _dm.load_activities_as_dataframe()
    
    if 'start_date_local' in _df.columns:
        _df['start_date_local'] = pd.to_datetime(_df['start_date_local'])
        
    # Reset active df to full data to ensure consistency
    _active_df = _df.copy()
    
    _update_processor()
    print("✅ Data refreshed successfully!")

def ask(question):
    """
    Ask the Intelligent Assistant a question about your data.
    
    Args:
        question (str): Your question (e.g., "Am I improving?", "Summary")
    """
    _ensure_initialized()
    if _ai is None: return
    
    print(f"🤖 Asking Ollama ({_ai.model})...")
    response = _ai.ask(question)
    display(Markdown(response))

def show(command="summary", **kwargs):
    """
    The main Smart Command function to show data or insights.
    
    Examples:
        show("summary")
        show("recent", limit=5)
        show("types")
    """
    _ensure_initialized()
    if _processor is None: return

    command = command.lower()
    
    if command == "summary":
        stats = _processor.get_summary_stats()
        # Basic name check to avoid crashing if athlete info missing
        try:
            name = _dm.fetch_and_cache_athlete_info()['firstname']
        except:
            name = "Athlete"
            
        print(f"--- Global Statistics for {name} ---")
        viz.plot_summary_table(stats)
        
    elif command == "recent":
        limit = kwargs.get('limit', 10)
        recent = _active_df.sort_values('start_date_local', ascending=False).head(limit)
        display(recent[['start_date_local', 'name', 'type', 'distance', 'total_elevation_gain']])
        
    elif command == "types":
        stats = _processor.get_summary_stats()
        viz.plot_activity_type_donut(stats)
        
    else:
        print(f"Unknown command: {command}. Try 'summary', 'recent', or 'types'.")

def compare(period="month"):
    """
    Compare your performance against the previous period.
    
    Args:
        period (str): 'month' or 'year'
    """
    _ensure_initialized()
    if _processor is None or _processor.df is None: return
    
    # Use processor.df which has the 'month', 'year' columns
    viz.plot_comparison(_processor.df, period=period)

def plot(what="progress", **kwargs):
    """
    The main Smart Command function to create visual plots.
    
    Examples:
        plot("progress")
        plot("heatmap", metric="steps")
        plot("map", index=0)
        plot("trend", metric="average_speed_kmh") # Changed default to speed
    """
    _ensure_initialized()
    if _processor is None: return

    what = what.lower()
    
    if what == "progress":
        weekly = _processor.get_weekly_aggregates().reset_index()
        viz.plot_weekly_progress(weekly)
    
    elif what == "heatmap":
        # Pass the metric to heatmap (now Daily Activity Bar), default to distance_km
        metric = kwargs.get('metric', 'distance_km')
        date = kwargs.get('date', None)
        # Use processor.df for date components
        viz.plot_heatmap(_processor.df, metric=metric, date=date)

    elif what == "map":
        idx = kwargs.get('index', 0)
        # Sort by date to make '0' the latest
        sorted_df = _active_df.sort_values('start_date_local', ascending=False)
        if idx < len(sorted_df):
            activity = sorted_df.iloc[idx]
            print(f"Displaying map for: {activity['name']} ({activity['start_date_local'].date()})")
            return viz.plot_activity_map(activity)
        else:
            print(f"Index {idx} out of range (total activities: {len(sorted_df)})")
            
    elif what == "trend":
        metric = kwargs.get('metric', 'average_speed_kmh') # Default to average_speed_kmh
        
        # Friendly aliases
        if metric == 'pace': metric = 'average_pace_min_km'
        if metric == 'speed': metric = 'average_speed_kmh'
        if metric == 'distance': metric = 'distance_km'
        
        # Check if metric exists in filtered df (ActivityProcessor adds them)
        viz.plot_metric_trend(_processor.df, metric=metric)
        
    else:
        print(f"Unknown plot type: {what}. Try 'progress', 'heatmap', 'map', or 'trend'.")

def details(index=0):
    """
    Show detailed statistics for a specific activity.
    
    Args:
        index (int): Index of the activity (0 is the latest).
    """
    _ensure_initialized()
    if _processor is None: return
    
    # Sort by date descending
    sorted_df = _active_df.sort_values('start_date_local', ascending=False)
    
    if index >= len(sorted_df):
        print(f"Index {index} out of range (total activities: {len(sorted_df)})")
        return

    activity = sorted_df.iloc[index]
    
    # Extract details
    name = activity.get('name', 'Unknown')
    date = activity.get('start_date_local').strftime('%Y-%m-%d')
    start_time = activity.get('start_date_local').strftime('%H:%M:%S')
    
    # Calculate End Time
    moving_time_sec = activity.get('moving_time', 0)
    end_time_dt = activity.get('start_date_local') + pd.Timedelta(seconds=moving_time_sec)
    end_time = end_time_dt.strftime('%H:%M:%S')
    
    dist_km = activity.get('distance_km', 0)
    moving_time_str = f"{int(moving_time_sec // 3600)}h {int((moving_time_sec % 3600) // 60)}m"
    
    # Calories: prefer kilocalories, then kilojoules. If missing, ESTIMATE.
    kcal = activity.get('kilocalories')
    if pd.isna(kcal) or kcal == 0:
        kcal = activity.get('kilojoules')
    
    estimated_kcal = False
    if pd.isna(kcal) or kcal == 0:
        # Estimation logic
        # Run/Walk: ~1 kcal/kg/km. Weight defaults to 75kg if missing.
        # Ride: Harder, but let's assume loose 25-30 kcal/km for moderate effort? (Very rough)
        # Actually for ride, kJ is better. If kJ is 0, maybe no power meter.
        
        weight = 75.0 # Default
        try:
            athlete = _dm.fetch_and_cache_athlete_info()
            if athlete.get('weight'):
                weight = athlete['weight']
        except:
            pass
            
        activity_type = activity.get('type')
        if activity_type in ['Run', 'Walk', 'Hike']:
            # Factor: ~0.9-1.0 kcal/kg/km. 
            kcal = dist_km * weight * 0.95
            estimated_kcal = True
        elif activity_type == 'Ride':
            # Very rough estimate: ~30 kcal / km (highly variable)
            kcal = dist_km * 30
            estimated_kcal = True
        else:
            kcal = 0.0

    avg_pace = activity.get('average_pace_min_km')
    avg_hr = activity.get('average_heartrate', 'N/A')
    activity_type = activity.get('type', 'Unknown')
    
    print(f"--- Activity Details: {name} ---")
    print(f"Workout type: {activity_type}")
    print(f"Date:       {date}")
    print(f"Time:       {start_time} - {end_time}")
    print(f"Duration:   {moving_time_str}")
    
    if dist_km > 0:
        print(f"Distance:   {dist_km:.2f} km")
    else:
        print(f"Distance:   0.00 km")
        
    kcal_str = f"{kcal:.0f} kcal"
    if estimated_kcal:
        kcal_str += " (est.)"
    print(f"Calories:   {kcal_str}")
    
    if avg_pace and not pd.isna(avg_pace) and avg_pace > 0:
        print(f"Avg Pace:   {avg_pace:.2f} min/km")
    else:
        print(f"Avg Pace:   N/A")
        
    print(f"Avg HR:     {avg_hr} bpm")

def get_data():
    """Returns the current (filtered) DataFrame"""
    _ensure_initialized()
    return _active_df