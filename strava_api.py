import requests
from datetime import datetime
from typing import List, Dict, Optional
from auth import StravaAuth
from config import STRAVA_API_BASE


class StravaAPI:
    """Interface for interacting with Strava API v3"""

    def __init__(self):
        self.auth = StravaAuth()
        self.base_url = STRAVA_API_BASE
        self.access_token = None

    def _get_headers(self):
        """Get headers with valid access token"""
        if not self.access_token:
            self.access_token = self.auth.get_valid_token()

        return {
            'Authorization': f'Bearer {self.access_token}'
        }

    def _make_request(self, endpoint: str, params: Optional[Dict] = None):
        """Make authenticated request to Strava API"""
        url = f"{self.base_url}/{endpoint}"
        headers = self._get_headers()

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        return response.json()

    def get_athlete(self):
        """Get the currently authenticated athlete"""
        return self._make_request('athlete')

    def get_athlete_stats(self, athlete_id: int):
        """Get athlete statistics"""
        return self._make_request(f'athletes/{athlete_id}/stats')

    def get_activities(
        self,
        before: Optional[int] = None,
        after: Optional[int] = None,
        page: int = 1,
        per_page: int = 30
    ) -> List[Dict]:
        """
        Get list of activities for authenticated athlete

        Args:
            before: Unix timestamp to get activities before this time
            after: Unix timestamp to get activities after this time
            page: Page number
            per_page: Number of activities per page (max 200)

        Returns:
            List of activity summaries
        """
        params = {
            'page': page,
            'per_page': min(per_page, 200)
        }

        if before:
            params['before'] = before
        if after:
            params['after'] = after

        return self._make_request('athlete/activities', params)

    def get_all_activities(
        self,
        after: Optional[int] = None,
        limit: Optional[int] = None
    ) -> List[Dict]:
        """
        Fetch all activities (handles pagination)

        Args:
            after: Unix timestamp to get activities after this time
            limit: Maximum number of activities to fetch (None for all)

        Returns:
            List of all activity summaries
        """
        all_activities = []
        page = 1
        per_page = 200

        print("Fetching activities from Strava API...")

        while True:
            activities = self.get_activities(
                after=after,
                page=page,
                per_page=per_page
            )

            if not activities:
                break

            all_activities.extend(activities)
            print(f"Fetched page {page}: {len(activities)} activities "
                  f"(Total: {len(all_activities)})")

            if limit and len(all_activities) >= limit:
                all_activities = all_activities[:limit]
                break

            if len(activities) < per_page:
                break

            page += 1

        print(f"Total activities fetched: {len(all_activities)}")
        return all_activities

    def get_activity_by_id(self, activity_id: int, include_all_efforts: bool = False):
        """
        Get detailed information about a specific activity

        Args:
            activity_id: The activity ID
            include_all_efforts: Include all segment efforts

        Returns:
            Detailed activity data
        """
        params = {'include_all_efforts': include_all_efforts}
        return self._make_request(f'activities/{activity_id}', params)

    def get_activity_streams(
        self,
        activity_id: int,
        stream_types: List[str] = None
    ):
        """
        Get streams (time-series data) for an activity

        Args:
            activity_id: The activity ID
            stream_types: List of stream types to fetch
                         (time, latlng, distance, altitude, velocity_smooth,
                          heartrate, cadence, watts, temp, moving, grade_smooth)

        Returns:
            Stream data for the activity
        """
        if stream_types is None:
            stream_types = [
                'time', 'latlng', 'distance', 'altitude',
                'velocity_smooth', 'heartrate', 'cadence', 'temp'
            ]

        stream_keys = ','.join(stream_types)
        endpoint = f'activities/{activity_id}/streams'

        params = {
            'keys': stream_keys,
            'key_by_type': True
        }

        return self._make_request(endpoint, params)

    def get_activity_zones(self, activity_id: int):
        """Get heart rate and power zones for an activity"""
        return self._make_request(f'activities/{activity_id}/zones')


if __name__ == "__main__":
    # Test the API
    try:
        api = StravaAPI()

        print("\n=== Testing Strava API ===\n")

        # Get athlete info
        athlete = api.get_athlete()
        print(f"Athlete: {athlete['firstname']} {athlete['lastname']}")
        print(f"ID: {athlete['id']}")

        # Get recent activities
        print("\nFetching recent activities...")
        activities = api.get_activities(per_page=5)

        for i, activity in enumerate(activities, 1):
            print(f"\n{i}. {activity['name']}")
            print(f"   Type: {activity['type']}")
            print(f"   Date: {activity['start_date']}")
            print(f"   Distance: {activity['distance']/1000:.2f} km")
            print(f"   Moving Time: {activity['moving_time']/60:.1f} min")

        print("\nAPI test successful!")

    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure you've run authentication first:")
        print("python auth.py")
