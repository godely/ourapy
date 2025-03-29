import requests
from datetime import date, datetime
from typing import Optional, Dict, Any


class OuraClient:
    """A client for interacting with the Oura API v2."""

    BASE_URL = "https://api.ouraring.com/v2"

    def __init__(self, access_token: str):
        """Initialize the Oura client with an access token.

        Args:
            access_token (str): Your Oura API personal access token
        """
        self.access_token = access_token
        self.headers = {"Authorization": f"Bearer {access_token}"}

    def _make_request(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make a GET request to the Oura API.

        Args:
            endpoint (str): The API endpoint to call
            params (dict, optional): Query parameters for the request

        Returns:
            dict: The JSON response from the API

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_heart_rate(
        self, start_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get heart rate data for a specified date range.

        Args:
            start_date (str, optional): Start date in YYYY-MM-DD format
            end_date (str, optional): End date in YYYY-MM-DD format

        Returns:
            dict: Heart rate data from the API
        """
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        return self._make_request("/usercollection/heartrate", params=params)

    def get_personal_info(self) -> Dict[str, Any]:
        """Get personal information for the authenticated user.

        Returns:
            dict: Personal information from the API
        """
        return self._make_request("/usercollection/personal_info")


# Example usage:
if __name__ == "__main__":
    # Replace with your actual access token
    ACCESS_TOKEN = "your_access_token_here"

    # Initialize the client
    client = OuraClient(ACCESS_TOKEN)

    # Get heart rate data for the last week
    from datetime import datetime, timedelta

    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    try:
        heart_rate_data = client.get_heart_rate(
            start_date=start_date, end_date=end_date
        )
        print("Heart rate data:", heart_rate_data)

        personal_info = client.get_personal_info()
        print("Personal info:", personal_info)
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
