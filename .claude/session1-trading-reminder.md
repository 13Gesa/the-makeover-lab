# SESSION 1 — Trading & Finanz-Tool

## Status: BEREIT ZUM WEITERBAUEN

### Was fertig ist (gepusht auf GitHub):
- Branch: `claude/trading-tool-projekt-lixcs8`
- Repo: `13Gesa/the-makeover-lab`
- Ordner: `trading/`

### Dateien:
- `data/fetch_data.py` — Kursdaten via yfinance (AAPL, BTC, ETH, etc.)
- `analysis/indicators.py` — RSI, MACD, Bollinger Bands, SMA, EMA
- `analysis/backtest.py` — Backtest-Engine mit Sharpe, Drawdown, Win Rate
- `strategies/simple_strategy.py` — Golden Cross & RSI-Strategie
- `dashboard/app.py` — Interaktives Plotly Dash Dashboard

### Nächste Schritte (Vorschläge):
- [ ] Portfolio-Tracker
- [ ] Live-Preise (WebSocket)
- [ ] Telegram-Alerts bei Signalen
- [ ] Mehr Strategien (Breakout, VWAP)
- [ ] Daten lokal cachen

### Start:
```bash
pip install -r trading/requirements.txt
python trading/data/fetch_data.py
python trading/dashboard/app.py
```
