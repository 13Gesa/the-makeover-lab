"""
Einfache Backtest-Engine: Strategie auf historischen Daten testen.
"""
import pandas as pd
import numpy as np


def run_backtest(df: pd.DataFrame, initial_capital: float = 10_000.0) -> dict:
    """
    Backtest für einen DataFrame mit 'Signal'-Spalte (1=Long, -1=Short/Cash, 0=Halten).
    Gibt Performance-Kennzahlen zurück.
    """
    df = df.copy().dropna(subset=["Signal"])
    df["Return"] = df["Close"].pct_change()
    df["Strategy_Return"] = df["Return"] * df["Signal"].shift(1)

    df["Equity"] = initial_capital * (1 + df["Strategy_Return"]).cumprod()
    df["Buy_Hold"] = initial_capital * (1 + df["Return"]).cumprod()

    total_return = (df["Equity"].iloc[-1] / initial_capital - 1) * 100
    bh_return = (df["Buy_Hold"].iloc[-1] / initial_capital - 1) * 100

    # Sharpe Ratio (annualisiert, risk-free = 0)
    sharpe = (df["Strategy_Return"].mean() / df["Strategy_Return"].std()) * np.sqrt(252)

    # Max Drawdown
    rolling_max = df["Equity"].cummax()
    drawdown = (df["Equity"] - rolling_max) / rolling_max
    max_drawdown = drawdown.min() * 100

    # Win Rate
    trades = df[df["Strategy_Return"] != 0]
    win_rate = (trades["Strategy_Return"] > 0).mean() * 100

    return {
        "start": str(df.index[0].date()),
        "end": str(df.index[-1].date()),
        "initial_capital": initial_capital,
        "final_equity": round(df["Equity"].iloc[-1], 2),
        "total_return_pct": round(total_return, 2),
        "buy_hold_return_pct": round(bh_return, 2),
        "sharpe_ratio": round(sharpe, 3),
        "max_drawdown_pct": round(max_drawdown, 2),
        "win_rate_pct": round(win_rate, 2),
        "num_trades": len(trades),
        "equity_series": df["Equity"],
        "buynhold_series": df["Buy_Hold"],
    }


def print_backtest_report(result: dict) -> None:
    print("\n" + "=" * 40)
    print("  BACKTEST-ERGEBNIS")
    print("=" * 40)
    print(f"  Zeitraum:          {result['start']} – {result['end']}")
    print(f"  Startkapital:      {result['initial_capital']:,.0f} €")
    print(f"  Endkapital:        {result['final_equity']:,.2f} €")
    print(f"  Strategie-Return:  {result['total_return_pct']:+.2f}%")
    print(f"  Buy & Hold:        {result['buy_hold_return_pct']:+.2f}%")
    print(f"  Sharpe Ratio:      {result['sharpe_ratio']:.3f}")
    print(f"  Max. Drawdown:     {result['max_drawdown_pct']:.2f}%")
    print(f"  Win Rate:          {result['win_rate_pct']:.1f}%")
    print(f"  Anzahl Trades:     {result['num_trades']}")
    print("=" * 40 + "\n")
