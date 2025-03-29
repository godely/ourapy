"""Tests for the Oura API client."""

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

from oura_api_client.api.client import OuraClient
from oura_api_client.models.heartrate import HeartRateResponse


class TestOuraClient(unittest.TestCase):
    """Test the OuraClient class."""

    def setUp(self):
        """Set up a client for testing."""
        self.client = OuraClient("test_token")

    def test_initialization(self):
        """Test that the client initializes correctly."""
        self.assertEqual(self.client.access_token, "test_token")
        self.assertEqual(self.client.headers["Authorization"], "Bearer test_token")
        self.assertIsNotNone(self.client.heartrate)
        self.assertIsNotNone(self.client.personal)

    @patch("requests.get")
    def test_get_heart_rate(self, mock_get):
        """Test getting heart rate data."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "data": [
                {"timestamp": "2024-03-01T12:00:00+00:00", "bpm": 75, "source": "test"}
            ],
            "next_token": None,
        }
        mock_get.return_value = mock_response

        # Test with return_model=True (default)
        heart_rate = self.client.heartrate.get_heartrate(
            start_date="2024-03-01", end_date="2024-03-15"
        )

        # Assert that the response was properly converted to a model
        self.assertIsInstance(heart_rate, HeartRateResponse)
        self.assertEqual(len(heart_rate.data), 1)
        self.assertEqual(heart_rate.data[0].bpm, 75)

        # Test with return_model=False
        heart_rate_raw = self.client.heartrate.get_heartrate(
            start_date="2024-03-01", end_date="2024-03-15", return_model=False
        )

        # Assert that the raw response was returned
        self.assertIsInstance(heart_rate_raw, dict)
        self.assertIn("data", heart_rate_raw)

        # Verify the API was called with the correct parameters
        mock_get.assert_called_with(
            "https://api.ouraring.com/v2/usercollection/heartrate",
            headers=self.client.headers,
            params={"start_date": "2024-03-01", "end_date": "2024-03-15"},
        )


if __name__ == "__main__":
    unittest.main()
