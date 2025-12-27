"""
Strava Data Processing Logic
============================

This module contains the core analytical logic for the dashboard.
It uses Pandas to process raw activity data into meaningful insights.

What this file does:
1. Cleans and preprocesses data (converting timestamps, handling missing values).
2. Computes derived metrics (Pace, Speed in km/h, Moving Time in hours).
3. Aggregates data by week and month for trend analysis.
4. Identifies personal records (longest run, fastest ride, etc.).
5. Provides filtering utilities for date ranges and activity types.

Usage:
    Import the ActivityProcessor class to analyze a DataFrame:
    from .data_processing import ActivityProcessor
    processor = ActivityProcessor(df)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class ActivityProcessor:
    """Process and analyze Strava activity data"""

    def __init__(self, df: pd.DataFrame):
        """
        Initialize with a DataFrame of activities

        Args:
            df: DataFrame with activity data
        """
        self.df = df.copy()
        self._preprocess()

    def _preprocess(self):
        """Preprocess the DataFrame"""
        # Ensure datetime columns
        if 'start_date' in self.df.columns:
            self.df['start_date'] = pd.to_datetime(self.df['start_date'])
        if 'start_date_local' in self.df.columns:
            self.df['start_date_local'] = pd.to_datetime(self.df['start_date_local'])

        # Add computed columns
        self._add_computed_metrics()

    def _add_computed_metrics(self):
        """Add computed metrics to the DataFrame"""
        # Distance in kilometers
        if 'distance' in self.df.columns:
            self.df['distance_km'] = self.df['distance'] / 1000

        # Time in minutes and hours
        if 'moving_time' in self.df.columns:
            self.df['moving_time_min'] = self.df['moving_time'] / 60
            self.df['moving_time_hours'] = self.df['moving_time'] / 3600

        if 'elapsed_time' in self.df.columns:
            self.df['elapsed_time_min'] = self.df['elapsed_time'] / 60

        # Average pace (min/km) for running/walking
        if 'distance_km' in self.df.columns and 'moving_time_min' in self.df.columns:
            # Avoid division by zero
            self.df['pace_min_per_km'] = np.where(
                self.df['distance_km'] > 0,
                self.df['moving_time_min'] / self.df['distance_km'],
                np.nan
            )

        # Speed in km/h
        if 'average_speed' in self.df.columns:
            self.df['average_speed_kmh'] = self.df['average_speed'] * 3.6

        if 'max_speed' in self.df.columns:
            self.df['max_speed_kmh'] = self.df['max_speed'] * 3.6

        # Calculate average pace (min/km)
        # Speed is m/s. 1 m/s = 60 m/min.
        # Pace (min/km) = 1000 / (speed * 60)
        if 'average_speed' in self.df.columns:
             self.df['average_pace_min_km'] = self.df['average_speed'].apply(
                lambda x: (1000 / (x * 60)) if pd.notnull(x) and x > 0 else None
            )

        # Date components for analysis
        if 'start_date_local' in self.df.columns:
            self.df['date'] = self.df['start_date_local'].dt.date
            self.df['year'] = self.df['start_date_local'].dt.year
            self.df['month'] = self.df['start_date_local'].dt.month
            self.df['week'] = self.df['start_date_local'].dt.isocalendar().week
            self.df['day_of_week'] = self.df['start_date_local'].dt.day_name()
            self.df['hour'] = self.df['start_date_local'].dt.hour

    def get_summary_stats(self) -> Dict:
        """Get overall summary statistics"""
        stats = {
            'total_activities': len(self.df),
            'total_distance_km': self.df['distance_km'].sum() if 'distance_km' in self.df else 0,
            'total_elevation_gain_m': self.df['total_elevation_gain'].sum() if 'total_elevation_gain' in self.df else 0,
            'total_moving_time_hours': self.df['moving_time_hours'].sum() if 'moving_time_hours' in self.df else 0,
            'average_distance_km': self.df['distance_km'].mean() if 'distance_km' in self.df else 0,
            'average_speed_kmh': self.df['average_speed_kmh'].mean() if 'average_speed_kmh' in self.df else 0,
            'max_speed_kmh': self.df['average_speed_kmh'].max() if 'average_speed_kmh' in self.df else 0,
            'min_speed_kmh': self.df['average_speed_kmh'][self.df['average_speed_kmh'] > 0].min() if 'average_speed_kmh' in self.df else 0,
        }

        # Activity type breakdown
        if 'type' in self.df.columns:
            stats['activity_types'] = self.df['type'].value_counts().to_dict()

        # Date range
        if 'start_date_local' in self.df.columns:
            stats['date_range'] = {
                'earliest': self.df['start_date_local'].min().strftime('%Y-%m-%d'),
                'latest': self.df['start_date_local'].max().strftime('%Y-%m-%d')
            }

        return stats

    def get_stats_by_type(self) -> pd.DataFrame:
        """Get statistics grouped by activity type"""
        if 'type' not in self.df.columns:
            return pd.DataFrame()

        agg_dict = {}

        if 'distance_km' in self.df.columns:
            agg_dict['distance_km'] = ['count', 'sum', 'mean', 'max']

        if 'moving_time_hours' in self.df.columns:
            agg_dict['moving_time_hours'] = ['sum', 'mean']

        if 'total_elevation_gain' in self.df.columns:
            agg_dict['total_elevation_gain'] = ['sum', 'mean']

        if 'average_speed_kmh' in self.df.columns:
            agg_dict['average_speed_kmh'] = ['mean', 'max']

        if not agg_dict:
            return pd.DataFrame()

        return self.df.groupby('type').agg(agg_dict).round(2)

    def get_weekly_aggregates(self) -> pd.DataFrame:
        """Get weekly aggregated statistics"""
        if 'year' not in self.df.columns or 'week' not in self.df.columns:
            return pd.DataFrame()

        weekly = self.df.groupby(['year', 'week']).agg({
            'distance_km': 'sum',
            'moving_time_hours': 'sum',
            'total_elevation_gain': 'sum',
            'id': 'count'
        }).round(2)

        weekly.rename(columns={'id': 'num_activities'}, inplace=True)

        return weekly

    def get_monthly_aggregates(self) -> pd.DataFrame:
        """Get monthly aggregated statistics"""
        if 'year' not in self.df.columns or 'month' not in self.df.columns:
            return pd.DataFrame()

        monthly = self.df.groupby(['year', 'month']).agg({
            'distance_km': 'sum',
            'moving_time_hours': 'sum',
            'total_elevation_gain': 'sum',
            'id': 'count'
        }).round(2)

        monthly.rename(columns={'id': 'num_activities'}, inplace=True)

        return monthly

    def filter_by_type(self, activity_type: str) -> pd.DataFrame:
        """Filter activities by type"""
        if 'type' not in self.df.columns:
            return pd.DataFrame()

        return self.df[self.df['type'] == activity_type].copy()

    def filter_by_date_range(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Filter activities by date range

        Args:
            start_date: Start date in 'YYYY-MM-DD' format
            end_date: End date in 'YYYY-MM-DD' format
        """
        if 'start_date_local' not in self.df.columns:
            return pd.DataFrame()

        df_filtered = self.df.copy()

        if start_date:
            df_filtered = df_filtered[
                df_filtered['start_date_local'] >= pd.to_datetime(start_date)
            ]

        if end_date:
            df_filtered = df_filtered[
                df_filtered['start_date_local'] <= pd.to_datetime(end_date)
            ]

        return df_filtered

    def get_personal_records(self) -> Dict:
        """Find personal records"""
        records = {}

        if 'distance_km' in self.df.columns:
            max_distance_idx = self.df['distance_km'].idxmax()
            records['longest_distance'] = {
                'value': self.df.loc[max_distance_idx, 'distance_km'],
                'activity_name': self.df.loc[max_distance_idx, 'name'],
                'date': self.df.loc[max_distance_idx, 'start_date_local'].strftime('%Y-%m-%d')
            }

        if 'total_elevation_gain' in self.df.columns:
            max_elevation_idx = self.df['total_elevation_gain'].idxmax()
            records['highest_elevation_gain'] = {
                'value': self.df.loc[max_elevation_idx, 'total_elevation_gain'],
                'activity_name': self.df.loc[max_elevation_idx, 'name'],
                'date': self.df.loc[max_elevation_idx, 'start_date_local'].strftime('%Y-%m-%d')
            }

        if 'moving_time_hours' in self.df.columns:
            max_time_idx = self.df['moving_time_hours'].idxmax()
            records['longest_time'] = {
                'value': self.df.loc[max_time_idx, 'moving_time_hours'],
                'activity_name': self.df.loc[max_time_idx, 'name'],
                'date': self.df.loc[max_time_idx, 'start_date_local'].strftime('%Y-%m-%d')
            }

        if 'average_speed_kmh' in self.df.columns:
            max_speed_idx = self.df['average_speed_kmh'].idxmax()
            records['highest_average_speed'] = {
                'value': self.df.loc[max_speed_idx, 'average_speed_kmh'],
                'activity_name': self.df.loc[max_speed_idx, 'name'],
                'date': self.df.loc[max_speed_idx, 'start_date_local'].strftime('%Y-%m-%d')
            }

        return records

    def get_activity_by_day_of_week(self) -> pd.DataFrame:
        """Get activity counts and totals by day of week"""
        if 'day_of_week' not in self.df.columns:
            return pd.DataFrame()

        # Define day order
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        by_day = self.df.groupby('day_of_week').agg({
            'id': 'count',
            'distance_km': 'sum',
            'moving_time_hours': 'sum'
        }).round(2)

        by_day.rename(columns={'id': 'num_activities'}, inplace=True)

        # Reorder by day of week
        by_day = by_day.reindex(day_order)

        return by_day


if __name__ == "__main__":
    # Test with sample data
    try:
        from .data_manager import DataManager
    except ImportError:
        from data_manager import DataManager

    try:
        dm = DataManager()
        df = dm.load_activities_as_dataframe()

        print("\n=== Testing Activity Processor ===\n")

        processor = ActivityProcessor(df)

        # Summary stats
        print("Summary Statistics:")
        stats = processor.get_summary_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")

        # Stats by type
        print("\n\nStatistics by Activity Type:")
        print(processor.get_stats_by_type())

        # Personal records
        print("\n\nPersonal Records:")
        records = processor.get_personal_records()
        for record_name, record_data in records.items():
            print(f"\n  {record_name}:")
            for key, value in record_data.items():
                print(f"    {key}: {value}")

        print("\n\nProcessor test successful!")

    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure you have cached data first:")
        print("python -m src.data_manager")
