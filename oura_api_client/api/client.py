"""Oura API client implementation."""

import requests
from typing import Optional, Dict, Any

from ..exceptions import create_api_error, OuraConnectionError, OuraTimeoutError
from ..utils import RetryConfig, retry_with_backoff

from .heartrate import HeartRateEndpoints
from .personal import PersonalEndpoints
from .daily_activity import DailyActivity
from .daily_sleep import DailySleep
from .daily_readiness import DailyReadiness
from .sleep import Sleep
from .session import Session
from .tag import Tag
from .workout import Workout
from .enhanced_tag import EnhancedTag
from .daily_spo2 import DailySpo2
from .sleep_time import SleepTime
from .rest_mode_period import RestModePeriod
from .ring_configuration import RingConfiguration
from .daily_stress import DailyStress
from .daily_resilience import DailyResilience
from .daily_cardiovascular_age import DailyCardiovascularAge
from .vo2_max import Vo2Max
from .webhook import Webhook


class OuraClient:
    """Client for interacting with the Oura API v2."""

    BASE_URL = "https://api.ouraring.com/v2"

    def __init__(
        self, 
        access_token: str, 
        retry_config: Optional[RetryConfig] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None
    ):
        """Initialize the Oura client with an access token.

        Args:
            access_token (str): Your Oura API personal access token
            retry_config (RetryConfig, optional): Configuration for retry behavior
            client_id (str, optional): Client ID for webhook operations
            client_secret (str, optional): Client secret for webhook operations
        """
        self.access_token = access_token
        self.client_id = client_id
        self.client_secret = client_secret
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        self.retry_config = retry_config or RetryConfig()

        # Initialize endpoint modules
        self.heartrate = HeartRateEndpoints(self)
        self.personal = PersonalEndpoints(self)
        self.daily_activity = DailyActivity(self)
        self.daily_sleep = DailySleep(self)
        self.daily_readiness = DailyReadiness(self)
        self.sleep = Sleep(self)
        self.session = Session(self)
        self.tag = Tag(self)
        self.workout = Workout(self)
        self.enhanced_tag = EnhancedTag(self)
        self.daily_spo2 = DailySpo2(self)
        self.sleep_time = SleepTime(self)
        self.rest_mode_period = RestModePeriod(self)
        self.ring_configuration = RingConfiguration(self)
        self.daily_stress = DailyStress(self)
        self.daily_resilience = DailyResilience(self)
        self.daily_cardiovascular_age = DailyCardiovascularAge(self)
        self.vo2_max = Vo2Max(self)
        self.webhook = Webhook(self)

    def _make_request(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        method: str = "GET",
        timeout: Optional[float] = 30.0,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make a request to the Oura API.

        Args:
            endpoint (str): The API endpoint to call (should start with /)
            params (dict, optional): Query parameters for the request
            method (str): HTTP method to use (default: GET)
            timeout (float, optional): Request timeout in seconds
            json_data (dict, optional): JSON data for request body (POST/PUT/PATCH)
            headers (dict, optional): Additional headers to merge with default headers

        Returns:
            dict: The JSON response from the API

        Raises:
            OuraAPIError: If the API request fails with specific error details
        """
        # Ensure endpoint starts with /
        if not endpoint.startswith('/'):
            endpoint = f"/{endpoint}"
        
        # Remove any duplicate /v2 prefix if present
        if endpoint.startswith('/v2/'):
            endpoint = endpoint[3:]  # Remove '/v2' prefix
        
        url = f"{self.BASE_URL}{endpoint}"

        # Wrap the actual request in retry logic if enabled
        if self.retry_config.enabled:
            return self._make_request_with_retry(url, method, params, timeout, endpoint, json_data, headers)
        else:
            return self._make_single_request(url, method, params, timeout, endpoint, json_data, headers)

    def _make_single_request(
        self,
        url: str,
        method: str,
        params: Optional[Dict[str, Any]],
        timeout: Optional[float],
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make a single HTTP request without retry logic.
        
        Args:
            url: Full URL to request
            method: HTTP method
            params: Query parameters
            timeout: Request timeout
            endpoint: Original endpoint for error context
            json_data: JSON data for request body
            headers: Additional headers to merge with default headers
            
        Returns:
            dict: The JSON response from the API
            
        Raises:
            OuraAPIError: If the request fails
        """
        try:
            # Merge headers with default client headers
            request_headers = self.headers.copy()
            if headers:
                request_headers.update(headers)

            method_upper = method.upper()
            if method_upper == "GET":
                response = requests.get(url, headers=request_headers, params=params, timeout=timeout)
            elif method_upper == "POST":
                if json_data is not None:
                    response = requests.post(url, headers=request_headers, params=params, json=json_data, timeout=timeout)
                else:
                    response = requests.post(url, headers=request_headers, params=params, timeout=timeout)
            elif method_upper == "PUT":
                if json_data is not None:
                    response = requests.put(url, headers=request_headers, params=params, json=json_data, timeout=timeout)
                else:
                    response = requests.put(url, headers=request_headers, params=params, timeout=timeout)
            elif method_upper == "PATCH":
                if json_data is not None:
                    response = requests.patch(url, headers=request_headers, params=params, json=json_data, timeout=timeout)
                else:
                    response = requests.patch(url, headers=request_headers, params=params, timeout=timeout)
            elif method_upper == "DELETE":
                response = requests.delete(url, headers=request_headers, params=params, timeout=timeout)
            else:
                raise ValueError(f"HTTP method {method} is not supported")

            # Check for HTTP errors
            if not response.ok:
                raise create_api_error(response, endpoint)

            # Handle empty responses (e.g., for DELETE requests)
            if response.status_code == 204 or not response.content.strip():
                return {}
            
            return response.json()

        except requests.exceptions.Timeout as e:
            raise OuraTimeoutError(f"Request timed out after {timeout} seconds", endpoint=endpoint) from e
        except requests.exceptions.ConnectionError as e:
            raise OuraConnectionError(f"Failed to connect to API: {str(e)}", endpoint=endpoint) from e
        except requests.exceptions.RequestException as e:
            raise create_api_error(getattr(e, 'response', None), endpoint, str(e)) from e

    def _make_request_with_retry(
        self,
        url: str,
        method: str,
        params: Optional[Dict[str, Any]],
        timeout: Optional[float],
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make HTTP request with retry logic.
        
        Args:
            url: Full URL to request
            method: HTTP method
            params: Query parameters
            timeout: Request timeout
            endpoint: Original endpoint for error context
            json_data: JSON data for request body
            headers: Additional headers to merge with default headers
            
        Returns:
            dict: The JSON response from the API
            
        Raises:
            OuraAPIError: If all retries fail
        """
        @retry_with_backoff(
            max_retries=self.retry_config.max_retries,
            base_delay=self.retry_config.base_delay,
            max_delay=self.retry_config.max_delay,
            jitter=self.retry_config.jitter
        )
        def make_request():
            return self._make_single_request(url, method, params, timeout, endpoint, json_data, headers)
        
        return make_request()
