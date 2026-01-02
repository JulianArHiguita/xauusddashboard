import pandas as pd
import ta
import numpy as np

def calculate_indicators(df: pd.DataFrame):
    """
    Adds technical indicators to the dataframe.
    """
    if df is None or df.empty:
        return df

    # Ensure we use the correct column for price
    close = df['Close']
    high = df['High']
    low = df['Low']
    volume = df['Volume'] if 'Volume' in df.columns else pd.Series([0]*len(df), index=df.index)

    # RSI (14)
    df['RSI'] = ta.momentum.RSIIndicator(close=close, window=14).rsi()

    # MACD (12, 26, 9)
    macd = ta.trend.MACD(close=close, window_slow=26, window_fast=12, window_sign=9)
    df['MACD'] = macd.macd()
    df['MACD_Signal'] = macd.macd_signal()
    df['MACD_Hist'] = macd.macd_diff()

    # Bollinger Bands (20, 2)
    bb = ta.volatility.BollingerBands(close=close, window=20, window_dev=2)
    df['BB_High'] = bb.bollinger_hband()
    df['BB_Low'] = bb.bollinger_lband()
    df['BB_Mid'] = bb.bollinger_mavg()
    
    # EMAs
    df['EMA_50'] = ta.trend.EMAIndicator(close=close, window=50).ema_indicator()
    df['EMA_200'] = ta.trend.EMAIndicator(close=close, window=200).ema_indicator()

    # ATR for Volatility/Risk
    atr = ta.volatility.AverageTrueRange(high=high, low=low, close=close, window=14)
    df['ATR'] = atr.average_true_range()

    return df

def generate_signal(df: pd.DataFrame):
    """
    Analyzes the latest candle to generate a signal.
    Returns: Score (-1 to 1), Recommendation (BUY/SELL/NEUTRAL), details
    """
    if df is None or df.empty:
        return {"recommendation": "NEUTRAL", "confidence": 0, "reason": "No Data"}

    # Get latest complete candle (iloc[-1])
    # Note: latest candle might be incomplete if market is open. 
    # For signals, often better to look at closed candles (iloc[-2]) or treat -1 as live.
    # We will use latest for real-time feel.
    
    latest = df.iloc[-1]
    
    score = 0
    reasons = []

    # RSI Logic
    rsi = latest['RSI']
    if rsi < 30:
        score += 2
        reasons.append("RSI Oversold (<30)")
    elif rsi > 70:
        score -= 2
        reasons.append("RSI Overbought (>70)")
    elif rsi > 50:
        score += 0.5
    else:
        score -= 0.5

    # MACD Logic
    if latest['MACD'] > latest['MACD_Signal']:
        score += 1.5
        reasons.append("MACD Bullish Crossover")
    else:
        score -= 1.5
        reasons.append("MACD Bearish Crossover")

    # EMA Trend
    price = latest['Close']
    if price > latest['EMA_50']:
        score += 1
        reasons.append("Price above EMA 50")
    else:
        score -= 1
        reasons.append("Price below EMA 50")

    # Final Decision
    confidence = min(abs(score) / 5 * 100, 100) # Normalize roughly
    
    if score >= 1.5:
        recommendation = "BUY"
    elif score <= -1.5:
        recommendation = "SELL"
    else:
        recommendation = "NEUTRAL"
        
    return {
        "recommendation": recommendation,
        "score": score,
        "confidence": round(confidence, 1),
        "reasons": reasons,
        "rsi": round(rsi, 2),
        "price": round(price, 2)
    }

def get_risk_levels(price, atr, recommendation):
    """
    Calculates dynamic SL/TP based on ATR.
    """
    sl = 0.0
    tp = 0.0
    
    # 1.5 ATR for SL, 3.0 ATR for TP (1:2 Risk/Reward)
    risk_margin = atr * 1.5
    reward_margin = atr * 3.0
    
    if recommendation == "BUY":
        sl = price - risk_margin
        tp = price + reward_margin
    elif recommendation == "SELL":
        sl = price + risk_margin
        tp = price - reward_margin
    else:
        # For Neutral, give a range
        sl = price - risk_margin
        tp = price + risk_margin
        
    return {
        "stop_loss": round(sl, 2),
        "take_profit": round(tp, 2),
        "risk_reward_ratio": "1:2"
    }
