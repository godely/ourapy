"""Tests for pagination helpers functionality."""

import unittest
from unittest.mock import Mock, MagicMock
from datetime import date

from oura_api_client.utils.pagination import stream_paginated_data
from oura_api_client.api.daily_sleep import DailySleep
from oura_api_client.api.daily_activity import DailyActivity
from oura_api_client.api.heartrate import HeartRateEndpoints
from oura_api_client.api.session import Session
from oura_api_client.models.daily_sleep import DailySleepResponse, DailySleepModel, SleepContributors
from oura_api_client.models.daily_activity import DailyActivityResponse, DailyActivityModel, ActivityContributors
from oura_api_client.models.heartrate import HeartRateResponse, HeartRateSample
from oura_api_client.models.session import SessionResponse, SessionModel


class MockResponse:
    """Mock response class for testing pagination."""
    
    def __init__(self, data, next_token=None):
        self.data = data
        self.next_token = next_token


class TestPaginationUtils(unittest.TestCase):
    """Test the core pagination utility functions."""

    def test_stream_paginated_data_single_page(self):
        """Test pagination with a single page of results."""
        # Mock response with no next_token
        mock_response = MockResponse(data=[1, 2, 3], next_token=None)
        
        # Mock fetch function
        mock_fetch = Mock(return_value=mock_response)
        
        # Stream the data
        results = list(stream_paginated_data(mock_fetch, start_date="2024-01-01"))
        
        # Verify results
        self.assertEqual(results, [1, 2, 3])
        mock_fetch.assert_called_once_with(
            start_date="2024-01-01",
            end_date=None,
            next_token=None
        )

    def test_stream_paginated_data_multiple_pages(self):
        """Test pagination with multiple pages of results."""
        # Mock responses for multiple pages
        page1 = MockResponse(data=[1, 2], next_token="token_page2")
        page2 = MockResponse(data=[3, 4], next_token="token_page3")
        page3 = MockResponse(data=[5], next_token=None)
        
        # Mock fetch function that returns different pages
        mock_fetch = Mock(side_effect=[page1, page2, page3])
        
        # Stream the data
        results = list(stream_paginated_data(
            mock_fetch,
            start_date="2024-01-01",
            end_date="2024-01-31"
        ))
        
        # Verify results
        self.assertEqual(results, [1, 2, 3, 4, 5])
        
        # Verify the fetch function was called correctly for each page
        expected_calls = [
            unittest.mock.call(start_date="2024-01-01", end_date="2024-01-31", next_token=None),
            unittest.mock.call(start_date="2024-01-01", end_date="2024-01-31", next_token="token_page2"),
            unittest.mock.call(start_date="2024-01-01", end_date="2024-01-31", next_token="token_page3")
        ]
        mock_fetch.assert_has_calls(expected_calls)

    def test_stream_paginated_data_with_kwargs(self):
        """Test pagination with additional keyword arguments."""
        mock_response = MockResponse(data=[1, 2, 3], next_token=None)
        mock_fetch = Mock(return_value=mock_response)
        
        results = list(stream_paginated_data(
            mock_fetch,
            start_date="2024-01-01",
            custom_param="test_value"
        ))
        
        self.assertEqual(results, [1, 2, 3])
        mock_fetch.assert_called_once_with(
            start_date="2024-01-01",
            end_date=None,
            next_token=None,
            custom_param="test_value"
        )


class TestEndpointStreamMethods(unittest.TestCase):
    """Test the stream methods on endpoint classes."""

    def setUp(self):
        """Set up mock client for testing."""
        self.mock_client = Mock()

    def test_daily_sleep_stream(self):
        """Test DailySleep stream method."""
        # Create endpoint instance
        endpoint = DailySleep(self.mock_client)
        
        # Mock the get_daily_sleep_documents method
        mock_data = [
            DailySleepModel(
                id="1", 
                contributors=SleepContributors(), 
                day=date.today(), 
                timestamp="2024-01-01T00:00:00"
            ),
            DailySleepModel(
                id="2", 
                contributors=SleepContributors(), 
                day=date.today(), 
                timestamp="2024-01-02T00:00:00"
            )
        ]
        mock_response = MockResponse(data=mock_data, next_token=None)
        endpoint.get_daily_sleep_documents = Mock(return_value=mock_response)
        
        # Test streaming
        results = list(endpoint.stream(start_date="2024-01-01"))
        
        # Verify results
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].id, "1")
        self.assertEqual(results[1].id, "2")
        
        # Verify the method was called correctly
        endpoint.get_daily_sleep_documents.assert_called_once_with(
            start_date="2024-01-01",
            end_date=None,
            next_token=None
        )

    def test_daily_activity_stream(self):
        """Test DailyActivity stream method."""
        endpoint = DailyActivity(self.mock_client)
        
        # Mock data
        mock_data = [
            DailyActivityModel(
                id="1", 
                day=date.today(), 
                timestamp="2024-01-01T00:00:00",
                contributors=ActivityContributors()
            ),
            DailyActivityModel(
                id="2", 
                day=date.today(), 
                timestamp="2024-01-02T00:00:00",
                contributors=ActivityContributors()
            )
        ]
        mock_response = MockResponse(data=mock_data, next_token=None)
        endpoint.get_daily_activity_documents = Mock(return_value=mock_response)
        
        # Test streaming
        results = list(endpoint.stream(start_date="2024-01-01"))
        
        # Verify results
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].id, "1")
        
    def test_heartrate_stream(self):
        """Test HeartRateEndpoints stream method."""
        endpoint = HeartRateEndpoints(self.mock_client)
        
        # Mock data
        mock_data = [
            HeartRateSample(timestamp="2024-01-01T12:00:00", bpm=70, source="ring"),
            HeartRateSample(timestamp="2024-01-01T12:01:00", bpm=72, source="ring")
        ]
        mock_response = MockResponse(data=mock_data, next_token=None)
        endpoint.get_heartrate = Mock(return_value=mock_response)
        
        # Test streaming
        results = list(endpoint.stream(start_date="2024-01-01"))
        
        # Verify results
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].bpm, 70)
        self.assertEqual(results[1].bpm, 72)

    def test_session_stream(self):
        """Test Session stream method."""
        endpoint = Session(self.mock_client)
        
        # Mock data with required fields
        mock_data = [
            SessionModel(
                id="1", 
                day=date.today(), 
                timestamp="2024-01-01T00:00:00",
                start_datetime="2024-01-01T10:00:00",
                end_datetime="2024-01-01T11:00:00",
                type="workout"
            ),
            SessionModel(
                id="2", 
                day=date.today(), 
                timestamp="2024-01-02T00:00:00",
                start_datetime="2024-01-02T10:00:00",
                end_datetime="2024-01-02T11:00:00",
                type="workout"
            )
        ]
        mock_response = MockResponse(data=mock_data, next_token=None)
        endpoint.get_session_documents = Mock(return_value=mock_response)
        
        # Test streaming with date objects
        results = list(endpoint.stream(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31)
        ))
        
        # Verify results
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].id, "1")

    def test_stream_multiple_pages(self):
        """Test streaming across multiple pages."""
        endpoint = DailySleep(self.mock_client)
        
        # Mock multiple pages
        page1_data = [DailySleepModel(
            id="1", 
            contributors=SleepContributors(), 
            day=date.today(), 
            timestamp="2024-01-01T00:00:00"
        )]
        page2_data = [DailySleepModel(
            id="2", 
            contributors=SleepContributors(), 
            day=date.today(), 
            timestamp="2024-01-02T00:00:00"
        )]
        
        page1 = MockResponse(data=page1_data, next_token="token2")
        page2 = MockResponse(data=page2_data, next_token=None)
        
        endpoint.get_daily_sleep_documents = Mock(side_effect=[page1, page2])
        
        # Test streaming
        results = list(endpoint.stream(start_date="2024-01-01"))
        
        # Verify we got data from both pages
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].id, "1")
        self.assertEqual(results[1].id, "2")
        
        # Verify correct pagination calls
        expected_calls = [
            unittest.mock.call(start_date="2024-01-01", end_date=None, next_token=None),
            unittest.mock.call(start_date="2024-01-01", end_date=None, next_token="token2")
        ]
        endpoint.get_daily_sleep_documents.assert_has_calls(expected_calls)


if __name__ == "__main__":
    unittest.main()