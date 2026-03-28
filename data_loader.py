"""
data_loader.py — Load and clean all CSV data files
"""
import pandas as pd
import numpy as np
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def _path(fname):
    return os.path.join(DATA_DIR, fname)


@st_cache
def load_nifty50_watchlist():
    df = pd.read_csv(_path("MW-NIFTY-50-28-Mar-2026.csv"))
    df.columns = [c.strip().replace("\n", "").strip() for c in df.columns]
    # Remove first row (NIFTY 50 index row) & blank rows
    df = df[df["SYMBOL"].notna()].copy()
    df = df[df["SYMBOL"] != "NIFTY 50"].copy()
    # Clean numeric columns
    num_cols = ["OPEN", "HIGH", "LOW", "PREV. CLOSE", "LTP", "CHNG", "%CHNG",
                "52W H", "52W L", "30 D   %CHNG", "365 D   %CHNG"]
    for col in num_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(",", "").str.strip()
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["LTP"])
    df["SYMBOL"] = df["SYMBOL"].str.strip()
    return df.reset_index(drop=True)


@st_cache
def load_stock_prices():
    df = pd.read_csv(_path("01_stock_prices_mar27_2026.csv"))
    return df


@st_cache
def load_fii_dii():
    df = pd.read_csv(_path("02_fii_dii_flows.csv"))
    return df


@st_cache
def load_macro():
    df = pd.read_csv(_path("03_macro_indicators.csv"))
    return df


@st_cache
def load_sector_performance():
    df = pd.read_csv(_path("04_sector_performance.csv"))
    return df


@st_cache
def load_risk_metrics():
    df = pd.read_csv(_path("05_risk_metrics.csv"))
    return df


@st_cache
def load_price_history():
    df = pd.read_csv(_path("06_daily_price_history.csv"))
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    return df


@st_cache
def load_correlation():
    df = pd.read_csv(_path("07_correlation_matrix.csv"), index_col=0)
    return df


@st_cache
def load_top10():
    df = pd.read_csv(_path("top10nifty50_270326.csv"))
    df.columns = [c.strip() for c in df.columns]
    return df


@st_cache
def load_all_indices():
    df = pd.read_csv(_path("ind_close_all_27032026.csv"))
    df.columns = [c.strip() for c in df.columns]
    return df


@st_cache
def load_largemidcap_history():
    df = pd.read_csv(_path("NIFTY_LARGEMIDCAP_250-28-09-2025-to-28-03-2026.csv"))
    df.columns = [c.strip() for c in df.columns]
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%b-%Y", errors="coerce")
    df = df.dropna(subset=["Date"]).sort_values("Date").reset_index(drop=True)
    return df


@st_cache
def load_nifty_next50_history():
    df = pd.read_csv(_path("NIFTY_NEXT_50-28-09-2025-to-28-03-2026.csv"))
    df.columns = [c.strip() for c in df.columns]
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%b-%Y", errors="coerce")
    df = df.dropna(subset=["Date"]).sort_values("Date").reset_index(drop=True)
    return df


# ── Analytics helpers ──────────────────────────────────────────────────────

def compute_returns(price_series: pd.Series) -> pd.Series:
    return price_series.pct_change().dropna()


def compute_cagr(price_series: pd.Series, periods_per_year: int = 252) -> float:
    s = price_series.dropna()
    if len(s) < 2:
        return np.nan
    n_years = len(s) / periods_per_year
    return (s.iloc[-1] / s.iloc[0]) ** (1 / n_years) - 1


def compute_sharpe(returns: pd.Series, rf_annual: float = 0.0525,
                   periods_per_year: int = 252) -> float:
    rf_daily = (1 + rf_annual) ** (1 / periods_per_year) - 1
    excess = returns - rf_daily
    if excess.std() == 0:
        return np.nan
    return (excess.mean() / excess.std()) * np.sqrt(periods_per_year)


def compute_sortino(returns: pd.Series, rf_annual: float = 0.0525,
                    periods_per_year: int = 252) -> float:
    rf_daily = (1 + rf_annual) ** (1 / periods_per_year) - 1
    excess = returns - rf_daily
    downside = returns[returns < 0].std()
    if downside == 0:
        return np.nan
    return (excess.mean() / downside) * np.sqrt(periods_per_year)


def compute_max_drawdown(price_series: pd.Series) -> float:
    roll_max = price_series.cummax()
    drawdown = (price_series - roll_max) / roll_max
    return drawdown.min()


def compute_var(returns: pd.Series, confidence: float = 0.95) -> float:
    return np.percentile(returns.dropna(), (1 - confidence) * 100)


def compute_beta(stock_returns: pd.Series, market_returns: pd.Series) -> float:
    aligned = pd.concat([stock_returns, market_returns], axis=1).dropna()
    if len(aligned) < 10:
        return np.nan
    cov = np.cov(aligned.iloc[:, 0], aligned.iloc[:, 1])
    return cov[0, 1] / cov[1, 1] if cov[1, 1] != 0 else np.nan


def compute_drawdown_series(price_series: pd.Series) -> pd.Series:
    roll_max = price_series.cummax()
    return (price_series - roll_max) / roll_max * 100


def compute_moving_averages(price_series: pd.Series):
    return {
        "MA_50": price_series.rolling(50).mean(),
        "MA_200": price_series.rolling(200).mean(),
        "MA_20": price_series.rolling(20).mean(),
    }


def compute_rsi(price_series: pd.Series, window: int = 14) -> pd.Series:
    delta = price_series.diff()
    gain = delta.clip(lower=0).rolling(window).mean()
    loss = (-delta.clip(upper=0)).rolling(window).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def get_trend_signal(price_series: pd.Series) -> dict:
    if len(price_series) < 200:
        return {"signal": "INSUFFICIENT DATA", "color": "#888"}
    ma50 = price_series.rolling(50).mean().iloc[-1]
    ma200 = price_series.rolling(200).mean().iloc[-1]
    current = price_series.iloc[-1]
    rsi = compute_rsi(price_series).iloc[-1]
    if current > ma200 and current > ma50 and rsi > 50:
        return {"signal": "BULLISH", "color": "#00c853", "rsi": round(rsi, 1)}
    elif current < ma200 and current < ma50 and rsi < 50:
        return {"signal": "BEARISH", "color": "#d50000", "rsi": round(rsi, 1)}
    else:
        return {"signal": "NEUTRAL", "color": "#ff9800", "rsi": round(rsi, 1)}


# Patch: cache decorator alias (will be replaced in main app)
def st_cache(fn):
    return fn
