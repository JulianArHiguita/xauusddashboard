import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

try:
    from backend.analysis import generate_signal
    import pandas as pd
    
    print("Successfully imported backend modules.")
    
    # Create dummy data
    data = {
        'Close': [100, 101, 102, 103, 104, 105, 104, 103, 102, 101, 100, 99, 98, 97, 96],
        'High': [105] * 15,
        'Low': [95] * 15,
        'Volume': [1000] * 15,
        'RSI': [25] * 15, # Oversold
        'MACD': [1] * 15,
        'MACD_Signal': [0] * 15,
        'EMA_50': [110] * 15,
        'ATR': [2] * 15
    }
    df = pd.DataFrame(data)
    
    print("Testing Signal Generation...")
    signal = generate_signal(df)
    print("Result:", signal)
    
    if signal['recommendation'] == 'BUY': # RSI < 30 should be bullish
        print("SUCCESS: Buy signal generated correctly for oversold condition.")
    else:
        print(f"WARNING: Unexpected signal {signal['recommendation']}")

except Exception as e:
    print(f"FAILED: {e}")
