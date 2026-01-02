import sys
import os
import pandas as pd
import traceback

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

try:
    from backend.data_service import get_historical_data
    from backend.analysis import calculate_indicators, generate_signal
    
    print("Fetching data...")
    df = get_historical_data(interval="1h")
    
    if df is None:
        print("Data is None")
        sys.exit(1)
        
    print(f"Data columns: {df.columns}")
    print(f"Data types:\n{df.dtypes}")
    print(f"First row: {df.iloc[0].to_dict()}")
    
    print("Calculating indicators...")
    df = calculate_indicators(df)
    print("Indicators calculated.")
    print(f"Columns after indicators: {df.columns}")
    
    print("Generating signal...")
    signal = generate_signal(df)
    print("Signal generated.")
    print(signal)

except Exception:
    print("CRASHED:")
    traceback.print_exc()
