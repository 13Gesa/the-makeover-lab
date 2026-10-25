"""
Einfache Handelsstrategien als Einstieg.
"""
import pandas as pd
from analysis.indicators import sma, rsi, add_all_indicators


def golden_cross_strategy(df: pd.DataFrame) -> pd.DataFrame:
    """
    Golden/Death Cross: Kaufsignal wenn SMA20 über SMA50 kreuzt,
    Verkaufssignal wenn SMA20 unter SMA50 fällt.
    """
    df = df.copy()
    df["SMA_20"] = sma(df["Close"], 20)
    df["SMA_50"] = sma(df["Close"], 50)
    df["Signal"] = 0
    df.loc[df["SMA_20"] > df["SMA_50"], "Signal"] = 1   # Long
    df.loc[df["SMA_20"] < df["SMA_50"], "Signal"] = -1  # Short/Cash
    df["Position"] = df["Signal"].diff()
    return df


def rsi_strategy(df: pd.DataFrame, oversold: int = 30, overbought: int = 70) -> pd.DataFrame:
    """
    RSI-Strategie: Kaufen bei Überverkauft (<30), Verkaufen bei Überkauft (>70).
    """
    df = df.copy()
    df["RSI"] = rsi(df["Close"])
    df["Signal"] = 0
    df.loc[df["RSI"] < oversold, "Signal"] = 1    # Kaufsignal
    df.loc[df["RSI"] > overbought, "Signal"] = -1  # Verkaufssignal
    df["Position"] = df["Signal"].diff()
    return df


def get_latest_signals(df: pd.DataFrame, strategy_fn) -> dict:
    """Aktuellste Signale für ein Symbol zurückgeben."""
    result = strategy_fn(df)
    latest = result.iloc[-1]
    return {
        "date": result.index[-1],
        "close": round(latest["Close"], 2),
        "signal": latest["Signal"],
        "signal_text": {1: "KAUFEN", -1: "VERKAUFEN", 0: "HALTEN"}.get(latest["Signal"], "–"),
    }
