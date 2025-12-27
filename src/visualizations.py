"""
Strava Visualization Toolbox
============================

This module contains reusable functions for creating interactive visualizations
of Strava data. It abstracts the complexity of Plotly and Folium.

What this file does:
1. Provides functions for common charts (Pie, Bar, Line).
2. Handles map generation from Strava polylines.
3. Formats data specifically for Jupyter Notebook display.

Usage:
    from src.visualizations import plot_activity_map, plot_weekly_progress
    plot_activity_map(df.iloc[0])
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
import polyline
from IPython.display import display, HTML

def plot_summary_table(stats: dict):
    """Display a clean HTML table of global statistics"""
    summary_data = {
        'Metric': ['Total Activities', 'Total Distance', 'Total Elevation', 'Moving Time', 'Avg Speed', 'Max Speed', 'Min Speed'],
        'Value': [
            f"{stats['total_activities']}",
            f"{stats['total_distance_km']:.1f} km",
            f"{stats['total_elevation_gain_m']:.0f} m",
            f"{stats['total_moving_time_hours']:.1f} hrs",
            f"{stats['average_speed_kmh']:.1f} km/h",
            f"{stats['max_speed_kmh']:.1f} km/h",
            f"{stats['min_speed_kmh']:.1f} km/h"
        ]
    }
    df_stats = pd.DataFrame(summary_data)
    display(HTML(df_stats.to_html(index=False, classes='table table-striped')))

def plot_activity_type_donut(stats: dict):
    """Plot distribution of activity types"""
    if 'activity_types' not in stats or not stats['activity_types']:
        print("No activity type data available.")
        return
        
    type_df = pd.DataFrame(list(stats['activity_types'].items()), columns=['Type', 'Count'])
    fig = px.pie(
        type_df, 
        values='Count', 
        names='Type', 
        title='Activities by Type',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig.update_layout(margin=dict(t=40, b=0, l=0, r=0))
    fig.show()

def plot_weekly_progress(weekly_df: pd.DataFrame):
    """Plot weekly distance bar chart"""
    if weekly_df.empty:
        print("No weekly data available.")
        return

    # Ensure date column for x-axis
    if 'week_start' not in weekly_df.columns:
        weekly_df['week_start'] = weekly_df.apply(
            lambda row: pd.to_datetime(f"{int(row['year'])}-W{int(row['week'])}-1", format="%G-W%V-%u"), 
            axis=1
        )
    
    fig = px.bar(
        weekly_df, 
        x='week_start', 
        y='distance_km', 
        title='Weekly Distance Progress',
        labels={'week_start': 'Week', 'distance_km': 'Distance (km)'},
        color_discrete_sequence=['#FC4C02'] # Strava Orange
    )
    fig.update_layout(xaxis_title="Week", yaxis_title="Distance (km)")
    fig.show()

def plot_activity_map(activity_row: pd.Series):
    """Plot an interactive map for a single activity using its polyline"""
    line = activity_row.get('map_polyline')
    
    if pd.isna(line) or not line:
        print(f"No map data available for activity: {activity_row['name']}")
        return None

    # Decode polyline
    coordinates = polyline.decode(line)
    
    # Create map centered at start
    start_point = coordinates[0]
    m = folium.Map(location=start_point, zoom_start=14, tiles='CartoDB positron')
    
    # Add path
    folium.PolyLine(coordinates, color='#FC4C02', weight=5, opacity=0.8).add_to(m)
    
    # Add start/end markers
    folium.Marker(coordinates[0], popup='Start', icon=folium.Icon(color='green', icon='play')).add_to(m)
    folium.Marker(coordinates[-1], popup='End', icon=folium.Icon(color='red', icon='stop')).add_to(m)
    
    # Fit bounds
    m.fit_bounds([min(coordinates), max(coordinates)])
    
    return m

def plot_metric_trend(df: pd.DataFrame, metric='distance', title=None):
    """Plot a trend line for a specific metric over time"""
    if df.empty:
        return
        
    df = df.sort_values('start_date_local')
    
    # Check if we have multiple types to compare
    has_multiple_types = 'type' in df.columns and df['type'].nunique() > 1
    
    fig = px.line(
        df, 
        x='start_date_local', 
        y=metric, 
        color='type' if has_multiple_types else None,
        title=title or f'{metric.replace("_", " ").title()} Over Time',
        template='plotly_white'
    )
    
    # Use Strava Orange only if it's a single line
    if not has_multiple_types:
        fig.update_traces(line_color='#FC4C02', line_width=2)
        
    fig.show()

def plot_heatmap(df: pd.DataFrame, metric='distance_km'):
    """Plot a heatmap of activity intensity (Day of Week vs Month)"""
    if df.empty: return

    # Ensure we have the right columns
    if 'month' not in df.columns or 'day_of_week' not in df.columns:
        print("Missing date components for heatmap.")
        return

    # Aggregate metric by Month and Day of Week
    # We want y=Month, x=Day of Week
    pivot_table = df.pivot_table(
        index='month', 
        columns='day_of_week', 
        values=metric, 
        aggfunc='sum',
        fill_value=0
    )

    # Reorder columns for correct day order
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot_table = pivot_table.reindex(columns=days_order)
    
    # Sort index (months) reversed so Jan is at top or bottom as preferred. 
    # Usually Heatmaps have Jan at top.
    
    fig = px.imshow(
        pivot_table,
        labels=dict(x="Day of Week", y="Month", color=metric),
        x=pivot_table.columns,
        y=pivot_table.index,
        title=f"Activity Heatmap ({metric})",
        color_continuous_scale='Oranges'
    )
    fig.show()

def plot_comparison(df: pd.DataFrame, period='month'):
    """Compare current period vs previous period"""
    if df.empty: return

    current_date = pd.Timestamp.now()
    
    if period == 'month':
        current_period = current_date.month
        current_year = current_date.year
        
        # Simple logic: This Month vs Last Month (same year handling for simplicity)
        # For a robust solution, we'd handle year roll-over, but for MVP:
        prev_period = current_period - 1 if current_period > 1 else 12
        prev_year = current_year if current_period > 1 else current_year - 1
        
        curr_data = df[(df['month'] == current_period) & (df['year'] == current_year)]
        prev_data = df[(df['month'] == prev_period) & (df['year'] == prev_year)]
        
        labels = ['Last Month', 'This Month']
        
    elif period == 'year':
        current_year = current_date.year
        prev_year = current_year - 1
        
        curr_data = df[df['year'] == current_year]
        prev_data = df[df['year'] == prev_year]
        
        labels = ['Last Year', 'This Year']
        
    else:
        print("Unsupported period. Use 'month' or 'year'.")
        return

    # Calculate metrics
    metrics = {
        'Distance (km)': [prev_data['distance_km'].sum(), curr_data['distance_km'].sum()],
        'Elevation (m)': [prev_data['total_elevation_gain'].sum(), curr_data['total_elevation_gain'].sum()],
        'Count': [len(prev_data), len(curr_data)]
    }
    
    # Create comparison dataframe for plotting
    comp_df = pd.DataFrame(metrics, index=labels).reset_index()
    comp_df = pd.melt(comp_df, id_vars=['index'], var_name='Metric', value_name='Value')
    
    fig = px.bar(
        comp_df, 
        x='index', 
        y='Value', 
        color='index', 
        facet_col='Metric', 
        facet_col_wrap=3,
        title=f"Comparison: {labels[0]} vs {labels[1]}",
        height=400,
        color_discrete_map={labels[0]: 'gray', labels[1]: '#FC4C02'}
    )
    # Allow independent y-axes for different scales (distance vs count)
    fig.update_yaxes(matches=None, showticklabels=True)
    fig.update_xaxes(title=None)
    fig.show()

