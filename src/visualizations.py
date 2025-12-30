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
    
    base_title = title or f'{metric.replace("_", " ").title()} Over Time'
    
    # Invert Y-axis for Pace (Lower is Faster)
    is_pace = 'pace' in metric
    if is_pace:
        base_title += " (Lower is Faster)"
    
    fig = px.line(
        df, 
        x='start_date_local', 
        y=metric, 
        color='type' if has_multiple_types else None,
        title=base_title,
        template='plotly_white'
    )
    
    # Use Strava Orange only if it's a single line
    if not has_multiple_types:
        fig.update_traces(line_color='#FC4C02', line_width=2)
    
    if is_pace:
        fig.update_yaxes(autorange="reversed")
        
    fig.show()

def plot_heatmap(df: pd.DataFrame, metric='distance_km'):
    """
    Plot daily activity for the current month (Bar Graph).
    Replaces the old heatmap as per user request.
    """
    if df.empty: return

    # Filter for current month/year
    now = pd.Timestamp.now()
    # Use the latest month in data if current month has no data, or just strict current month?
    # Strict current month is safer for "This Month" context.
    
    current_month_df = df[(df['month'] == now.month) & (df['year'] == now.year)].copy()
    
    if current_month_df.empty:
        print(f"No activities found for this month ({now.strftime('%B %Y')}).")
        # Optional: Try previous month if empty? No, sticking to specific request.
        return

    # Check if we can use steps
    if metric == 'steps' or (metric == 'distance_km' and 'estimated_steps' in df.columns and df['estimated_steps'].sum() > 0):
        # Prefer steps if available and significant, or if requested
        if 'estimated_steps' in df.columns:
            metric = 'estimated_steps'
            # Filter out rides for step count?
            # User asked "step counts for the whole month". 
            # If we include rides (where steps=0), it's fine.
            
    # Aggregate by day
    current_month_df['day'] = current_month_df['start_date_local'].dt.day
    daily_stats = current_month_df.groupby('day')[metric].sum().reset_index()
    
    # Ensure all days are present
    days_in_month = pd.Period(now.strftime('%Y-%m')).days_in_month
    all_days = pd.DataFrame({'day': range(1, days_in_month + 1)})
    daily_stats = pd.merge(all_days, daily_stats, on='day', how='left').fillna(0)
    
    title_metric = "Distance (km)"
    if metric == 'estimated_steps': title_metric = "Steps"
    elif metric == 'distance_km': title_metric = "Distance (km)"
    else: title_metric = metric.replace('_', ' ').title()
    
    fig = px.bar(
        daily_stats,
        x='day',
        y=metric,
        title=f"Daily Activity ({title_metric}) - {now.strftime('%B %Y')}",
        labels={'day': 'Day of Month', metric: title_metric},
        color_discrete_sequence=['#FC4C02']
    )
    fig.update_xaxes(dtick=1)
    fig.show()

def plot_comparison(df: pd.DataFrame, period='month'):
    """
    Compare current period vs previous period.
    Modified to show Avg/Max/Min Speed for Ride and Walk separately.
    """
    if df.empty: return

    current_date = pd.Timestamp.now()
    
    if period == 'month':
        curr_period_val = current_date.month
        curr_year = current_date.year
        prev_period_val = curr_period_val - 1 if curr_period_val > 1 else 12
        prev_year = curr_year if curr_period_val > 1 else curr_year - 1
        
        labels = ['Last Month', 'This Month']
        
        # Filter Data
        curr_data = df[(df['month'] == curr_period_val) & (df['year'] == curr_year)]
        prev_data = df[(df['month'] == prev_period_val) & (df['year'] == prev_year)]
    else:
        print("Only 'month' comparison is fully supported with these metrics.")
        return

    # Define activities to compare
    target_types = ['Ride', 'Walk']
    
    for sport in target_types:
        # Filter for sport
        curr_sport = curr_data[curr_data['type'] == sport]
        prev_sport = prev_data[prev_data['type'] == sport]
        
        if curr_sport.empty and prev_sport.empty:
            continue
            
        # Metrics: Avg Speed, Max Speed, Min Speed (Average)
        # We calculate the mean of 'average_speed_kmh' for the period, 
        # max of 'max_speed_kmh', and min of 'average_speed_kmh' (slowest ride avg)
        
        metrics = {
            'Avg Speed (km/h)': [
                prev_sport['average_speed_kmh'].mean() if not prev_sport.empty else 0,
                curr_sport['average_speed_kmh'].mean() if not curr_sport.empty else 0
            ],
            'Max Speed (km/h)': [
                prev_sport['max_speed_kmh'].max() if not prev_sport.empty else 0,
                curr_sport['max_speed_kmh'].max() if not curr_sport.empty else 0
            ],
            'Min Speed (km/h)': [
                prev_sport['average_speed_kmh'].min() if not prev_sport.empty else 0,
                curr_sport['average_speed_kmh'].min() if not curr_sport.empty else 0
            ]
        }
        
        # Create comparison dataframe
        comp_df = pd.DataFrame(metrics, index=labels).reset_index()
        comp_df = pd.melt(comp_df, id_vars=['index'], var_name='Metric', value_name='Value')
        
        fig = px.bar(
            comp_df, 
            x='index', 
            y='Value', 
            color='index', 
            facet_col='Metric', 
            title=f"Comparison ({sport}): {labels[0]} vs {labels[1]}",
            height=400,
            color_discrete_map={labels[0]: 'gray', labels[1]: '#FC4C02'}
        )
        fig.update_yaxes(matches=None, showticklabels=True)
        fig.update_xaxes(title=None)
        fig.show()


