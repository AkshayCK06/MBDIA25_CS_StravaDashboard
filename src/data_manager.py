
"""
Strava Data Management Layer
============================

This module handles the lifecycle of data within the application.
It acts as a bridge between the API, the local file cache, and the data processing layer.

What this file does:
1. Fetches activities from the Strava API via strava_api.py.
2. Caches raw data (JSON) and processed tables (CSV) to the data/ directory.
3. Loads cached data into Pandas DataFrames for analysis.
4. Manages detailed activity streams (GPS, Heart Rate) caching.

Usage:
    Run this file directly to fetch and update your data cache:
    python -m src.data_manager
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from .strava_api import StravaAPI
from .config import DATA_DIR, CACHE_DIR


class DataManager:
    """Manage fetching, caching, and loading of Strava data"""

    def __init__(self):
        self.api = StravaAPI()
        self.data_dir = DATA_DIR
        self.cache_dir = CACHE_DIR

        # File paths
        self.activities_json = self.data_dir / 'activities.json'
        self.activities_csv = self.data_dir / 'activities.csv'
        self.athlete_json = self.data_dir / 'athlete_info.json'

    def fetch_and_cache_activities(
        self,
        after: Optional[int] = None,
        limit: Optional[int] = None,
        force_refresh: bool = False
    ) -> List[Dict]:
        """
        Fetch activities from API and cache them locally

        Args:
            after: Unix timestamp to fetch activities after this time
            limit: Maximum number of activities to fetch
            force_refresh: Force refresh even if cache exists

        Returns:
            List of activity dictionaries
        """
        # Check if we have cached data
        if not force_refresh and self.activities_json.exists():
            print("Loading activities from cache...")
            return self.load_activities_from_json()

        # Fetch from API
        print("Fetching activities from Strava API...")
        activities = self.api.get_all_activities(after=after, limit=limit)

        # Cache the data
        self._save_activities_json(activities)
        self._save_activities_csv(activities)

        return activities

    def fetch_and_cache_athlete_info(self, force_refresh: bool = False) -> Dict:
        """Fetch and cache athlete information"""
        if not force_refresh and self.athlete_json.exists():
            print("Loading athlete info from cache...")
            with open(self.athlete_json, 'r') as f:
                return json.load(f)

        print("Fetching athlete info from API...")
        athlete = self.api.get_athlete()

        # Save to cache
        with open(self.athlete_json, 'w') as f:
            json.dump(athlete, f, indent=2)

        print(f"Athlete info cached to {self.athlete_json}")
        return athlete

    def _save_activities_json(self, activities: List[Dict]):
        """Save activities to JSON file"""
        with open(self.activities_json, 'w') as f:
            json.dump(activities, f, indent=2)

        print(f"Activities saved to {self.activities_json}")

    def _save_activities_csv(self, activities: List[Dict]):
        """Save activities to CSV file"""
        if not activities:
            print("No activities to save")
            return

        # Convert to DataFrame and save
        df = self._activities_to_dataframe(activities)
        df.to_csv(self.activities_csv, index=False)

        print(f"Activities saved to {self.activities_csv}")

    def load_activities_from_json(self) -> List[Dict]:
        """Load activities from JSON cache"""
        if not self.activities_json.exists():
            raise FileNotFoundError(
                f"No cached activities found at {self.activities_json}. "
                "Run fetch_and_cache_activities() first."
            )

        with open(self.activities_json, 'r') as f:
            activities = json.load(f)

        print(f"Loaded {len(activities)} activities from cache")
        return activities

    def load_activities_as_dataframe(self) -> pd.DataFrame:
        """Load activities as pandas DataFrame"""
        if self.activities_csv.exists():
            print(f"Loading activities from {self.activities_csv}")
            return pd.read_csv(self.activities_csv)

        # Fallback to JSON
        if self.activities_json.exists():
            activities = self.load_activities_from_json()
            return self._activities_to_dataframe(activities)

        raise FileNotFoundError(
            "No cached activities found. Run fetch_and_cache_activities() first."
        )

    def _activities_to_dataframe(self, activities: List[Dict]) -> pd.DataFrame:
        """Convert activities list to pandas DataFrame"""
        # Extract key fields
        data = []
        for activity in activities:
            row = {
                'id': activity.get('id'),
                'name': activity.get('name'),
                'type': activity.get('type'),
                'sport_type': activity.get('sport_type'),
                'start_date': activity.get('start_date'),
                'start_date_local': activity.get('start_date_local'),
                'distance': activity.get('distance'),  # meters
                'moving_time': activity.get('moving_time'),  # seconds
                'elapsed_time': activity.get('elapsed_time'),  # seconds
                'total_elevation_gain': activity.get('total_elevation_gain'),  # meters
                'average_speed': activity.get('average_speed'),  # m/s
                'max_speed': activity.get('max_speed'),  # m/s
                'average_heartrate': activity.get('average_heartrate'),
                'max_heartrate': activity.get('max_heartrate'),
                'average_cadence': activity.get('average_cadence'),
                'average_watts': activity.get('average_watts'),
                'kilojoules': activity.get('kilojoules'),
                'has_heartrate': activity.get('has_heartrate', False),
                'elev_high': activity.get('elev_high'),
                'elev_low': activity.get('elev_low'),
                'kudos_count': activity.get('kudos_count'),
                'achievement_count': activity.get('achievement_count'),
                'map_polyline': activity.get('map', {}).get('summary_polyline')
            }
            data.append(row)

        df = pd.DataFrame(data)

        # Convert date columns to datetime
        df['start_date'] = pd.to_datetime(df['start_date'])
        df['start_date_local'] = pd.to_datetime(df['start_date_local'])

        return df

    def fetch_activity_streams(
        self,
        activity_id: int,
        cache: bool = True
    ) -> Dict:
        """
        Fetch detailed streams for a specific activity

        Args:
            activity_id: The activity ID
            cache: Whether to cache the streams

        Returns:
            Stream data dictionary
        """
        cache_file = self.cache_dir / f'activity_{activity_id}_streams.json'

        # Check cache first
        if cache and cache_file.exists():
            print(f"Loading streams from cache for activity {activity_id}")
            with open(cache_file, 'r') as f:
                return json.load(f)

        # Fetch from API
        print(f"Fetching streams from API for activity {activity_id}")
        streams = self.api.get_activity_streams(activity_id)

        # Cache if requested
        if cache:
            with open(cache_file, 'w') as f:
                json.dump(streams, f, indent=2)
            print(f"Streams cached to {cache_file}")

        return streams

    def get_cache_info(self) -> Dict:
        """Get information about cached data"""
        info = {
            'activities_json_exists': self.activities_json.exists(),
            'activities_csv_exists': self.activities_csv.exists(),
            'athlete_info_exists': self.athlete_json.exists(),
        }

        if info['activities_json_exists']:
            with open(self.activities_json, 'r') as f:
                activities = json.load(f)
                info['num_activities'] = len(activities)
                info['last_updated'] = datetime.fromtimestamp(
                    self.activities_json.stat().st_mtime
                ).strftime('%Y-%m-%d %H:%M:%S')

        return info


if __name__ == "__main__":
    # Test data manager
    try:
        dm = DataManager()

        print("\n=== Testing Data Manager ===\n")

        # Check cache
        cache_info = dm.get_cache_info()
        print("Cache info:", cache_info)

        # Fetch athlete info
        print("\nFetching athlete info...")
        athlete = dm.fetch_and_cache_athlete_info()
        print(f"Athlete: {athlete['firstname']} {athlete['lastname']}")

        # Fetch activities
        print("\nFetching activities (limit 10 for testing)...")
        activities = dm.fetch_and_cache_activities(limit=10)
        print(f"Fetched {len(activities)} activities")

        # Load as DataFrame
        print("\nLoading as DataFrame...")
        df = dm.load_activities_as_dataframe()
        print(f"\nDataFrame shape: {df.shape}")
        print("\nColumns:", df.columns.tolist())
        print("\nFirst activity:")
        print(df.iloc[0][['name', 'type', 'distance', 'moving_time']])

        print("\nData manager test successful!")

    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure you've authenticated first:")
        print("python -m src.auth")
