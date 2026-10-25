# Trading & Finanz-Tool

Ein selbst gebautes Trading-Analyse-Tool — kein teures Kurs nötig.

## Projektstruktur

```
trading/
├── data/           # Kursdaten laden & speichern (yfinance, CSV)
├── strategies/     # Handelsstrategien (Moving Average, RSI, etc.)
├── analysis/       # Technische Analyse & Backtesting
├── dashboard/      # Web-Dashboard zum Anzeigen der Ergebnisse
└── utils/          # Hilfsfunktionen (Berechnungen, Formatierung)
```

## Was wir bauen können

- **Kursdaten abrufen** — kostenlos via Yahoo Finance (yfinance)
- **Technische Indikatoren** — RSI, MACD, Bollinger Bands, Moving Averages
- **Backtesting** — Strategien auf historischen Daten testen
- **Live-Dashboard** — interaktive Charts im Browser
- **Signale & Alerts** — Kauf-/Verkaufssignale automatisch erkennen
- **Portfolio-Tracker** — Positionen und Performance überwachen

## Schnellstart

```bash
pip install yfinance pandas matplotlib plotly
python data/fetch_data.py
```

## Roadmap

- [ ] Kursdaten-Fetcher (yfinance)
- [ ] Technische Indikatoren (RSI, MACD)
- [ ] Einfache Backtest-Engine
- [ ] Interaktives Dashboard (Plotly/Dash)
- [ ] Portfolio-Tracker
- [ ] Signalgenerator
