"""Oura API client implementation."""

import requests
from typing import Optional, Dict, Any, List
from datetime import date, datetime

from .heartrate import HeartRateEndpoints
from .personal import PersonalEndpoints
from .daily_activity import DailyActivity
from .daily_sleep import DailySleep
from .daily_readiness import DailyReadiness
from .sleep import Sleep
from .session import Session


class OuraClient:
    """Client for interacting with the Oura API v2."""

    BASE_URL = "https://api.ouraring.com/v2"

    def __init__(self, access_token: str):
        """Initialize the Oura client with an access token.

        Args:
            access_token (str): Your Oura API personal access token
        """
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        # Initialize endpoint modules
        self.heartrate = HeartRateEndpoints(self)
        self.personal = PersonalEndpoints(self)
        self.daily_activity = DailyActivity(self)
        self.daily_sleep = DailySleep(self)
        self.daily_readiness = DailyReadiness(self)
        self.sleep = Sleep(self)
        self.session = Session(self)

    def _make_request(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        method: str = "GET",
    ) -> Dict[str, Any]:
        """Make a request to the Oura API.

        Args:
            endpoint (str): The API endpoint to call
            params (dict, optional): Query parameters for the request
            method (str): HTTP method to use (default: GET)

        Returns:
            dict: The JSON response from the API

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        url = f"{self.BASE_URL}{endpoint}"

        if method.upper() == "GET":
            response = requests.get(url, headers=self.headers, params=params)
        else:
            raise ValueError(f"HTTP method {method} is not supported yet")

        response.raise_for_status()
        return response.json()
