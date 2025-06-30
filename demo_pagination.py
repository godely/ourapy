#!/usr/bin/env python3
"""
Demonstration of the new pagination helpers in the Oura API client.

This script shows how to use the new .stream() methods for seamless pagination.
"""

import os
from datetime import date, timedelta
from oura_api_client.api.client import OuraClient


def demo_pagination_helpers():
    """Demonstrate the pagination helpers functionality."""
    
    print("🔄 Oura API Pagination Helpers Demo")
    print("=" * 50)
    
    # Note: This demo shows the API usage but won't make real calls
    # without a valid access token and data
    
    print("\n1. Setting up client...")
    # Use a dummy token for demo (replace with real token for actual use)
    client = OuraClient(access_token="demo_token_here")
    
    print("\n2. NEW: Seamless pagination with .stream() methods")
    print("-" * 50)
    
    # Calculate date range for last 7 days
    end_date = date.today() 
    start_date = end_date - timedelta(days=7)
    
    print(f"\n🛌 Streaming sleep data from {start_date} to {end_date}:")
    print("for sleep_record in client.daily_sleep.stream(start_date='2024-01-01'):")
    print("    print(f'Date: {sleep_record.day}, Score: {sleep_record.score}')")
    
    print(f"\n💓 Streaming heart rate data:")
    print("for hr_sample in client.heartrate.stream(start_date='2024-01-01'):")
    print("    print(f'HR: {hr_sample.bpm} at {hr_sample.timestamp}')")
    
    print(f"\n🏃 Streaming activity data:")
    print("for activity in client.daily_activity.stream(start_date='2024-01-01'):")
    print("    print(f'Steps: {activity.steps}, Calories: {activity.active_calories}')")
    
    print(f"\n⚡ Streaming readiness data:")
    print("for readiness in client.daily_readiness.stream(start_date='2024-01-01'):")
    print("    print(f'Readiness: {readiness.score}')")
    
    print(f"\n🏋️ Streaming session data:")
    print("for session in client.session.stream(start_date='2024-01-01'):")
    print("    print(f'Session: {session.type} from {session.start_datetime}')")
    
    print("\n3. Benefits of the new approach:")
    print("-" * 50)
    print("✅ No manual pagination logic needed")
    print("✅ Memory efficient - items yielded one at a time") 
    print("✅ Pythonic iteration with simple for loops")
    print("✅ Automatic handling of next_token parameters")
    print("✅ Works with date ranges and filtering")
    print("✅ No breaking changes to existing code")
    
    print("\n4. Advanced: Collecting all data")
    print("-" * 50)
    print("# Collect all items into a list if needed:")
    print("all_sleep_data = list(client.daily_sleep.stream(start_date='2024-01-01'))")
    print("print(f'Total records: {len(all_sleep_data)}')")
    
    print("\n5. Advanced: Processing with filters")
    print("-" * 50)
    print("# Process only high-quality sleep records:")
    print("high_quality_sleep = [")
    print("    record for record in client.daily_sleep.stream(start_date='2024-01-01')")
    print("    if record.score and record.score > 80")
    print("]")
    
    print("\n🎉 The pagination helpers make working with Oura data much simpler!")
    print("   Check the README for more examples and usage patterns.")


if __name__ == "__main__":
    demo_pagination_helpers()