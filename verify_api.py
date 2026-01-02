import sys
import os
import logging

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

try:
    from backend.data_service import get_current_price, get_historical_data
    
    print("Testing Twelve Data API Integration...")
    
    # 1. Test Current Price
    print("\n[1] Fetching Current Price...")
    price_data = get_current_price()
    if price_data:
        print(f"SUCCESS: {price_data}")
    else:
        print("FAILED: Could not fetch current price.")

    # 2. Test History
    print("\n[2] Fetching Historical Data (1h)...")
    history = get_historical_data(interval="1h")
    if history is not None and not history.empty:
        print(f"SUCCESS: Retrieved {len(history)} candles.")
        print(history.head(1).to_string())
    else:
        print("FAILED: Could not fetch history.")

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
