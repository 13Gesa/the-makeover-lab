"""
Technische Indikatoren für Trading-Analyse.
"""
import pandas as pd
import numpy as np


def sma(series: pd.Series, window: int) -> pd.Series:
    """Simple Moving Average."""
    return series.rolling(window=window).mean()


def ema(series: pd.Series, window: int) -> pd.Series:
    """Exponential Moving Average."""
    return series.ewm(span=window, adjust=False).mean()


def rsi(series: pd.Series, window: int = 14) -> pd.Series:
    """Relative Strength Index (0–100). Über 70 = überkauft, unter 30 = überverkauft."""
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(window).mean()
    loss = (-delta.clip(upper=0)).rolling(window).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def macd(series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
    """MACD Linie, Signal-Linie und Histogramm."""
    macd_line = ema(series, fast) - ema(series, slow)
    signal_line = ema(macd_line, signal)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def bollinger_bands(series: pd.Series, window: int = 20, num_std: float = 2.0):
    """Bollinger Bänder: Mitte, Obere, Untere."""
    mid = sma(series, window)
    std = series.rolling(window).std()
    upper = mid + num_std * std
    lower = mid - num_std * std
    return mid, upper, lower


def add_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Alle Indikatoren auf einen OHLCV-DataFrame anwenden."""
    close = df["Close"]
    df["SMA_20"] = sma(close, 20)
    df["SMA_50"] = sma(close, 50)
    df["EMA_12"] = ema(close, 12)
    df["EMA_26"] = ema(close, 26)
    df["RSI"] = rsi(close)
    df["MACD"], df["MACD_Signal"], df["MACD_Hist"] = macd(close)
    df["BB_Mid"], df["BB_Upper"], df["BB_Lower"] = bollinger_bands(close)
    return df
