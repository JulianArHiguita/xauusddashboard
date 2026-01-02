import sys
import os
import traceback
import json

sys.path.append(os.path.join(os.getcwd(), 'backend'))

try:
    from backend.data_service import get_historical_data
    from backend.analysis import calculate_indicators, generate_signal, get_risk_levels
    import pandas as pd
    
    print("=== Testing Full API Flow ===\n")
    
    # Simulate what main.py does
    timeframe = "1h"
    period = "1mo"
    
    print(f"1. Fetching data for {timeframe}...")
    df = get_historical_data(period=period, interval=timeframe)
    
    if df is None:
        print("ERROR: Data is None")
        sys.exit(1)
        
    print(f"   ✓ Retrieved {len(df)} candles\n")
    
    print("2. Calculating indicators...")
    df = calculate_indicators(df)
    print(f"   ✓ Indicators calculated\n")
    
    print("3. Generating signal...")
    signal = generate_signal(df)
    print(f"   ✓ Signal: {signal['recommendation']}\n")
    
    print("4. Calculating risk levels...")
    risk = get_risk_levels(signal['price'], df['ATR'].iloc[-1], signal['recommendation'])
    print(f"   ✓ SL: {risk['stop_loss']}, TP: {risk['take_profit']}\n")
    
    print("5. Converting chart data to JSON format...")
    chart_data = []
    subset = df.tail(200).copy()
    
    for i, row in subset.iterrows():
        dt_str = row['Datetime'] if 'Datetime' in row else str(row.get('Date', ''))
        
        # Convert datetime to string if needed
        if hasattr(dt_str, 'strftime'):
            dt_str = dt_str.strftime('%Y-%m-%dT%H:%M:%S')
        
        item = {
            "time": dt_str,
            "open": float(row['Open']),
            "high": float(row['High']),
            "low": float(row['Low']),
            "close": float(row['Close']),
            "volume": float(row.get('Volume', 0)),
            "ema50": None if pd.isna(row.get('EMA_50')) else float(row['EMA_50']),
            "ema200": None if pd.isna(row.get('EMA_200')) else float(row['EMA_200']),
            "bb_upper": None if pd.isna(row.get('BB_High')) else float(row['BB_High']),
            "bb_lower": None if pd.isna(row.get('BB_Low')) else float(row['BB_Low'])
        }
        chart_data.append(item)
    
    print(f"   ✓ Prepared {len(chart_data)} candles for chart\n")
    
    print("6. Testing JSON serialization...")
    response = {
        "timeframe": timeframe,
        "signal": {
            "recommendation": signal['recommendation'],
            "score": float(signal['score']),
            "confidence": float(signal['confidence']),
            "reasons": signal['reasons'],
            "rsi": float(signal['rsi']),
            "price": float(signal['price'])
        },
        "risk_management": risk,
        "chart_data": chart_data
    }
    
    json_output = json.dumps(response, indent=2)
    print(f"   ✓ JSON serialization successful ({len(json_output)} bytes)\n")
    
    print("=== ALL TESTS PASSED ===")
    print("\nSample chart data item:")
    print(json.dumps(chart_data[0], indent=2))

except Exception as e:
    print("\n=== ERROR ENCOUNTERED ===")
    traceback.print_exc()
    sys.exit(1)
