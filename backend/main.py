from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from data_service import get_historical_data, get_current_price
from analysis import calculate_indicators, generate_signal, get_risk_levels
import pandas as pd

app = FastAPI(title="XAUUSD Analysis Dashboard API")

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/market-data/current")
def get_current_market_data():
    """
    Returns real-time price info.
    """
    return get_current_price()

@app.get("/api/analysis")
def get_analysis_data(timeframe: str = Query("1h", enum=["5m", "15m", "1h"])):
    """
    Returns historical data + indicators + signal for a specific timeframe.
    """
    period_map = {
        "5m": "5d", 
        "15m": "5d",
        "1h": "1mo"
    }
    
    period = period_map.get(timeframe, "1mo")
    df = get_historical_data(period=period, interval=timeframe)
    
    if df is None:
        return {"error": "Failed to fetch data"}
    
    # Calculate indicators
    df = calculate_indicators(df)
    
    # Generate signal based on latest data
    signal = generate_signal(df)
    
    # Risk
    risk = get_risk_levels(signal['price'], df['ATR'].iloc[-1], signal['recommendation'])
    
    # Convert latest 100 candles to JSON for chart
    # Front-end typically needs [ {time, open, high, low, close}, ... ]
    chart_data = []
    # Take last 200 candles for performance
    subset = df.tail(200).copy()
    
    for i, row in subset.iterrows():
        # Handle datetime - convert to Unix timestamp for Lightweight Charts
        dt = row.get('Datetime', row.get('Date', ''))
        
        # Convert to Unix timestamp (seconds since epoch)
        if hasattr(dt, 'timestamp'):
            timestamp = int(dt.timestamp())
        else:
            # Parse string and convert
            from datetime import datetime as dt_module
            if isinstance(dt, str):
                try:
                    parsed = dt_module.fromisoformat(dt.replace('Z', '+00:00'))
                    timestamp = int(parsed.timestamp())
                except:
                    timestamp = int(dt_module.now().timestamp())
            else:
                timestamp = int(dt_module.now().timestamp())
        
        item = {
            "time": timestamp,
            "open": float(row['Open']),
            "high": float(row['High']),
            "low": float(row['Low']),
            "close": float(row['Close']),
            "volume": float(row.get('Volume', 0)),
            # Add indicators if needed for drawing
            "ema50": None if pd.isna(row.get('EMA_50')) else float(row['EMA_50']),
            "ema200": None if pd.isna(row.get('EMA_200')) else float(row['EMA_200']),
            "bb_upper": None if pd.isna(row.get('BB_High')) else float(row['BB_High']),
            "bb_lower": None if pd.isna(row.get('BB_Low')) else float(row['BB_Low'])
        }
        chart_data.append(item)
        
    return {
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

@app.get("/api/recommendation/summary")
def get_full_summary():
    """
    Aggregates signals from all timeframes to give a master recommendation.
    """
    timeframes = ["5m", "15m", "1h"]
    results = {}
    total_score = 0
    
    for tf in timeframes:
        period = "5d" if tf != "1h" else "1mo"
        df = get_historical_data(period=period, interval=tf)
        if df is not None:
             df = calculate_indicators(df)
             sig = generate_signal(df)
             results[tf] = sig
             total_score += sig['score'] # Simple sum
    
    # Final weighting
    # 1h is trend, 15m is setup, 5m is trigger
    # Current logic just sums them up.
    
    if total_score >= 3:
        master_call = "STRONG BUY"
    elif total_score >= 1:
        master_call = "BUY"
    elif total_score <= -3:
        master_call = "STRONG SELL"
    elif total_score <= -1:
        master_call = "SELL"
    else:
        master_call = "NEUTRAL"
        
    return {
        "master_recommendation": master_call,
        "total_score": total_score,
        "timeframe_breakdown": results
    }
