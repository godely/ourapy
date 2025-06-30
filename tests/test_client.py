"""Tests for the Oura API client."""

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, date

from oura_api_client.api.client import OuraClient
from oura_api_client.models.heartrate import HeartRateResponse
from oura_api_client.models.daily_activity import (
    DailyActivityResponse, DailyActivityModel, ActivityContributors
)
from oura_api_client.models.daily_sleep import (
    DailySleepResponse, DailySleepModel, SleepContributors as DailySleepContributors
)
from oura_api_client.models.daily_readiness import (
    DailyReadinessResponse, DailyReadinessModel, ReadinessContributors as DailyReadinessContributors
)
from oura_api_client.models.sleep import SleepResponse, SleepModel, SleepContributors, ReadinessContributors
from oura_api_client.models.session import SessionResponse, SessionModel
from oura_api_client.models.tag import TagResponse, TagModel
from oura_api_client.models.workout import WorkoutResponse, WorkoutModel
from oura_api_client.models.enhanced_tag import (
    EnhancedTagResponse, EnhancedTagModel
)
from oura_api_client.models.daily_spo2 import (
    DailySpO2Response, DailySpO2Model, DailySpO2AggregatedValuesModel
)
from oura_api_client.models.sleep_time import (
    SleepTimeResponse, SleepTimeModel, SleepTimeWindow,
    SleepTimeRecommendation, SleepTimeStatus
)
from oura_api_client.models.rest_mode_period import (
    RestModePeriodResponse, RestModePeriodModel
)  # Added RestModePeriod models
from oura_api_client.models.daily_stress import (
    DailyStressResponse, DailyStressModel
)  # Added DailyStress models
from oura_api_client.models.daily_resilience import (
    DailyResilienceResponse, DailyResilienceModel
)  # Added DailyResilience models
from oura_api_client.models.daily_cardiovascular_age import (
    DailyCardiovascularAgeResponse, DailyCardiovascularAgeModel
)  # Added DailyCardiovascularAge models
from oura_api_client.models.vo2_max import (
    Vo2MaxResponse, Vo2MaxModel
)  # Added Vo2Max models
from oura_api_client.models.ring_configuration import (
    RingConfigurationResponse, RingConfigurationModel
)  # Added RingConfiguration models
from oura_api_client.models.personal import (
    PersonalInfo
)  # Added Personal models
import requests

from oura_api_client.exceptions import (
    OuraNotFoundError, OuraRateLimitError,
    OuraClientError, OuraConnectionError
)

class TestOuraClient(unittest.TestCase):
    """Test the OuraClient class."""

    def setUp(self):
        """Set up a client for testing."""
        self.client = OuraClient("test_token")

    def test_initialization(self):
        """Test that the client initializes correctly."""
        self.assertEqual(self.client.access_token, "test_token")
        self.assertEqual(
            self.client.headers["Authorization"], "Bearer test_token"
        )
        self.assertIsNotNone(self.client.heartrate)
        self.assertIsNotNone(self.client.personal)
        self.assertIsNotNone(self.client.daily_activity)
        self.assertIsNotNone(self.client.daily_sleep)
        self.assertIsNotNone(self.client.daily_readiness)
        self.assertIsNotNone(self.client.sleep)
        self.assertIsNotNone(self.client.session)
        self.assertIsNotNone(self.client.tag)
        self.assertIsNotNone(self.client.workout)
        self.assertIsNotNone(self.client.enhanced_tag)
        self.assertIsNotNone(self.client.daily_spo2)
        self.assertIsNotNone(self.client.sleep_time)
        # Added rest_mode_period
        self.assertIsNotNone(self.client.rest_mode_period)
        # Added daily_stress
        self.assertIsNotNone(self.client.daily_stress)
        # Added daily_resilience
        self.assertIsNotNone(self.client.daily_resilience)
        # Added daily_cardiovascular_age
        self.assertIsNotNone(self.client.daily_cardiovascular_age)
        # Added vo2_max
        self.assertIsNotNone(self.client.vo2_max)
        # Added ring_configuration
        self.assertIsNotNone(self.client.ring_configuration)

    @patch("requests.get")
    def test_get_heart_rate(self, mock_get):
        """Test getting heart rate data."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "data": [
                {
                    "timestamp": "2024-03-01T12:00:00+00:00",
                    "bpm": 75,
                    "source": "test"
                }
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
            timeout=30.0,
        )

if __name__ == "__main__":
    unittest.main()

class TestDailyActivity(unittest.TestCase):
    def setUp(self):

        self.client = OuraClient(access_token="test_token")

    @patch("requests.get")
    def test_get_daily_activity_documents(self, mock_get):
        mock_data = [
            {
                "id": "test_id_1",
                "day": "2024-03-10",
                "timestamp": "2024-03-10T00:00:00+00:00",
            },
            {
                "id": "test_id_2",
                "day": "2024-03-11",
                "timestamp": "2024-03-11T00:00:00+00:00",
            },
        ]
        mock_response_json = {
            "data": mock_data,
            "next_token": "test_next_token"
        }
        # Configure the mock_get object to simulate a successful response
        mock_response = MagicMock()
        # Simulate no HTTP error
        mock_response.raise_for_status.return_value = None
        # Set the JSON response
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        start_date_str = "2024-03-10"
        end_date_str = "2024-03-11"
        start_date = date.fromisoformat(start_date_str)
        end_date = date.fromisoformat(end_date_str)

        daily_activity_response = (
            self.client.daily_activity.get_daily_activity_documents(
                start_date=start_date,
                end_date=end_date,
                next_token="test_token"
            )
        )

        self.assertIsInstance(daily_activity_response, DailyActivityResponse)
        self.assertEqual(len(daily_activity_response.data), 2)
        self.assertIsInstance(
            daily_activity_response.data[0], DailyActivityModel
        )
        self.assertEqual(
            daily_activity_response.next_token, "test_next_token"
        )
        # Use self.client.client._make_request for assertion
        # if client.get is not available
        actual_call_url = mock_get.call_args[0][0]
        base_url = self.client.BASE_URL
        expected_url = f"{base_url}/usercollection/daily_activity"
        self.assertTrue(actual_call_url.endswith(expected_url))

        called_params = mock_get.call_args[1]['params']
        expected_params = {
            "start_date": start_date_str,
            "end_date": end_date_str,
            "next_token": "test_token",
        }
        self.assertEqual(called_params, expected_params)

    @patch("requests.get")
    def test_get_daily_activity_documents_with_string_dates(self, mock_get):
        mock_data = [
            {
                "id": "test_id_1",
                "day": "2024-03-10",
                "timestamp": "2024-03-10T00:00:00+00:00",
            }
        ]
        mock_response_json = {"data": mock_data, "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        start_date_str = "2024-03-10"
        end_date_str = "2024-03-11"

        self.client.daily_activity.get_daily_activity_documents(
            start_date=start_date_str, end_date=end_date_str
        )
        actual_call_url = mock_get.call_args[0][0]
        base_url = self.client.BASE_URL
        expected_url = f"{base_url}/usercollection/daily_activity"
        self.assertTrue(actual_call_url.endswith(expected_url))

        called_params = mock_get.call_args[1]['params']
        expected_params = {"start_date": start_date_str, "end_date": end_date_str}
        self.assertEqual(called_params, expected_params)

    @patch("requests.get")
    def test_get_daily_activity_documents_error(self, mock_get):
        mock_get.side_effect = OuraConnectionError("API error")
        with self.assertRaises(OuraConnectionError):
            self.client.daily_activity.get_daily_activity_documents(
                start_date="2024-03-10", end_date="2024-03-11"
            )

    @patch("requests.get")
    def test_get_daily_activity_document(self, mock_get):
        mock_response_json = {
            "id": "test_document_id",
            "class_5_min": "test_class_5_min",
            "score": 80,
            "active_calories": 500,
            "average_met_minutes": 2.5,
            "contributors": {
                "meet_daily_targets": 1,
                "move_every_hour": 1,
                "recovery_time": 1,
                "stay_active": 1,
                "training_frequency": 1,
                "training_volume": 1,
            },
            "equivalent_walking_distance": 5000,
            "high_activity_met_minutes": 30,
            "high_activity_time": 600,
            "inactivity_alerts": 2,
            "low_activity_met_minutes": 60,
            "low_activity_time": 1200,
            "medium_activity_met_minutes": 90,
            "medium_activity_time": 1800,
            "met": {
                "interval": 5,
                "items": [1.5, 2.0, 1.8, 2.2],
                "timestamp": "2024-03-10T12:00:00+00:00"
            },
            "meters_to_target": 1000,
            "non_wear_time": 300,
            "resting_time": 3600,
            "sedentary_met_minutes": 120,
            "sedentary_time": 2400,
            "steps": 10000,
            "target_calories": 600,
            "target_meters": 6000,
            "total_calories": 2500,
            "day": "2024-03-10",
            "timestamp": "2024-03-10T12:00:00+00:00",
        }
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        document_id = "test_document_id"
        daily_activity_document = self.client.daily_activity.get_daily_activity_document(
            document_id=document_id
        )

        self.assertIsInstance(daily_activity_document, DailyActivityModel)
        self.assertEqual(daily_activity_document.id, document_id)
        self.assertIsInstance(daily_activity_document.contributors, ActivityContributors)

        actual_call_url = mock_get.call_args[0][0]
        base_url = self.client.BASE_URL
        expected_url = f"{base_url}/usercollection/daily_activity/{document_id}"
        self.assertTrue(actual_call_url.endswith(expected_url))

        called_params = mock_get.call_args[1]['params']
        self.assertEqual(called_params, None)

    @patch("requests.get")
    def test_get_daily_activity_document_error(self, mock_get):
        mock_get.side_effect = OuraConnectionError("API error")
        document_id = "test_document_id"
        with self.assertRaises(OuraConnectionError):
            self.client.daily_activity.get_daily_activity_document(document_id=document_id)

class TestDailySleep(unittest.TestCase):
    def setUp(self):

        self.client = OuraClient(access_token="test_token")

    @patch("requests.get")
    def test_get_daily_sleep_documents(self, mock_get):
        mock_data = [
            {
                "id": "sleep_id_1",
                "contributors": {
                    "deep_sleep": 70,
                    "efficiency": 80,
                    "latency": 90,
                    "rem_sleep": 60,
                    "restfulness": 75,
                    "timing": 85,
                    "total_sleep": 95,
                },
                "day": "2024-03-10",
                "timestamp": "2024-03-10T22:00:00+00:00",
            },
            {
                "id": "sleep_id_2",
                "contributors": {
                    "deep_sleep": 75,
                    "efficiency": 85,
                    "latency": 95,
                    "rem_sleep": 65,
                    "restfulness": 80,
                    "timing": 90,
                    "total_sleep": 100,
                },
                "day": "2024-03-11",
                "timestamp": "2024-03-11T22:00:00+00:00",
            },
        ]
        mock_response_json = {"data": mock_data, "next_token": "next_sleep_token"}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        start_date_str = "2024-03-10"
        end_date_str = "2024-03-11"
        start_date = date.fromisoformat(start_date_str)
        end_date = date.fromisoformat(end_date_str)

        daily_sleep_response = (
            self.client.daily_sleep.get_daily_sleep_documents(
                start_date=start_date,
                end_date=end_date,
                next_token="test_sleep_token"
            )
        )

        self.assertIsInstance(daily_sleep_response, DailySleepResponse)
        self.assertEqual(len(daily_sleep_response.data), 2)
        self.assertIsInstance(daily_sleep_response.data[0], DailySleepModel)
        self.assertIsInstance(
            daily_sleep_response.data[0].contributors,
            DailySleepContributors
        )
        self.assertEqual(daily_sleep_response.next_token, "next_sleep_token")

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/daily_sleep",
            headers=self.client.headers,
            params={
                "start_date": start_date_str,
                "end_date": end_date_str,
                "next_token": "test_sleep_token",
            },
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_sleep_documents_with_string_dates(self, mock_get):
        mock_data = [
            {
                "id": "sleep_id_1",
                "contributors": {"deep_sleep": 70},
                "day": "2024-03-10",
                "timestamp": "2024-03-10T22:00:00+00:00",
            }
        ]
        mock_response_json = {"data": mock_data, "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        start_date_str = "2024-03-10"
        end_date_str = "2024-03-11"

        self.client.daily_sleep.get_daily_sleep_documents(
            start_date=start_date_str, end_date=end_date_str
        )

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/daily_sleep",
            headers=self.client.headers,
            params={"start_date": start_date_str, "end_date": end_date_str},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_sleep_documents_error(self, mock_get):
        mock_get.side_effect = OuraConnectionError("API error")
        with self.assertRaises(OuraConnectionError):
            self.client.daily_sleep.get_daily_sleep_documents(
                start_date="2024-03-10", end_date="2024-03-11"
            )

    @patch("requests.get")
    def test_get_daily_sleep_document(self, mock_get):
        mock_response_json = {
            "id": "test_sleep_document_id",
            "contributors": {
                "deep_sleep": 70,
                "efficiency": 80,
                "latency": 90,
                "rem_sleep": 60,
                "restfulness": 75,
                "timing": 85,
                "total_sleep": 95,
            },
            "day": "2024-03-10",
            "timestamp": "2024-03-10T22:00:00+00:00",
            "score": 85,
            "bedtime_end": "2024-03-11T07:00:00+00:00",
            "bedtime_start": "2024-03-10T22:00:00+00:00",
            "type": "main_sleep",
        }
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        document_id = "test_sleep_document_id"
        daily_sleep_document = self.client.daily_sleep.get_daily_sleep_document(
            document_id=document_id
        )

        self.assertIsInstance(daily_sleep_document, DailySleepModel)
        self.assertEqual(daily_sleep_document.id, document_id)
        self.assertIsInstance(
            daily_sleep_document.contributors, DailySleepContributors
        )
        self.assertEqual(daily_sleep_document.score, 85)
        self.assertEqual(
            daily_sleep_document.bedtime_end,
            datetime.fromisoformat("2024-03-11T07:00:00+00:00")
        )
        self.assertEqual(
            daily_sleep_document.bedtime_start,
            datetime.fromisoformat("2024-03-10T22:00:00+00:00")
        )

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/daily_sleep/{document_id}",
            headers=self.client.headers,
            params=None,
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_sleep_document_error(self, mock_get):
        mock_get.side_effect = OuraConnectionError("API error")
        document_id = "test_sleep_document_id"
        with self.assertRaises(OuraConnectionError):
            self.client.daily_sleep.get_daily_sleep_document(document_id=document_id)

class TestDailyReadiness(unittest.TestCase):
    def setUp(self):

        self.client = OuraClient(access_token="test_token")

    @patch("requests.get")
    def test_get_daily_readiness_documents(self, mock_get):
        mock_data = [
            {
                "id": "readiness_id_1",
                "contributors": {"activity_balance": 60, "body_temperature": 70},
                "day": "2024-03-10",
                "score": 75,
                "timestamp": "2024-03-10T00:00:00+00:00",
            },
            {
                "id": "readiness_id_2",
                "contributors": {"activity_balance": 65, "body_temperature": 75},
                "day": "2024-03-11",
                "score": 80,
                "timestamp": "2024-03-11T00:00:00+00:00",
            },
        ]
        mock_response_json = {"data": mock_data, "next_token": "next_readiness_token"}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        start_date_str = "2024-03-10"
        end_date_str = "2024-03-11"
        start_date = date.fromisoformat(start_date_str)
        end_date = date.fromisoformat(end_date_str)

        daily_readiness_response = (
            self.client.daily_readiness.get_daily_readiness_documents(
                start_date=start_date,
                end_date=end_date,
                next_token="test_readiness_token"
            )
        )

        self.assertIsInstance(daily_readiness_response, DailyReadinessResponse)
        self.assertEqual(len(daily_readiness_response.data), 2)
        self.assertIsInstance(
            daily_readiness_response.data[0], DailyReadinessModel
        )
        self.assertIsInstance(
            daily_readiness_response.data[0].contributors,
            DailyReadinessContributors
        )
        self.assertEqual(
            daily_readiness_response.next_token, "next_readiness_token"
        )

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/daily_readiness",
            headers=self.client.headers,
            params={
                "start_date": start_date_str,
                "end_date": end_date_str,
                "next_token": "test_readiness_token",
            },
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_readiness_documents_with_string_dates(self, mock_get):
        mock_data = [
            {
                "id": "readiness_id_1",
                "contributors": {"activity_balance": 60},
                "day": "2024-03-10",
                "score": 75,
                "timestamp": "2024-03-10T00:00:00+00:00",
            }
        ]
        mock_response_json = {"data": mock_data, "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        start_date_str = "2024-03-10"
        end_date_str = "2024-03-11"

        self.client.daily_readiness.get_daily_readiness_documents(
            start_date=start_date_str, end_date=end_date_str
        )

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/daily_readiness",
            headers=self.client.headers,
            params={"start_date": start_date_str, "end_date": end_date_str},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_readiness_documents_error(self, mock_get):
        mock_get.side_effect = OuraConnectionError("API error")
        with self.assertRaises(OuraConnectionError):
            self.client.daily_readiness.get_daily_readiness_documents(
                start_date="2024-03-10", end_date="2024-03-11"
            )

    @patch("requests.get")
    def test_get_daily_readiness_document(self, mock_get):
        mock_response_json = {
            "id": "test_readiness_document_id",
            "contributors": {
                "activity_balance": 60,
                "body_temperature": 70,
                "hrv_balance": 80,
                "previous_day_activity": 90,
                "previous_night": 50,
                "recovery_index": 65,
                "resting_heart_rate": 75,
                "sleep_balance": 85,
            },
            "day": "2024-03-10",
            "score": 78,
            "temperature_trend_deviation": 0.1,
            "timestamp": "2024-03-10T00:00:00+00:00",
            "activity_class_5_min": "some_activity_class",  # New field
            "hrv_balance_data": "some_hrv_data",  # New field
            "spo2_percentage": 98.5,  # New field
        }
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        document_id = "test_readiness_document_id"
        daily_readiness_document = (
            self.client.daily_readiness.get_daily_readiness_document(
                document_id=document_id
            )
        )

        self.assertIsInstance(daily_readiness_document, DailyReadinessModel)
        self.assertEqual(daily_readiness_document.id, document_id)
        self.assertIsInstance(
            daily_readiness_document.contributors,
            DailyReadinessContributors
        )
        self.assertEqual(daily_readiness_document.score, 78)
        self.assertEqual(
            daily_readiness_document.activity_class_5_min,
            "some_activity_class"
        )
        self.assertEqual(daily_readiness_document.hrv_balance_data, "some_hrv_data")
        self.assertEqual(daily_readiness_document.spo2_percentage, 98.5)

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/daily_readiness/{document_id}",
            headers=self.client.headers,
            params=None,
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_readiness_document_error(self, mock_get):
        mock_get.side_effect = OuraConnectionError("API error")
        document_id = "test_readiness_document_id"
        with self.assertRaises(OuraConnectionError):
            self.client.daily_readiness.get_daily_readiness_document(
                document_id=document_id
            )

class TestSleep(unittest.TestCase):
    def setUp(self):

        self.client = OuraClient(access_token="test_token")

    @patch("requests.get")
    def test_get_sleep_documents(self, mock_get):
        # Reused from DailySleep for consistency
        mock_contributors_data = {
            "deep_sleep": 70, "efficiency": 80,
            "latency": 90, "rem_sleep": 60,
            "restfulness": 75, "timing": 85, "total_sleep": 95,
        }
        # Reused from DailyReadiness
        mock_readiness_contributors_data = {
            "activity_balance": 60, "body_temperature": 70,
            "hrv_balance": 80,
            "previous_day_activity": 90, "previous_night": 50,
            "recovery_index": 65,
            "resting_heart_rate": 75, "sleep_balance": 85,
        }
        mock_data = [
            {
                "id": "sleep_doc_1",
                "average_breath": 14.5,
                "average_heart_rate": 58.0,
                "average_hrv": 65,
                "awake_time": 3600,
                "bedtime_end": "2024-03-11T07:00:00+00:00",
                "bedtime_start": "2024-03-10T22:00:00+00:00",
                "day": "2024-03-10",
                "deep_sleep_duration": 7200,
                "efficiency": 90,
                "latency": 600,
                "light_sleep_duration": 18000,
                "period": 1,
                "readiness": mock_readiness_contributors_data,  # Nested model
                "rem_sleep_duration": 3600,
                "score": 85,
                "contributors": mock_contributors_data,  # Nested SleepContributors
                "type": "main_sleep",
                "timestamp": "2024-03-10T22:00:00+00:00",  # Added timestamp for SleepModel
            },
        ]
        mock_response_json = {
            "data": mock_data,
            "next_token": "next_sleep_doc_token"
        }
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        start_date_str = "2024-03-10"
        end_date_str = "2024-03-11"
        start_date = date.fromisoformat(start_date_str)
        end_date = date.fromisoformat(end_date_str)

        sleep_response = self.client.sleep.get_sleep_documents(
            start_date=start_date,
            end_date=end_date,
            next_token="test_sleep_doc_token"
        )

        self.assertIsInstance(sleep_response, SleepResponse)
        self.assertEqual(len(sleep_response.data), 1)
        self.assertIsInstance(sleep_response.data[0], SleepModel)
        self.assertIsInstance(

            sleep_response.data[0].contributors,
            SleepContributors

        )
        self.assertIsInstance(
            sleep_response.data[0].readiness, ReadinessContributors
        )
        self.assertEqual(sleep_response.next_token, "next_sleep_doc_token")

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/sleep",
            headers=self.client.headers,
            params={
                "start_date": start_date_str,
                "end_date": end_date_str,
                "next_token": "test_sleep_doc_token",
            },
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_sleep_documents_with_string_dates(self, mock_get):
        # Simplified mock data for this test
        mock_data = [{
            "id": "sleep_doc_str_date",
            "day": "2024-03-10",
            "contributors": {"deep_sleep": 1},
            "timestamp": "2024-03-10T22:00:00+00:00"
        }]
        mock_response_json = {"data": mock_data, "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        start_date_str = "2024-03-10"
        end_date_str = "2024-03-11"

        self.client.sleep.get_sleep_documents(
            start_date=start_date_str, end_date=end_date_str
        )

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/sleep",
            headers=self.client.headers,
            params={"start_date": start_date_str, "end_date": end_date_str},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_sleep_documents_error(self, mock_get):
        mock_get.side_effect = OuraConnectionError("API error")
        with self.assertRaises(OuraConnectionError):
            self.client.sleep.get_sleep_documents(
                start_date="2024-03-10", end_date="2024-03-11"
            )

    @patch("requests.get")
    def test_get_sleep_document(self, mock_get):
        mock_contributors_data = {"deep_sleep": 70}
        mock_readiness_contributors_data = {"activity_balance": 60}
        mock_response_json = {
            "id": "test_sleep_doc_single",
            "average_breath": 14.2,
            "day": "2024-03-10",
            "bedtime_end": "2024-03-11T07:30:00+00:00",
            "bedtime_start": "2024-03-10T22:15:00+00:00",
            "contributors": mock_contributors_data,
            "readiness": mock_readiness_contributors_data,
            "score": 88,
            "type": "main_sleep",
            "timestamp": "2024-03-10T22:15:00+00:00",
        }
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        document_id = "test_sleep_doc_single"
        sleep_document = self.client.sleep.get_sleep_document(
            document_id=document_id
        )

        self.assertIsInstance(sleep_document, SleepModel)
        self.assertEqual(sleep_document.id, document_id)
        self.assertIsInstance(sleep_document.contributors, SleepContributors)
        self.assertIsInstance(sleep_document.readiness, ReadinessContributors)
        self.assertEqual(sleep_document.score, 88)
        self.assertEqual(
            sleep_document.bedtime_end,
            datetime.fromisoformat("2024-03-11T07:30:00+00:00")
        )

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/sleep/{document_id}",
            headers=self.client.headers,
            params=None,
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_sleep_document_error(self, mock_get):
        mock_get.side_effect = OuraConnectionError("API error")
        document_id = "test_sleep_doc_single_error"
        with self.assertRaises(OuraConnectionError):
            self.client.sleep.get_sleep_document(document_id=document_id)

class TestSession(unittest.TestCase):
    def setUp(self):

        self.client = OuraClient(access_token="test_token")

    @patch("requests.get")
    def test_get_session_documents(self, mock_get):
        mock_data = [
            {
                "id": "session_doc_1",
                "day": "2024-03-10",
                "start_datetime": "2024-03-10T10:00:00+00:00",
                "end_datetime": "2024-03-10T10:30:00+00:00",
                "type": "meditation",
                "mood": "good",
                "duration": 1800,
            },
            {
                "id": "session_doc_2",
                "day": "2024-03-11",
                "start_datetime": "2024-03-11T14:00:00+00:00",
                "end_datetime": "2024-03-11T14:20:00+00:00",
                "type": "nap",
                "duration": 1200,
            },
        ]
        mock_response_json = {"data": mock_data, "next_token": "next_session_token"}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        start_date_str = "2024-03-10"
        end_date_str = "2024-03-11"
        start_date = date.fromisoformat(start_date_str)
        end_date = date.fromisoformat(end_date_str)

        session_response = self.client.session.get_session_documents(
            start_date=start_date,
            end_date=end_date,
            next_token="test_session_token"
        )

        self.assertIsInstance(session_response, SessionResponse)
        self.assertEqual(len(session_response.data), 2)
        self.assertIsInstance(session_response.data[0], SessionModel)
        self.assertEqual(session_response.next_token, "next_session_token")

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/session",
            headers=self.client.headers,
            params={
                "start_date": start_date_str,
                "end_date": end_date_str,
                "next_token": "test_session_token",
            },
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_session_documents_with_string_dates(self, mock_get):
        mock_data = [
            {
                "id": "session_doc_str",
                "day": "2024-03-10",
                "start_datetime": "2024-03-10T10:00:00+00:00",
                "end_datetime": "2024-03-10T10:30:00+00:00",
                "type": "meditation",
            }
        ]
        mock_response_json = {"data": mock_data, "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        start_date_str = "2024-03-10"
        end_date_str = "2024-03-11"

        self.client.session.get_session_documents(
            start_date=start_date_str, end_date=end_date_str
        )

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/session",
            headers=self.client.headers,
            params={"start_date": start_date_str, "end_date": end_date_str},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_session_documents_error(self, mock_get):
        mock_get.side_effect = OuraConnectionError("API error")
        with self.assertRaises(OuraConnectionError):
            self.client.session.get_session_documents(
                start_date="2024-03-10", end_date="2024-03-11"
            )

    @patch("requests.get")
    def test_get_session_document(self, mock_get):
        mock_response_json = {
            "id": "test_session_single",
            "day": "2024-03-10",
            "start_datetime": "2024-03-10T15:00:00+00:00",
            "end_datetime": "2024-03-10T15:45:00+00:00",
            "type": "workout",
            "mood": "great",
            "duration": 2700,
            "energy": 250.0,
            "stress": 10.5,
        }
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        document_id = "test_session_single"
        session_document = self.client.session.get_session_document(
            document_id=document_id
        )

        self.assertIsInstance(session_document, SessionModel)
        self.assertEqual(session_document.id, document_id)
        self.assertEqual(session_document.type, "workout")
        self.assertEqual(session_document.mood, "great")
        self.assertEqual(session_document.duration, 2700)
        self.assertEqual(
            session_document.start_datetime,
            datetime.fromisoformat("2024-03-10T15:00:00+00:00")
        )

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/session/{document_id}",
            headers=self.client.headers,
            params=None,
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_session_document_error(self, mock_get):
        mock_get.side_effect = OuraConnectionError("API error")
        document_id = "test_session_single_error"
        with self.assertRaises(OuraConnectionError):
            self.client.session.get_session_document(document_id=document_id)

class TestTag(unittest.TestCase):
    def setUp(self):

        self.client = OuraClient(access_token="test_token")

    @patch("requests.get")
    def test_get_tag_documents(self, mock_get):
        mock_data = [
            {
                "id": "tag_doc_1",
                "day": "2024-03-10",
                "text": "Morning workout",
                "timestamp": "2024-03-10T09:00:00+00:00",
            },
            {
                "id": "tag_doc_2",
                "day": "2024-03-11",
                "text": "Big presentation",
                "timestamp": "2024-03-11T14:00:00+00:00",
            },
        ]
        mock_response_json = {"data": mock_data, "next_token": "next_tag_token"}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        start_date_str = "2024-03-10"
        end_date_str = "2024-03-11"
        start_date = date.fromisoformat(start_date_str)
        end_date = date.fromisoformat(end_date_str)

        tag_response = self.client.tag.get_tag_documents(
            start_date=start_date,
            end_date=end_date,
            next_token="test_tag_token"
        )

        self.assertIsInstance(tag_response, TagResponse)
        self.assertEqual(len(tag_response.data), 2)
        self.assertIsInstance(tag_response.data[0], TagModel)
        self.assertEqual(tag_response.next_token, "next_tag_token")

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/tag",
            headers=self.client.headers,
            params={
                "start_date": start_date_str,
                "end_date": end_date_str,
                "next_token": "test_tag_token",
            },
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_tag_documents_with_string_dates(self, mock_get):
        mock_data = [
            {
                "id": "tag_doc_str",
                "day": "2024-03-10",
                "text": "String date test",
                "timestamp": "2024-03-10T09:00:00+00:00",
            }
        ]
        mock_response_json = {"data": mock_data, "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        start_date_str = "2024-03-10"
        end_date_str = "2024-03-11"

        self.client.tag.get_tag_documents(
            start_date=start_date_str, end_date=end_date_str
        )

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/tag",
            headers=self.client.headers,
            params={"start_date": start_date_str, "end_date": end_date_str},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_tag_documents_error(self, mock_get):
        mock_get.side_effect = OuraConnectionError("API error")
        with self.assertRaises(OuraConnectionError):
            self.client.tag.get_tag_documents(
                start_date="2024-03-10", end_date="2024-03-11"
            )

    @patch("requests.get")
    def test_get_tag_document(self, mock_get):
        mock_response_json = {
            "id": "test_tag_single",
            "day": "2024-03-10",
            "text": "Single tag test",
            "timestamp": "2024-03-10T11:00:00+00:00",
        }
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        document_id = "test_tag_single"
        tag_document = self.client.tag.get_tag_document(
            document_id=document_id
        )

        self.assertIsInstance(tag_document, TagModel)
        self.assertEqual(tag_document.id, document_id)
        self.assertEqual(tag_document.text, "Single tag test")
        self.assertEqual(
            tag_document.timestamp,
            datetime.fromisoformat("2024-03-10T11:00:00+00:00")
        )

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/tag/{document_id}",
            headers=self.client.headers,
            params=None,
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_tag_document_error(self, mock_get):
        mock_get.side_effect = OuraConnectionError("API error")
        document_id = "test_tag_single_error"
        with self.assertRaises(OuraConnectionError):
            self.client.tag.get_tag_document(document_id=document_id)

class TestWorkout(unittest.TestCase):
    def setUp(self):

        self.client = OuraClient(access_token="test_token")

    @patch("requests.get")
    def test_get_workout_documents(self, mock_get):
        mock_data = [
            {
                "id": "workout_doc_1",
                "activity": "running",
                "calories": 300.5,
                "day": "2024-03-10",
                "distance": 5000.0,
                "end_datetime": "2024-03-10T08:30:00+00:00",
                "intensity": "moderate",
                "source": "manual",
                "start_datetime": "2024-03-10T08:00:00+00:00",
            },
            {
                "id": "workout_doc_2",
                "activity": "yoga",
                "day": "2024-03-11",
                "end_datetime": "2024-03-11T17:00:00+00:00",
                "intensity": "easy",
                "source": "oura_app",
                "start_datetime": "2024-03-11T16:00:00+00:00",
            },
        ]
        mock_response_json = {"data": mock_data, "next_token": "next_workout_token"}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        start_date_str = "2024-03-10"
        end_date_str = "2024-03-11"
        start_date = date.fromisoformat(start_date_str)
        end_date = date.fromisoformat(end_date_str)

        workout_response = self.client.workout.get_workout_documents(
            start_date=start_date,
            end_date=end_date,
            next_token="test_workout_token"
        )

        self.assertIsInstance(workout_response, WorkoutResponse)
        self.assertEqual(len(workout_response.data), 2)
        self.assertIsInstance(workout_response.data[0], WorkoutModel)
        self.assertEqual(workout_response.next_token, "next_workout_token")

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/workout",
            headers=self.client.headers,
            params={
                "start_date": start_date_str,
                "end_date": end_date_str,
                "next_token": "test_workout_token",
            },
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_workout_documents_with_string_dates(self, mock_get):
        mock_data = [
            {
                "id": "workout_doc_str",
                "activity": "cycling",
                "day": "2024-03-10",
                "end_datetime": "2024-03-10T18:00:00+00:00",
                "intensity": "hard",
                "source": "strava",
                "start_datetime": "2024-03-10T17:00:00+00:00",
            }
        ]
        mock_response_json = {"data": mock_data, "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        start_date_str = "2024-03-10"
        end_date_str = "2024-03-11"

        self.client.workout.get_workout_documents(
            start_date=start_date_str, end_date=end_date_str
        )

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/workout",
            headers=self.client.headers,
            params={"start_date": start_date_str, "end_date": end_date_str},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_workout_documents_error(self, mock_get):
        mock_get.side_effect = OuraConnectionError("API error")
        with self.assertRaises(OuraConnectionError):
            self.client.workout.get_workout_documents(
                start_date="2024-03-10", end_date="2024-03-11"
            )

    @patch("requests.get")
    def test_get_workout_document(self, mock_get):
        mock_response_json = {
            "id": "test_workout_single",
            "activity": "swimming",
            "calories": 400.0,
            "day": "2024-03-10",
            "distance": 1000.0,
            "end_datetime": "2024-03-10T12:45:00+00:00",
            "energy": 1673.6,  # Example energy in kJ
            "intensity": "moderate",
            "label": "Pool session",
            "source": "apple_health",
            "start_datetime": "2024-03-10T12:00:00+00:00",
        }
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        document_id = "test_workout_single"
        workout_document = self.client.workout.get_workout_document(
            document_id=document_id
        )

        self.assertIsInstance(workout_document, WorkoutModel)
        self.assertEqual(workout_document.id, document_id)
        self.assertEqual(workout_document.activity, "swimming")
        self.assertEqual(workout_document.intensity, "moderate")
        self.assertEqual(workout_document.source, "apple_health")
        self.assertEqual(
            workout_document.start_datetime,
            datetime.fromisoformat("2024-03-10T12:00:00+00:00")
        )

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/workout/{document_id}",
            headers=self.client.headers,
            params=None,
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_workout_document_error(self, mock_get):
        mock_get.side_effect = OuraConnectionError("API error")
        document_id = "test_workout_single_error"
        with self.assertRaises(OuraConnectionError):
            self.client.workout.get_workout_document(document_id=document_id)

class TestEnhancedTag(unittest.TestCase):
    def setUp(self):

        self.client = OuraClient(access_token="test_token")

    @patch("requests.get")
    def test_get_enhanced_tag_documents(self, mock_get):
        mock_data = [
            {
                "id": "tag_1",
                "tag_type_code": "common_cold",
                "start_time": "2024-03-10T00:00:00+00:00",
                "end_time": "2024-03-12T00:00:00+00:00",
                "start_day": "2024-03-10",
                "end_day": "2024-03-12",
                "comment": "Feeling under the weather."
            },
            {
                "id": "tag_2",
                "tag_type_code": "vacation",
                "start_time": "2024-03-15T00:00:00+00:00",
                "start_day": "2024-03-15",
                "comment": "Beach time!"
            },
        ]
        mock_response_json = {
            "data": mock_data,
            "next_token": "next_enhanced_tag_token"
        }
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        start_date_str = "2024-03-01"  # Using different dates for query
        end_date_str = "2024-03-31"
        start_date = date.fromisoformat(start_date_str)
        end_date = date.fromisoformat(end_date_str)

        enhanced_tag_response = self.client.enhanced_tag.get_enhanced_tag_documents(
            start_date=start_date,
            end_date=end_date,
            next_token="test_enhanced_tag_token"
        )

        self.assertIsInstance(enhanced_tag_response, EnhancedTagResponse)
        self.assertEqual(len(enhanced_tag_response.data), 2)
        self.assertIsInstance(
            enhanced_tag_response.data[0], EnhancedTagModel
        )
        self.assertEqual(
            enhanced_tag_response.next_token, "next_enhanced_tag_token"
        )
        self.assertEqual(enhanced_tag_response.data[0].tag_type_code, "common_cold")
        self.assertEqual(
            enhanced_tag_response.data[1].start_day, date(2024, 3, 15)
        )

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/enhanced_tag",
            headers=self.client.headers,
            params={
                "start_date": start_date_str,
                "end_date": end_date_str,
                "next_token": "test_enhanced_tag_token",
            },
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_enhanced_tag_documents_with_string_dates(self, mock_get):
        mock_data = [
            {
                "id": "tag_str_date",
                "tag_type_code": "travel",
                "start_time": "2024-03-05T00:00:00+00:00",
                "start_day": "2024-03-05",
            }
        ]
        mock_response_json = {"data": mock_data, "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        start_date_str = "2024-03-01"
        end_date_str = "2024-03-31"

        self.client.enhanced_tag.get_enhanced_tag_documents(
            start_date=start_date_str, end_date=end_date_str
        )

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/enhanced_tag",
            headers=self.client.headers,
            params={"start_date": start_date_str, "end_date": end_date_str},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_enhanced_tag_documents_error(self, mock_get):
        mock_get.side_effect = OuraConnectionError("API error")
        with self.assertRaises(OuraConnectionError):
            self.client.enhanced_tag.get_enhanced_tag_documents(
                start_date="2024-03-01", end_date="2024-03-31"
            )

    @patch("requests.get")
    def test_get_enhanced_tag_document(self, mock_get):
        mock_response_json = {
            "id": "test_enhanced_tag_single",
            "tag_type_code": "stress",
            "start_time": "2024-03-10T10:00:00+00:00",
            "end_time": "2024-03-10T18:00:00+00:00",
            "start_day": "2024-03-10",
            "end_day": "2024-03-10",
            "comment": "Tough day at work."
        }
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        document_id = "test_enhanced_tag_single"
        enhanced_tag_document = self.client.enhanced_tag.get_enhanced_tag_document(
            document_id=document_id
        )

        self.assertIsInstance(enhanced_tag_document, EnhancedTagModel)
        self.assertEqual(enhanced_tag_document.id, document_id)
        self.assertEqual(enhanced_tag_document.tag_type_code, "stress")
        self.assertEqual(enhanced_tag_document.comment, "Tough day at work.")
        self.assertEqual(
            enhanced_tag_document.start_time,
            datetime.fromisoformat("2024-03-10T10:00:00+00:00")
        )
        self.assertEqual(
            enhanced_tag_document.end_day, date(2024, 3, 10)
        )

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/enhanced_tag/{document_id}",
            headers=self.client.headers,
            params=None,
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_enhanced_tag_document_error(self, mock_get):
        mock_get.side_effect = OuraConnectionError("API error")
        document_id = "test_enhanced_tag_single_error"
        with self.assertRaises(OuraConnectionError):
            self.client.enhanced_tag.get_enhanced_tag_document(document_id=document_id)

class TestDailySpo2(unittest.TestCase):
    def setUp(self):

        self.client = OuraClient(access_token="test_token")

    @patch("requests.get")
    def test_get_daily_spo2_documents(self, mock_get):
        mock_data = [
            {
                "id": "spo2_1",
                "day": "2024-03-10",
                "spo2_percentage": 97.5,
                "aggregated_values": {"average": 97.5},
                "timestamp": "2024-03-11T00:00:00+00:00"
            },
            {
                "id": "spo2_2",
                "day": "2024-03-11",
                "aggregated_values": {"average": 98.0},
                "timestamp": "2024-03-12T00:00:00+00:00"
            },
        ]
        mock_response_json = {
            "data": mock_data,
            "next_token": "next_spo2_token"
        }
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        start_date_str = "2024-03-10"
        end_date_str = "2024-03-11"
        start_date = date.fromisoformat(start_date_str)
        end_date = date.fromisoformat(end_date_str)

        daily_spo2_response = self.client.daily_spo2.get_daily_spo2_documents(
            start_date=start_date,
            end_date=end_date,
            next_token="test_spo2_token"
        )

        self.assertIsInstance(daily_spo2_response, DailySpO2Response)
        self.assertEqual(len(daily_spo2_response.data), 2)
        self.assertIsInstance(daily_spo2_response.data[0], DailySpO2Model)
        # Check if aggregated_values exists
        if daily_spo2_response.data[0].aggregated_values:
            self.assertIsInstance(
                daily_spo2_response.data[0].aggregated_values,
                DailySpO2AggregatedValuesModel
            )
        self.assertEqual(daily_spo2_response.next_token, "next_spo2_token")
        self.assertEqual(daily_spo2_response.data[0].spo2_percentage, 97.5)

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/daily_spo2",
            headers=self.client.headers,
            params={
                "start_date": start_date_str,
                "end_date": end_date_str,
                "next_token": "test_spo2_token",
            },
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_spo2_documents_with_string_dates(self, mock_get):
        mock_data = [
            {
                "id": "spo2_str_date",
                "day": "2024-03-10",
                "aggregated_values": {"average": 96.0},
                "timestamp": "2024-03-11T00:00:00+00:00"
            }
        ]
        mock_response_json = {"data": mock_data, "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        start_date_str = "2024-03-10"
        end_date_str = "2024-03-11"

        self.client.daily_spo2.get_daily_spo2_documents(
            start_date=start_date_str, end_date=end_date_str
        )

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/daily_spo2",
            headers=self.client.headers,
            params={"start_date": start_date_str, "end_date": end_date_str},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_spo2_documents_error(self, mock_get):
        mock_get.side_effect = OuraConnectionError("API error")
        with self.assertRaises(OuraConnectionError):
            self.client.daily_spo2.get_daily_spo2_documents(
                start_date="2024-03-10", end_date="2024-03-11"
            )

    @patch("requests.get")
    def test_get_daily_spo2_document(self, mock_get):
        mock_response_json = {
            "id": "test_spo2_single",
            "day": "2024-03-10",
            "spo2_percentage": 98.2,
            "aggregated_values": {"average": 98.2},
            "timestamp": "2024-03-11T00:00:00+00:00"
        }
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        document_id = "test_spo2_single"
        daily_spo2_document = self.client.daily_spo2.get_daily_spo2_document(
            document_id=document_id
        )

        self.assertIsInstance(daily_spo2_document, DailySpO2Model)
        self.assertEqual(daily_spo2_document.id, document_id)
        self.assertEqual(daily_spo2_document.spo2_percentage, 98.2)
        if daily_spo2_document.aggregated_values:
            self.assertEqual(daily_spo2_document.aggregated_values.average, 98.2)
        self.assertEqual(
            daily_spo2_document.timestamp,
            datetime.fromisoformat("2024-03-11T00:00:00+00:00")
        )

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/daily_spo2/{document_id}",
            headers=self.client.headers,
            params=None,
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_spo2_document_error(self, mock_get):
        mock_get.side_effect = OuraConnectionError("API error")
        document_id = "test_spo2_single_error"
        with self.assertRaises(OuraConnectionError):
            self.client.daily_spo2.get_daily_spo2_document(document_id=document_id)

class TestSleepTime(unittest.TestCase):
    def setUp(self):

        self.client = OuraClient(access_token="test_token")

    @patch("requests.get")
    def test_get_sleep_time_documents(self, mock_get):
        mock_data = [
            {
                "id": "st_1",
                "day": "2024-03-10",
                "optimal_bedtime": {
                    "start_offset": -1800,
                    "end_offset": 3600,
                    "day_light_saving_time": 0
                },
                "recommendation": {"recommendation": "go_to_bed_earlier"},
                "status": {"status": "slightly_late"},
                "timestamp": "2024-03-10T04:00:00+00:00"
            },
            {
                "id": "st_2",
                "day": "2024-03-11",
                  # Missing day_light_saving_time to test Optional
                "optimal_bedtime": {
                    "start_offset": -1500,
                    "end_offset": 3900
                },
                "recommendation": {
                    "recommendation": "maintain_consistent_schedule"
                },
                "status": {"status": "optimal"},
                "timestamp": "2024-03-11T04:00:00+00:00"
            },
        ]
        mock_response_json = {
            "data": mock_data,
            "next_token": "next_sleep_time_token"
        }
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        start_date_str = "2024-03-10"
        end_date_str = "2024-03-11"
        start_date = date.fromisoformat(start_date_str)
        end_date = date.fromisoformat(end_date_str)

        sleep_time_response = self.client.sleep_time.get_sleep_time_documents(
            start_date=start_date,
            end_date=end_date,
            next_token="test_sleep_time_token"
        )

        self.assertIsInstance(sleep_time_response, SleepTimeResponse)
        self.assertEqual(len(sleep_time_response.data), 2)
        self.assertIsInstance(sleep_time_response.data[0], SleepTimeModel)
        if sleep_time_response.data[0].optimal_bedtime:
            self.assertIsInstance(
                sleep_time_response.data[0].optimal_bedtime,
                SleepTimeWindow
            )
        if sleep_time_response.data[0].recommendation:
            self.assertIsInstance(
                sleep_time_response.data[0].recommendation,
                SleepTimeRecommendation
            )
        if sleep_time_response.data[0].status:
            self.assertIsInstance(
                sleep_time_response.data[0].status,
                SleepTimeStatus
            )
        self.assertEqual(sleep_time_response.next_token, "next_sleep_time_token")
        self.assertEqual(sleep_time_response.data[0].day, date(2024, 3, 10))

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/sleep_time",
            headers=self.client.headers,
            params={
                "start_date": start_date_str,
                "end_date": end_date_str,
                "next_token": "test_sleep_time_token",
            },
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_sleep_time_documents_with_string_dates(self, mock_get):
        mock_data = [
            {
                "id": "st_str_date",
                "day": "2024-03-10",
                "optimal_bedtime": {"start_offset": -1800, "end_offset": 3600},
                "timestamp": "2024-03-10T04:00:00+00:00"
            }
        ]
        mock_response_json = {"data": mock_data, "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        start_date_str = "2024-03-10"
        end_date_str = "2024-03-11"

        self.client.sleep_time.get_sleep_time_documents(
            start_date=start_date_str, end_date=end_date_str
        )

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/sleep_time",
            headers=self.client.headers,
            params={"start_date": start_date_str, "end_date": end_date_str},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_sleep_time_documents_error(self, mock_get):
        mock_get.side_effect = OuraConnectionError("API error")
        with self.assertRaises(OuraConnectionError):
            self.client.sleep_time.get_sleep_time_documents(
                start_date="2024-03-10", end_date="2024-03-11"
            )

    @patch("requests.get")
    def test_get_sleep_time_document(self, mock_get):
        mock_response_json = {
            "id": "test_st_single",
            "day": "2024-03-10",
            "optimal_bedtime": {
                "start_offset": -1800,
                "end_offset": 3600,
                "day_light_saving_time": 0
            },
            "recommendation": {"recommendation": "go_to_bed_earlier"},
            "status": {"status": "slightly_late"},
            "timestamp": "2024-03-10T04:00:00+00:00"
        }
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        document_id = "test_st_single"
        sleep_time_document = self.client.sleep_time.get_sleep_time_document(
            document_id=document_id
        )

        self.assertIsInstance(sleep_time_document, SleepTimeModel)
        self.assertEqual(sleep_time_document.id, document_id)
        if sleep_time_document.optimal_bedtime:
            self.assertEqual(
                sleep_time_document.optimal_bedtime.start_offset, -1800
            )
        if sleep_time_document.recommendation:
            self.assertEqual(
                sleep_time_document.recommendation.recommendation,
                "go_to_bed_earlier"
            )
        if sleep_time_document.status:
            self.assertEqual(
                sleep_time_document.status.status, "slightly_late"
            )
        self.assertEqual(
            sleep_time_document.timestamp,
            datetime.fromisoformat("2024-03-10T04:00:00+00:00")
        )

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/sleep_time/{document_id}",
            headers=self.client.headers,
            params=None,
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_sleep_time_document_error(self, mock_get):
        # As per the implementation note, this endpoint might not exist.
        # If it doesn't, the API would return a 404, which _make_request would
        # raise as an HTTPError (a subclass of RequestException).
        mock_get.side_effect = requests.exceptions.ConnectionError("API error or Not Found")
        document_id = "test_st_single_error"
        with self.assertRaises(OuraConnectionError):
            self.client.sleep_time.get_sleep_time_document(document_id=document_id)

class TestRestModePeriod(unittest.TestCase):
    def setUp(self):

        self.client = OuraClient(access_token="test_token")

    @patch("requests.get")
    def test_get_rest_mode_period_documents(self, mock_get):
        mock_data = [
            {
                "id": "rmp_1",
                "day": "2024-03-10",
                "start_time": "2024-03-10T10:00:00+00:00",
                "end_time": "2024-03-10T18:00:00+00:00",
                "rest_mode_state": "on_demand_rest",
                "baseline_heart_rate": 60,
            },
            {
                "id": "rmp_2",
                "day": "2024-03-11",
                "start_time": "2024-03-11T09:00:00+00:00",
                "rest_mode_state": "recovering_from_illness",
                "baseline_hrv": 50,
            },
        ]
        mock_response_json = {"data": mock_data, "next_token": "next_rmp_token"}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        start_date_str = "2024-03-10"
        end_date_str = "2024-03-11"
        start_date = date.fromisoformat(start_date_str)
        end_date = date.fromisoformat(end_date_str)

        rest_mode_response = (
            self.client.rest_mode_period.get_rest_mode_period_documents(
                start_date=start_date,
                end_date=end_date,
                next_token="test_rmp_token"
            )
        )

        self.assertIsInstance(rest_mode_response, RestModePeriodResponse)
        self.assertEqual(len(rest_mode_response.data), 2)
        self.assertIsInstance(
            rest_mode_response.data[0], RestModePeriodModel
        )
        self.assertEqual(rest_mode_response.next_token, "next_rmp_token")
        self.assertEqual(
            rest_mode_response.data[0].rest_mode_state, "on_demand_rest"
        )

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/rest_mode_period",
            headers=self.client.headers,
            params={
                "start_date": start_date_str,
                "end_date": end_date_str,
                "next_token": "test_rmp_token",
            },
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_rest_mode_period_documents_with_string_dates(self, mock_get):
        mock_data = [
            {
                "id": "rmp_str_date",
                "day": "2024-03-10",
                "start_time": "2024-03-10T10:00:00+00:00",
                "rest_mode_state": "on_demand_rest",
            }
        ]
        mock_response_json = {"data": mock_data, "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        start_date_str = "2024-03-10"
        end_date_str = "2024-03-11"

        self.client.rest_mode_period.get_rest_mode_period_documents(
            start_date=start_date_str, end_date=end_date_str
        )

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/rest_mode_period",
            headers=self.client.headers,
            params={"start_date": start_date_str, "end_date": end_date_str},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_rest_mode_period_documents_error(self, mock_get):
        mock_get.side_effect = OuraConnectionError("API error")
        with self.assertRaises(OuraConnectionError):
            self.client.rest_mode_period.get_rest_mode_period_documents(
                start_date="2024-03-10", end_date="2024-03-11"
            )

    @patch("requests.get")
    def test_get_rest_mode_period_document(self, mock_get):
        mock_response_json = {
            "id": "test_rmp_single",
            "day": "2024-03-10",
            "start_time": "2024-03-10T10:00:00+00:00",
            "end_time": "2024-03-10T18:00:00+00:00",
            "rest_mode_state": "recovering_from_illness",
            "baseline_heart_rate": 62,
            "baseline_hrv": 48,
            "baseline_skin_temperature": -0.2,
        }
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        document_id = "test_rmp_single"
        rmp_document = self.client.rest_mode_period.get_rest_mode_period_document(
            document_id=document_id
        )

        self.assertIsInstance(rmp_document, RestModePeriodModel)
        self.assertEqual(rmp_document.id, document_id)
        self.assertEqual(
            rmp_document.rest_mode_state, "recovering_from_illness"
        )
        self.assertEqual(rmp_document.baseline_hrv, 48)
        self.assertEqual(
            rmp_document.start_time,
            datetime.fromisoformat("2024-03-10T10:00:00+00:00")
        )

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/usercollection/rest_mode_period/{document_id}",
            headers=self.client.headers,
            params=None,
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_rest_mode_period_document_error(self, mock_get):
        mock_get.side_effect = OuraConnectionError("API error")
        document_id = "test_rmp_single_error"
        with self.assertRaises(OuraConnectionError):
            self.client.rest_mode_period.get_rest_mode_period_document(
                document_id=document_id
            )

class TestDailyStress(unittest.TestCase):
    def setUp(self):

        self.client = OuraClient(access_token="test_token")
        self.base_url = self.client.BASE_URL

    @patch("requests.get")
    def test_get_daily_stress_documents_no_params(self, mock_get):
        mock_response_data = {"data": [], "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        response = self.client.daily_stress.get_daily_stress_documents()
        self.assertIsInstance(response, DailyStressResponse)
        mock_get.assert_called_once_with(
            f"{self.base_url}/usercollection/daily_stress",
            headers=self.client.headers,
            params={},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_stress_documents_start_date(self, mock_get):
        mock_response_data = {"data": [], "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        self.client.daily_stress.get_daily_stress_documents(
            start_date="2024-01-01"
        )
        mock_get.assert_called_once_with(
            f"{self.base_url}/usercollection/daily_stress",
            headers=self.client.headers,
            params={"start_date": "2024-01-01"},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_stress_documents_end_date(self, mock_get):
        mock_response_data = {"data": [], "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        self.client.daily_stress.get_daily_stress_documents(end_date="2024-01-31")
        mock_get.assert_called_once_with(
            f"{self.base_url}/usercollection/daily_stress",
            headers=self.client.headers,
            params={"end_date": "2024-01-31"},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_stress_documents_start_and_end_date(self, mock_get):
        mock_response_data = {"data": [], "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        self.client.daily_stress.get_daily_stress_documents(
            start_date="2024-01-01", end_date="2024-01-31"
        )
        mock_get.assert_called_once_with(
            f"{self.base_url}/usercollection/daily_stress",
            headers=self.client.headers,
            params={"start_date": "2024-01-01", "end_date": "2024-01-31"},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_stress_documents_next_token(self, mock_get):
        mock_response_data = {"data": [], "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        self.client.daily_stress.get_daily_stress_documents(
            next_token="some_token"
        )
        mock_get.assert_called_once_with(
            f"{self.base_url}/usercollection/daily_stress",
            headers=self.client.headers,
            params={"next_token": "some_token"},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_stress_documents_success(self, mock_get):
        mock_data = [
            {
                "id": "stress_doc_1",
                "day": "2024-03-15",
                "stress_high": 1200,
                "recovery_high": 3600,
                "day_summary": "restored",
                "timestamp": "2024-03-15T08:00:00Z",
            }
        ]
        mock_response_json = {
            "data": mock_data,
            "next_token": "stress_next_token"
        }
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        response = self.client.daily_stress.get_daily_stress_documents(
            start_date="2024-03-15"
        )
        self.assertIsInstance(response, DailyStressResponse)
        self.assertEqual(len(response.data), 1)
        self.assertIsInstance(response.data[0], DailyStressModel)
        self.assertEqual(response.data[0].id, "stress_doc_1")
        self.assertEqual(response.data[0].stress_high, 1200)
        # Check day_summary value
        self.assertEqual(response.data[0].day_summary, "restored")
        self.assertEqual(response.next_token, "stress_next_token")
        mock_get.assert_called_with(
            f"{self.base_url}/usercollection/daily_stress",
            headers=self.client.headers,
            params={"start_date": "2024-03-15"},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_stress_documents_api_error_400(self, mock_get):
        # Mock a 400 error response
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 400
        mock_response.reason = "Client Error"
        mock_response.json.return_value = {"error": "400 Client Error"}
        mock_get.return_value = mock_response
        
        with self.assertRaises(OuraClientError):
            self.client.daily_stress.get_daily_stress_documents()

    @patch("requests.get")
    def test_get_daily_stress_documents_api_error_429(self, mock_get):
        # Mock a 429 error response
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 429
        mock_response.reason = "Too Many Requests"
        mock_response.json.return_value = {"error": "429 Client Error"}
        mock_get.return_value = mock_response
        
        with self.assertRaises(OuraRateLimitError):
            self.client.daily_stress.get_daily_stress_documents()

    @patch("requests.get")
    def test_get_daily_stress_document_success(self, mock_get):
        document_id = "sample_stress_id"
        mock_response_json = {
            "id": document_id,
            "day": "2024-03-16",
            "stress_high": 1500,
            "recovery_high": 3000,
            "day_summary": "stressful",
            "timestamp": "2024-03-16T08:00:00Z",
        }
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        response = self.client.daily_stress.get_daily_stress_document(document_id)
        self.assertIsInstance(response, DailyStressModel)
        self.assertEqual(response.id, document_id)
        self.assertEqual(response.day, date(2024, 3, 16))
        self.assertEqual(response.stress_high, 1500)
        # Check day_summary value
        self.assertEqual(response.day_summary, "stressful")

        mock_get.assert_called_once_with(
            f"{self.base_url}/usercollection/daily_stress/{document_id}",
            headers=self.client.headers,
            params=None,  # No params for single document GET
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_stress_document_not_found_404(self, mock_get):
        document_id = "non_existent_id"
        # Mock a 404 error response
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 404
        mock_response.reason = "Not Found"
        mock_response.json.return_value = {"error": "404 Client Error: Not Found"}
        mock_get.return_value = mock_response

        with self.assertRaises(OuraNotFoundError):
            self.client.daily_stress.get_daily_stress_document(document_id)

class TestDailyResilience(unittest.TestCase):
    def setUp(self):

        self.client = OuraClient(access_token="test_token")
        self.base_url = self.client.BASE_URL

    @patch("requests.get")
    def test_get_daily_resilience_documents_no_params(self, mock_get):
        mock_response_data = {"data": [], "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        response = self.client.daily_resilience.get_daily_resilience_documents()
        self.assertIsInstance(response, DailyResilienceResponse)
        mock_get.assert_called_once_with(
            f"{self.base_url}/usercollection/daily_resilience",
            headers=self.client.headers,
            params={},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_resilience_documents_start_date(self, mock_get):
        mock_response_data = {"data": [], "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        self.client.daily_resilience.get_daily_resilience_documents(
            start_date="2024-02-01"
        )
        mock_get.assert_called_once_with(
            f"{self.base_url}/usercollection/daily_resilience",
            headers=self.client.headers,
            params={"start_date": "2024-02-01"},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_resilience_documents_end_date(self, mock_get):
        mock_response_data = {"data": [], "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        self.client.daily_resilience.get_daily_resilience_documents(
            end_date="2024-02-28"
        )
        mock_get.assert_called_once_with(
            f"{self.base_url}/usercollection/daily_resilience",
            headers=self.client.headers,
            params={"end_date": "2024-02-28"},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_resilience_documents_start_and_end_date(self, mock_get):
        mock_response_data = {"data": [], "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        self.client.daily_resilience.get_daily_resilience_documents(
            start_date="2024-02-01", end_date="2024-02-28"
        )
        mock_get.assert_called_once_with(
            f"{self.base_url}/usercollection/daily_resilience",
            headers=self.client.headers,
            params={"start_date": "2024-02-01", "end_date": "2024-02-28"},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_resilience_documents_next_token(self, mock_get):
        mock_response_data = {"data": [], "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        self.client.daily_resilience.get_daily_resilience_documents(
            next_token="res_token"
        )
        mock_get.assert_called_once_with(
            f"{self.base_url}/usercollection/daily_resilience",
            headers=self.client.headers,
            params={"next_token": "res_token"},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_resilience_documents_success(self, mock_get):
        mock_contributors_data = {
            "sleep_recovery": 75.0,
            "daytime_recovery": 60.0,
            "stress": 80.0,
        }
        mock_data = [
            {
                "id": "res_doc_1",
                "day": "2024-03-18",
                "contributors": mock_contributors_data,
                "level": "solid",
                "timestamp": "2024-03-18T08:00:00Z",
            }
        ]
        mock_response_json = {
            "data": mock_data,
            "next_token": "res_next_token"
        }
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        response = self.client.daily_resilience.get_daily_resilience_documents(
            start_date="2024-03-18"
        )
        self.assertIsInstance(response, DailyResilienceResponse)
        self.assertEqual(len(response.data), 1)
        model_item = response.data[0]
        self.assertIsInstance(model_item, DailyResilienceModel)
        self.assertEqual(model_item.id, "res_doc_1")
        # Check contributors
        self.assertIsNotNone(model_item.contributors)
        self.assertEqual(model_item.contributors.sleep_recovery, 75.0)
        self.assertEqual(model_item.level, "solid")
        self.assertEqual(response.next_token, "res_next_token")
        mock_get.assert_called_with(
            f"{self.base_url}/usercollection/daily_resilience",
            headers=self.client.headers,
            params={"start_date": "2024-03-18"},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_resilience_documents_api_error_400(self, mock_get):
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 400
        mock_response.reason = "Bad Request"
        mock_response.json.return_value = {"error": "400 Client Error"}
        mock_get.return_value = mock_response
        with self.assertRaises(OuraClientError):
            self.client.daily_resilience.get_daily_resilience_documents()

    @patch("requests.get")
    def test_get_daily_resilience_document_success(self, mock_get):
        document_id = "sample_res_id"
        mock_contributors_data = {
            "sleep_recovery": 80.5,
            "daytime_recovery": 65.2,
            "stress": 70.1,
        }
        mock_response_json = {
            "id": document_id,
            "day": "2024-03-19",
            "contributors": mock_contributors_data,
            "level": "exceptional",
            "timestamp": "2024-03-19T08:00:00Z",
        }
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        response = self.client.daily_resilience.get_daily_resilience_document(
            document_id
        )
        self.assertIsInstance(response, DailyResilienceModel)
        self.assertEqual(response.id, document_id)
        self.assertEqual(response.day, date(2024, 3, 19))
        # Check contributors
        self.assertIsNotNone(response.contributors)
        self.assertEqual(response.contributors.daytime_recovery, 65.2)
        self.assertEqual(response.level, "exceptional")

        mock_get.assert_called_once_with(
            f"{self.base_url}/usercollection/daily_resilience/{document_id}",
            headers=self.client.headers,
            params=None,
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_resilience_document_not_found_404(self, mock_get):
        document_id = "non_existent_res_id"
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 404
        mock_response.reason = "Not Found"
        mock_response.json.return_value = {"error": "404 Client Error: Not Found"}
        mock_get.return_value = mock_response

        with self.assertRaises(OuraNotFoundError):
            self.client.daily_resilience.get_daily_resilience_document(
                document_id
            )

class TestDailyCardiovascularAge(unittest.TestCase):
    def setUp(self):

        self.client = OuraClient(access_token="test_token")
        self.base_url = self.client.BASE_URL

    @patch("requests.get")
    def test_get_daily_cardiovascular_age_documents_no_params(self, mock_get):
        mock_response_data = {"data": [], "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        response = (
            self.client.daily_cardiovascular_age.get_daily_cardiovascular_age_documents()
        )
        self.assertIsInstance(response, DailyCardiovascularAgeResponse)
        mock_get.assert_called_once_with(
            f"{self.base_url}/usercollection/daily_cardiovascular_age",
            headers=self.client.headers,
            params={},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_cardiovascular_age_documents_start_date(self, mock_get):
        mock_response_data = {"data": [], "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        self.client.daily_cardiovascular_age.get_daily_cardiovascular_age_documents(
            start_date="2024-03-01"
        )
        mock_get.assert_called_once_with(
            f"{self.base_url}/usercollection/daily_cardiovascular_age",
            headers=self.client.headers,
            params={"start_date": "2024-03-01"},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_cardiovascular_age_documents_end_date(self, mock_get):
        mock_response_data = {"data": [], "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        self.client.daily_cardiovascular_age.get_daily_cardiovascular_age_documents(
            end_date="2024-03-31"
        )
        mock_get.assert_called_once_with(
            f"{self.base_url}/usercollection/daily_cardiovascular_age",
            headers=self.client.headers,
            params={"end_date": "2024-03-31"},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_cardiovascular_age_documents_start_and_end_date(self, mock_get):
        mock_response_data = {"data": [], "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        self.client.daily_cardiovascular_age.get_daily_cardiovascular_age_documents(
            start_date="2024-03-01", end_date="2024-03-31"
        )
        mock_get.assert_called_once_with(
            f"{self.base_url}/usercollection/daily_cardiovascular_age",
            headers=self.client.headers,
            params={"start_date": "2024-03-01", "end_date": "2024-03-31"},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_cardiovascular_age_documents_next_token(self, mock_get):
        mock_response_data = {"data": [], "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        self.client.daily_cardiovascular_age.get_daily_cardiovascular_age_documents(
            next_token="cva_token"
        )
        mock_get.assert_called_once_with(
            f"{self.base_url}/usercollection/daily_cardiovascular_age",
            headers=self.client.headers,
            params={"next_token": "cva_token"},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_cardiovascular_age_documents_success(self, mock_get):
        mock_data = [
            {
                # The API might return an 'id' but DailyCardiovascularAgeModel doesn't have it.
                # This is fine, Pydantic will ignore extra fields.
                "id": "cva_doc_api_id_1",
                "day": "2024-03-20",
                "vascular_age": 30.5,  # Changed to float to match spec
                "timestamp": "2024-03-20T08:00:00Z",
            }
        ]
        mock_response_json = {
            "data": mock_data,
            "next_token": "cva_next_token"
        }
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        response = (
            self.client.daily_cardiovascular_age.get_daily_cardiovascular_age_documents(
                start_date="2024-03-20"
            )
        )
        self.assertIsInstance(response, DailyCardiovascularAgeResponse)
        self.assertEqual(len(response.data), 1)
        model_item = response.data[0]
        self.assertIsInstance(model_item, DailyCardiovascularAgeModel)
        self.assertEqual(model_item.day, date(2024, 3, 20))
        self.assertEqual(model_item.vascular_age, 30.5)
        self.assertEqual(response.next_token, "cva_next_token")
        mock_get.assert_called_with(
            f"{self.base_url}/usercollection/daily_cardiovascular_age",
            headers=self.client.headers,
            params={"start_date": "2024-03-20"},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_cardiovascular_age_documents_api_error_400(self, mock_get):
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 400
        mock_response.reason = "Bad Request"
        mock_response.json.return_value = {"error": "400 Client Error"}
        mock_get.return_value = mock_response
        with self.assertRaises(OuraClientError):
            self.client.daily_cardiovascular_age.get_daily_cardiovascular_age_documents()

    @patch("requests.get")
    def test_get_daily_cardiovascular_age_document_success(self, mock_get):
        document_id = "sample_cva_id"
        mock_response_json = {
            "id": document_id,
            "day": "2024-03-21",
            "vascular_age": 32.0,  # Changed to float
            "timestamp": "2024-03-21T08:00:00Z",
        }
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        response = (
            self.client.daily_cardiovascular_age.get_daily_cardiovascular_age_document(
                document_id
            )
        )
        self.assertIsInstance(response, DailyCardiovascularAgeModel)
        self.assertEqual(response.day, date(2024, 3, 21))
        self.assertEqual(response.vascular_age, 32.0)

        mock_get.assert_called_once_with(
            f"{self.base_url}/usercollection/daily_cardiovascular_age/{document_id}",
            headers=self.client.headers,
            params=None,
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_daily_cardiovascular_age_document_not_found_404(self, mock_get):
        document_id = "non_existent_cva_id"
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 404
        mock_response.reason = "Not Found"
        mock_response.json.return_value = {"error": "404 Client Error: Not Found"}
        mock_get.return_value = mock_response

        with self.assertRaises(OuraNotFoundError):
            self.client.daily_cardiovascular_age.get_daily_cardiovascular_age_document(
                document_id
            )

class TestVo2Max(unittest.TestCase):
    def setUp(self):

        self.client = OuraClient(access_token="test_token")
        self.base_url = self.client.BASE_URL
        self.correct_path_segment = "/usercollection/vO2_max"  # Note the casing

    @patch("requests.get")
    def test_get_vo2_max_documents_no_params(self, mock_get):
        mock_response_data = {"data": [], "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        response = self.client.vo2_max.get_vo2_max_documents()
        self.assertIsInstance(response, Vo2MaxResponse)
        mock_get.assert_called_once_with(
            f"{self.base_url}{self.correct_path_segment}",
            headers=self.client.headers,
            params={},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_vo2_max_documents_start_date(self, mock_get):
        mock_response_data = {"data": [], "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        self.client.vo2_max.get_vo2_max_documents(start_date="2024-04-01")
        mock_get.assert_called_once_with(
            f"{self.base_url}{self.correct_path_segment}",
            headers=self.client.headers,
            params={"start_date": "2024-04-01"},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_vo2_max_documents_end_date(self, mock_get):
        mock_response_data = {"data": [], "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        self.client.vo2_max.get_vo2_max_documents(end_date="2024-04-30")
        mock_get.assert_called_once_with(
            f"{self.base_url}{self.correct_path_segment}",
            headers=self.client.headers,
            params={"end_date": "2024-04-30"},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_vo2_max_documents_start_and_end_date(self, mock_get):
        mock_response_data = {"data": [], "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        self.client.vo2_max.get_vo2_max_documents(
            start_date="2024-04-01", end_date="2024-04-30"
        )
        mock_get.assert_called_once_with(
            f"{self.base_url}{self.correct_path_segment}",
            headers=self.client.headers,
            params={"start_date": "2024-04-01", "end_date": "2024-04-30"},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_vo2_max_documents_next_token(self, mock_get):
        mock_response_data = {"data": [], "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        self.client.vo2_max.get_vo2_max_documents(next_token="vo2_token")
        mock_get.assert_called_once_with(
            f"{self.base_url}{self.correct_path_segment}",
            headers=self.client.headers,
            params={"next_token": "vo2_token"},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_vo2_max_documents_success(self, mock_get):
        mock_data = [
            {
                "id": "vo2_doc_1",
                "day": "2024-04-10",
                "timestamp": "2024-04-10T10:00:00+00:00",
                "vo2_max": 35.5,
            }
        ]
        mock_response_json = {
            "data": mock_data,
            "next_token": "vo2_next_token"
        }
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        response = self.client.vo2_max.get_vo2_max_documents(
            start_date="2024-04-10"
        )
        self.assertIsInstance(response, Vo2MaxResponse)
        self.assertEqual(len(response.data), 1)
        model_item = response.data[0]
        self.assertIsInstance(model_item, Vo2MaxModel)
        self.assertEqual(model_item.id, "vo2_doc_1")
        self.assertEqual(model_item.day, date(2024, 4, 10))
        self.assertEqual(model_item.vo2_max, 35.5)
        self.assertEqual(response.next_token, "vo2_next_token")
        mock_get.assert_called_with(
            f"{self.base_url}{self.correct_path_segment}",
            headers=self.client.headers,
            params={"start_date": "2024-04-10"},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_vo2_max_documents_api_error_400(self, mock_get):
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 400
        mock_response.reason = "Bad Request"
        mock_response.json.return_value = {"error": "400 Client Error"}
        mock_get.return_value = mock_response
        with self.assertRaises(OuraClientError):
            self.client.vo2_max.get_vo2_max_documents()

    @patch("requests.get")
    def test_get_vo2_max_document_success(self, mock_get):
        document_id = "sample_vo2_id"
        mock_response_json = {
            "id": document_id,
            "day": "2024-04-11",
            "timestamp": "2024-04-11T11:00:00+00:00",
            "vo2_max": 36.2,
        }
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        response = self.client.vo2_max.get_vo2_max_document(document_id)
        self.assertIsInstance(response, Vo2MaxModel)
        self.assertEqual(response.id, document_id)
        self.assertEqual(response.day, date(2024, 4, 11))
        self.assertEqual(
            response.timestamp,
            datetime.fromisoformat("2024-04-11T11:00:00+00:00")
        )
        self.assertEqual(response.vo2_max, 36.2)

        mock_get.assert_called_once_with(
            f"{self.base_url}{self.correct_path_segment}/{document_id}",
            headers=self.client.headers,
            params=None,
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_vo2_max_document_not_found_404(self, mock_get):
        document_id = "non_existent_vo2_id"
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 404
        mock_response.reason = "Not Found"
        mock_response.json.return_value = {"error": "404 Client Error: Not Found"}
        mock_get.return_value = mock_response

        with self.assertRaises(OuraNotFoundError):
            self.client.vo2_max.get_vo2_max_document(document_id)


class TestRingConfiguration(unittest.TestCase):
    def setUp(self):
        self.client = OuraClient(access_token="test_token")
        self.base_url = self.client.BASE_URL

    @patch("requests.get")
    def test_get_ring_configuration_documents_no_params(self, mock_get):
        mock_response_data = {"data": [], "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        response = self.client.ring_configuration.get_ring_configuration_documents()
        self.assertIsInstance(response, RingConfigurationResponse)
        mock_get.assert_called_once_with(
            f"{self.base_url}/usercollection/ring_configuration",
            headers=self.client.headers,
            params=None,
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_ring_configuration_documents_start_date(self, mock_get):
        mock_response_data = {"data": [], "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        self.client.ring_configuration.get_ring_configuration_documents(
            start_date="2024-03-01"
        )
        mock_get.assert_called_once_with(
            f"{self.base_url}/usercollection/ring_configuration",
            headers=self.client.headers,
            params={"start_date": "2024-03-01"},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_ring_configuration_documents_end_date(self, mock_get):
        mock_response_data = {"data": [], "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        self.client.ring_configuration.get_ring_configuration_documents(
            end_date="2024-02-28"
        )
        mock_get.assert_called_once_with(
            f"{self.base_url}/usercollection/ring_configuration",
            headers=self.client.headers,
            params={"end_date": "2024-02-28"},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_ring_configuration_documents_start_and_end_date(self, mock_get):
        mock_response_data = {"data": [], "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        self.client.ring_configuration.get_ring_configuration_documents(
            start_date="2024-02-01", end_date="2024-02-28"
        )
        mock_get.assert_called_once_with(
            f"{self.base_url}/usercollection/ring_configuration",
            headers=self.client.headers,
            params={"start_date": "2024-02-01", "end_date": "2024-02-28"},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_ring_configuration_documents_next_token(self, mock_get):
        mock_response_data = {"data": [], "next_token": None}
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        self.client.ring_configuration.get_ring_configuration_documents(
            next_token="next_token_string"
        )
        mock_get.assert_called_once_with(
            f"{self.base_url}/usercollection/ring_configuration",
            headers=self.client.headers,
            params={"next_token": "next_token_string"},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_ring_configuration_documents_success(self, mock_get):
        mock_response_data = {
            "data": [{
                "id": "ring_config_1",
                "color": "silver",
                "design": "heritage",
                "firmware_version": "2.1.0",
                "hardware_type": "gen3",
                "set_up_at": "2024-01-15T10:00:00+00:00",
                "size": 8
            }],
            "next_token": "ring_next_token"
        }
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        response = self.client.ring_configuration.get_ring_configuration_documents(
            start_date="2024-01-15"
        )
        self.assertIsInstance(response, RingConfigurationResponse)
        self.assertEqual(len(response.data), 1)
        model_item = response.data[0]
        self.assertIsInstance(model_item, RingConfigurationModel)
        self.assertEqual(model_item.id, "ring_config_1")
        self.assertEqual(model_item.color, "silver")
        self.assertEqual(model_item.design, "heritage")
        self.assertEqual(model_item.firmware_version, "2.1.0")
        self.assertEqual(model_item.hardware_type, "gen3")
        self.assertEqual(model_item.size, 8)
        self.assertEqual(response.next_token, "ring_next_token")
        mock_get.assert_called_with(
            f"{self.base_url}/usercollection/ring_configuration",
            headers=self.client.headers,
            params={"start_date": "2024-01-15"},
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_ring_configuration_documents_api_error_400(self, mock_get):
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 400
        mock_response.reason = "Bad Request"
        mock_response.json.return_value = {"error": "400 Client Error"}
        mock_get.return_value = mock_response
        with self.assertRaises(OuraClientError):
            self.client.ring_configuration.get_ring_configuration_documents()

    @patch("requests.get")
    def test_get_ring_configuration_document_success(self, mock_get):
        document_id = "ring_config_test_id"
        mock_response_json = {
            "id": document_id,
            "color": "black",
            "design": "horizon",
            "firmware_version": "2.2.1",
            "hardware_type": "gen3",
            "set_up_at": "2024-02-01T08:30:00+00:00",
            "size": 9
        }
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_json
        mock_get.return_value = mock_response

        response = self.client.ring_configuration.get_ring_configuration_document(
            document_id=document_id
        )
        self.assertIsInstance(response, RingConfigurationModel)
        self.assertEqual(response.id, document_id)
        self.assertEqual(response.color, "black")
        self.assertEqual(response.design, "horizon")
        self.assertEqual(response.firmware_version, "2.2.1")
        self.assertEqual(response.hardware_type, "gen3")
        self.assertEqual(response.size, 9)

        mock_get.assert_called_once_with(
            f"{self.base_url}/usercollection/ring_configuration/{document_id}",
            headers=self.client.headers,
            params=None,
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_ring_configuration_document_not_found_404(self, mock_get):
        document_id = "non_existent_ring_config_id"
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 404
        mock_response.reason = "Not Found"
        mock_response.json.return_value = {"error": "404 Client Error: Not Found"}
        mock_get.return_value = mock_response

        with self.assertRaises(OuraNotFoundError):
            self.client.ring_configuration.get_ring_configuration_document(document_id)


class TestPersonal(unittest.TestCase):
    def setUp(self):
        self.client = OuraClient(access_token="test_token")
        self.base_url = self.client.BASE_URL

    @patch("requests.get")
    def test_get_personal_info_success(self, mock_get):
        mock_response_data = {
            "id": "user_123",
            "email": "test@example.com",
            "age": 30,
            "weight": 70.5,
            "height": 175.0,
            "biological_sex": "male",
            "birth_date": "1993-05-15"
        }
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        response = self.client.personal.get_personal_info()
        self.assertIsInstance(response, PersonalInfo)
        self.assertEqual(response.id, "user_123")
        self.assertEqual(response.email, "test@example.com")
        self.assertEqual(response.age, 30)
        self.assertEqual(response.weight, 70.5)
        self.assertEqual(response.height, 175.0)
        self.assertEqual(response.biological_sex, "male")
        self.assertEqual(response.birth_date, date(1993, 5, 15))

        mock_get.assert_called_once_with(
            f"{self.base_url}/usercollection/personal_info",
            headers=self.client.headers,
            params=None,
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_personal_info_raw_response(self, mock_get):
        mock_response_data = {
            "id": "user_123",
            "email": "test@example.com",
            "age": 30,
            "weight": 70.5,
            "height": 175.0,
            "biological_sex": "male",
            "birth_date": "1993-05-15"
        }
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        response = self.client.personal.get_personal_info(return_model=False)
        self.assertIsInstance(response, dict)
        self.assertEqual(response["id"], "user_123")
        self.assertEqual(response["email"], "test@example.com")
        self.assertEqual(response["age"], 30)

        mock_get.assert_called_once_with(
            f"{self.base_url}/usercollection/personal_info",
            headers=self.client.headers,
            params=None,
            timeout=30.0,
        )

    @patch("requests.get")
    def test_get_personal_info_api_error_401(self, mock_get):
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 401
        mock_response.reason = "Unauthorized"
        mock_response.json.return_value = {"error": "401 Client Error: Unauthorized"}
        mock_get.return_value = mock_response

        with self.assertRaises(Exception):  # Specific exception depends on error handling implementation
            self.client.personal.get_personal_info()

    @patch("requests.get")
    def test_get_personal_info_minimal_data(self, mock_get):
        mock_response_data = {
            "id": "user_456",
            "email": "minimal@example.com",
            "age": 25
        }
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        response = self.client.personal.get_personal_info()
        self.assertIsInstance(response, PersonalInfo)
        self.assertEqual(response.id, "user_456")
        self.assertEqual(response.email, "minimal@example.com")
        self.assertEqual(response.age, 25)
        self.assertIsNone(response.weight)
        self.assertIsNone(response.height)
        self.assertIsNone(response.biological_sex)
        self.assertIsNone(response.birth_date)
