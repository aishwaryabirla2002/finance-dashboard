# 📊 India Market Intelligence Dashboard

A professional, CFO/Director-level financial analytics dashboard built with **Streamlit** and **Plotly**.

**Data as of: March 28, 2026 | India Market Close**

---

## 🚀 Quick Start

### Option 1 — Run Locally

```bash
# 1. Clone / unzip the project
cd india_dashboard

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate          # Linux / Mac
venv\Scripts\activate             # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the dashboard
streamlit run app.py
```

Open your browser at **http://localhost:8501**

---

### Option 2 — Deploy to Streamlit Cloud (GitHub)

1. Push this entire folder to a **GitHub repository**
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **"New app"**
4. Select your repo, branch, and set **Main file path** to `app.py`
5. Click **Deploy** — it goes live in ~2 minutes

**Important:** The `data/` folder must be committed to your GitHub repo.

---

## 📁 Project Structure

```
india_dashboard/
├── app.py                          ← Main Streamlit application
├── data_loader.py                  ← Data loading & analytics helpers
├── requirements.txt                ← Python dependencies
├── README.md                       ← This file
└── data/                           ← All CSV data files
    ├── MW-NIFTY-50-28-Mar-2026.csv          ← Live NIFTY 50 watchlist
    ├── 01_stock_prices_mar27_2026.csv        ← 30-stock fundamental data
    ├── 02_fii_dii_flows.csv                  ← 12-month FII/DII flows
    ├── 03_macro_indicators.csv               ← 20 macro indicators
    ├── 04_sector_performance.csv             ← Sector returns FY26
    ├── 05_risk_metrics.csv                   ← Risk metrics per stock
    ├── 06_daily_price_history.csv            ← 252-day price history
    ├── 07_correlation_matrix.csv             ← 10x10 correlation matrix
    ├── top10nifty50_270326.csv               ← NIFTY 50 top 10 weightages
    ├── ind_close_all_27032026.csv            ← All NSE indices snapshot
    ├── NIFTY_LARGEMIDCAP_250-...csv          ← 6-month LargeMidcap history
    └── NIFTY_NEXT_50-...csv                  ← 6-month Next 50 history
```

---

## 📊 Dashboard Pages

| Page | What You Get |
|------|-------------|
| 🏠 Executive Summary | Market snapshot, FII/DII chart, sector performance, top movers, key insights |
| 📈 Return Analysis | Total return, CAGR, YTD, rolling 63-day returns, normalized price comparison, benchmark comparison |
| ⚠️ Risk Analysis | Sharpe ratio, Sortino, Beta, Max Drawdown, VaR, volatility comparison, risk-return scatter |
| 🧩 Portfolio Structure | NIFTY sector weights, top 10 holdings, asset allocation, live watchlist table |
| 🔗 Correlation & Diversification | 10x10 correlation heatmap, rolling correlation, diversification insights |
| 📉 Drawdown & Stress | Drawdown curves, candlestick chart, stress scenario table |
| 🌍 Macro & Sentiment | All macro KPIs, FII/DII vs NIFTY overlay, news sentiment scoring |
| 🤖 Predictive Signals | Moving averages (20/50/200 DMA), RSI, rolling volatility, trend signals |
| 📰 News Intelligence | 8 news event cards, stock sensitivity matrix, composite risk dashboard |

---

## 🎯 Key Features

- **Dark professional UI** — designed for executive boardroom presentations
- **Real market data** — sourced from NSE, BSE, NSDL (March 2026)
- **Interactive charts** — all Plotly charts with hover/zoom capability
- **Multi-stock comparison** — select up to 8 stocks for parallel analysis
- **Computed analytics** — Sharpe, Sortino, Beta, VaR, CAGR all computed live
- **Sensitivity analysis** — scenario-based impact scoring for key news events
- **Zero external API calls** — fully offline after initial load

---

## 🔑 KPI Framework Implemented

```
Layer A: Return KPIs     → Total Return, CAGR, YTD, Rolling 63D, vs Benchmark
Layer B: Risk KPIs       → Sharpe, Sortino, Beta, Max Drawdown, VaR 95%/99%
Layer C: Structure KPIs  → Sector weights, top 10 holdings, concentration
Layer D: Diversification → Correlation matrix, rolling correlation, diversification ratio
Layer E: Drawdown        → Drawdown curve, worst period, stress scenarios
Layer F: Macro           → VIX, rates, inflation, crude, FII/DII, sentiment score
Layer G: Predictive      → MA(20/50/200), RSI(14), trend signal, rolling volatility
```

---

## ⚙️ Dependencies

```
streamlit >= 1.32.0
pandas    >= 2.0.0
numpy     >= 1.24.0
plotly    >= 5.18.0
scipy     >= 1.11.0
```

---

## ⚠️ Disclaimer

This dashboard is for **educational and research purposes only**. It does not constitute
investment advice. All data sourced from publicly available NSE, BSE, and NSDL sources
as of March 28, 2026.

---

*Built for CFO / Director-level decision support | India Market Intelligence 2026*
