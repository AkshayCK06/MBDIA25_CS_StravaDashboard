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
from . import visualizations as viz
import pandas as pd
from IPython.display import display, Markdown

# Global state
_dm = None
_processor = None
_df = None        # The full, original dataframe
_active_df = None # The filtered dataframe used for analysis

def _ensure_initialized():
    """Lazy initialization of data components"""
    global _dm, _processor, _df, _active_df
    if _dm is None:
        _dm = DataManager()
        try:
            _df = _dm.load_activities_as_dataframe()
            # Basic cleaning
            if 'start_date_local' in _df.columns:
                _df['start_date_local'] = pd.to_datetime(_df['start_date_local'])
            
            # Initialize filtered state with full data
            if _active_df is None:
                _active_df = _df.copy()
                
            _processor = ActivityProcessor(_active_df)
        except Exception as e:
            print(f"⚠️ Error initializing data: {e}")
            print("Please ensure you have run 'python -m src.data_manager' first.")

def _update_processor():
    """Update the processor when the active dataframe changes"""
    global _processor, _active_df
    if _active_df is not None:
        _processor = ActivityProcessor(_active_df)

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
        plot("heatmap")
        plot("map", index=0)
        plot("trend", metric="average_pace_min_km")
    """
    _ensure_initialized()
    if _processor is None: return

    what = what.lower()
    
    if what == "progress":
        weekly = _processor.get_weekly_aggregates().reset_index()
        viz.plot_weekly_progress(weekly)
    
    elif what == "heatmap":
        # Pass the metric to heatmap, default to distance_km
        metric = kwargs.get('metric', 'distance_km')
        # Use processor.df for date components
        viz.plot_heatmap(_processor.df, metric=metric)

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
        metric = kwargs.get('metric', 'distance_km')
        
        # Friendly aliases
        if metric == 'pace': metric = 'average_pace_min_km'
        if metric == 'speed': metric = 'average_speed_kmh'
        if metric == 'distance': metric = 'distance_km'
        
        # Check if metric exists in filtered df (ActivityProcessor adds them)
        # We need to rely on the processor's enriched dataframe, which is stored in the processor but not exposed directly as _active_df 
        # Actually _active_df is just the raw data + some cleaning. The processor adds metrics to its OWN copy.
        # We should use the processor's dataframe for plotting trends.
        
        viz.plot_metric_trend(_processor.df, metric=metric)
        
    else:
        print(f"Unknown plot type: {what}. Try 'progress', 'heatmap', 'map', or 'trend'.")

def get_data():
    """Returns the current (filtered) DataFrame"""
    _ensure_initialized()
    return _active_df