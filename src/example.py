#!/usr/bin/env python3
"""Example usage of the Oura API client."""

import os
from datetime import datetime, timedelta
import json
from oura_api_client.api.client import OuraClient


def main():
    """Run a demo of the Oura API client."""
    # Get API token from environment variable
    token = os.environ.get("OURA_API_TOKEN")

    if not token:
        print("Please set the OURA_API_TOKEN environment variable")
        return

    # Initialize the client
    client = OuraClient(token)

    # Get heart rate data for the last 7 days
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    try:
        # Get heart rate data as a model
        heart_rate = client.heartrate.get_heartrate(
            start_date=start_date, end_date=end_date
        )
        print(f"Retrieved {len(heart_rate.data)} heart rate samples")

        if heart_rate.data:
            # Display the first 3 samples
            for sample in heart_rate.data[:3]:
                print(
                    f"Time: {sample.timestamp}, BPM: {sample.bpm}, Source: {sample.source}"
                )

        # Get heart rate data as raw JSON
        heart_rate_raw = client.heartrate.get_heartrate(
            start_date=start_date, end_date=end_date, return_model=False
        )

        # Save raw data to file
        with open("heart_rate_data.json", "w") as f:
            json.dump(heart_rate_raw, f, indent=2)

        print("Saved raw heart rate data to heart_rate_data.json")

        # Get personal info
        personal_info = client.personal.get_personal_info()
        print(f"\nUser ID: {personal_info.id}")
        print(f"Email: {personal_info.email}")
        print(f"Age: {personal_info.age}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
