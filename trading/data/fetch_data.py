"""
Kursdaten von Yahoo Finance abrufen und lokal speichern.
"""
import yfinance as yf
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent


def get_stock_data(symbol: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
    """Kursdaten für ein Symbol laden."""
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period, interval=interval)
    df.index = pd.to_datetime(df.index)
    return df


def save_data(df: pd.DataFrame, symbol: str) -> None:
    df.to_csv(DATA_DIR / f"{symbol}.csv")
    print(f"Gespeichert: {symbol}.csv ({len(df)} Datenpunkte)")


def load_data(symbol: str) -> pd.DataFrame:
    path = DATA_DIR / f"{symbol}.csv"
    if not path.exists():
        raise FileNotFoundError(f"Keine Daten für {symbol}. Zuerst fetch ausführen.")
    return pd.read_csv(path, index_col=0, parse_dates=True)


if __name__ == "__main__":
    symbols = ["AAPL", "MSFT", "BTC-USD", "ETH-USD"]
    for sym in symbols:
        print(f"Lade {sym}...")
        df = get_stock_data(sym)
        save_data(df, sym)
