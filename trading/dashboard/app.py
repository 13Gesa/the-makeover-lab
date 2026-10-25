"""
Interaktives Trading-Dashboard mit Plotly Dash.
Starten: python dashboard/app.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

try:
    import dash
    from dash import dcc, html, Input, Output
    DASH_AVAILABLE = True
except ImportError:
    DASH_AVAILABLE = False

from data.fetch_data import load_data, get_stock_data
from analysis.indicators import add_all_indicators
from strategies.simple_strategy import golden_cross_strategy, rsi_strategy, get_latest_signals
from analysis.backtest import run_backtest, print_backtest_report


def create_chart(symbol: str = "AAPL", strategy: str = "golden_cross") -> go.Figure:
    """Chart mit Kursverlauf, Indikatoren und Signalen."""
    try:
        df = load_data(symbol)
    except FileNotFoundError:
        df = get_stock_data(symbol)

    df = add_all_indicators(df)
    strat_fn = golden_cross_strategy if strategy == "golden_cross" else rsi_strategy
    df = strat_fn(df)

    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                        row_heights=[0.6, 0.2, 0.2],
                        subplot_titles=[f"{symbol} Kurs", "MACD", "RSI"])

    # Candlestick
    fig.add_trace(go.Candlestick(x=df.index, open=df["Open"], high=df["High"],
                                  low=df["Low"], close=df["Close"], name="Kurs"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["SMA_20"], name="SMA 20",
                              line=dict(color="orange", width=1)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["SMA_50"], name="SMA 50",
                              line=dict(color="blue", width=1)), row=1, col=1)

    # Bollinger Bands
    fig.add_trace(go.Scatter(x=df.index, y=df["BB_Upper"], name="BB Oben",
                              line=dict(color="gray", dash="dot", width=1)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["BB_Lower"], name="BB Unten",
                              line=dict(color="gray", dash="dot", width=1),
                              fill="tonexty", fillcolor="rgba(128,128,128,0.1)"), row=1, col=1)

    # Kaufsignale
    buys = df[df["Position"] > 0]
    sells = df[df["Position"] < 0]
    fig.add_trace(go.Scatter(x=buys.index, y=buys["Close"], mode="markers",
                              marker=dict(symbol="triangle-up", size=10, color="green"),
                              name="Kaufsignal"), row=1, col=1)
    fig.add_trace(go.Scatter(x=sells.index, y=sells["Close"], mode="markers",
                              marker=dict(symbol="triangle-down", size=10, color="red"),
                              name="Verkaufssignal"), row=1, col=1)

    # MACD
    fig.add_trace(go.Scatter(x=df.index, y=df["MACD"], name="MACD",
                              line=dict(color="blue")), row=2, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["MACD_Signal"], name="Signal",
                              line=dict(color="orange")), row=2, col=1)
    fig.add_trace(go.Bar(x=df.index, y=df["MACD_Hist"], name="Histogramm",
                          marker_color=df["MACD_Hist"].apply(
                              lambda x: "green" if x >= 0 else "red")), row=2, col=1)

    # RSI
    fig.add_trace(go.Scatter(x=df.index, y=df["RSI"], name="RSI",
                              line=dict(color="purple")), row=3, col=1)
    fig.add_hline(y=70, line_dash="dot", line_color="red", row=3, col=1)
    fig.add_hline(y=30, line_dash="dot", line_color="green", row=3, col=1)

    fig.update_layout(height=800, template="plotly_dark", showlegend=True,
                      title=f"{symbol} — Trading-Analyse")
    fig.update_xaxes(rangeslider_visible=False)
    return fig


if __name__ == "__main__":
    if not DASH_AVAILABLE:
        print("Dash nicht installiert. Installieren mit: pip install dash")
        sys.exit(1)

    app = dash.Dash(__name__)
    SYMBOLS = ["AAPL", "MSFT", "GOOGL", "BTC-USD", "ETH-USD", "DAX"]

    app.layout = html.Div([
        html.H1("Trading Dashboard", style={"color": "white", "textAlign": "center"}),
        html.Div([
            dcc.Dropdown(id="symbol", options=[{"label": s, "value": s} for s in SYMBOLS],
                         value="AAPL", style={"width": "200px"}),
            dcc.Dropdown(id="strategy",
                         options=[{"label": "Golden Cross (SMA)", "value": "golden_cross"},
                                  {"label": "RSI Strategie", "value": "rsi"}],
                         value="golden_cross", style={"width": "200px"}),
        ], style={"display": "flex", "gap": "20px", "padding": "10px"}),
        dcc.Graph(id="chart"),
    ], style={"backgroundColor": "#1e1e1e", "minHeight": "100vh"})

    @app.callback(Output("chart", "figure"),
                  [Input("symbol", "value"), Input("strategy", "value")])
    def update_chart(symbol, strategy):
        return create_chart(symbol, strategy)

    print("Dashboard läuft auf http://127.0.0.1:8050")
    app.run(debug=True)
