"""
India Market Intelligence Dashboard
CFO / Director-level Portfolio Analytics
March 28, 2026
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os, sys

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="India Market Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject global CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Base */
  [data-testid="stAppViewContainer"] { background: #0d1117; color: #e6edf3; }
  [data-testid="stSidebar"] { background: #161b22; border-right: 1px solid #30363d; }
  [data-testid="stHeader"] { background: transparent; }

  /* Typography */
  h1, h2, h3 { color: #e6edf3 !important; font-family: 'Segoe UI', sans-serif; }
  p, li, label, .stMarkdown { color: #8b949e; font-family: 'Segoe UI', sans-serif; }

  /* KPI Cards */
  .kpi-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 18px 20px;
    text-align: center;
    margin: 4px 0;
  }
  .kpi-label { font-size: 11px; color: #8b949e; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 6px; }
  .kpi-value { font-size: 26px; font-weight: 700; font-family: 'Segoe UI', sans-serif; }
  .kpi-sub { font-size: 12px; margin-top: 4px; }
  .kpi-up { color: #3fb950; }
  .kpi-down { color: #f85149; }
  .kpi-warn { color: #e3b341; }
  .kpi-neutral { color: #58a6ff; }

  /* News cards */
  .news-card {
    background: #161b22;
    border-left: 4px solid;
    border-radius: 8px;
    padding: 14px 16px;
    margin: 8px 0;
  }
  .news-tag { font-size: 10px; font-weight: 700; letter-spacing: 1px; padding: 2px 8px; border-radius: 4px; }
  .news-headline { font-size: 14px; font-weight: 600; color: #e6edf3; margin: 6px 0 4px; }
  .news-meta { font-size: 11px; color: #8b949e; }
  .news-body { font-size: 12px; color: #8b949e; line-height: 1.6; margin-top: 6px; }

  /* Insight boxes */
  .insight-box {
    background: #1c2128;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 16px 18px;
    margin: 8px 0;
  }
  .insight-title { font-size: 12px; font-weight: 700; color: #58a6ff; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }
  .insight-row { display: flex; align-items: flex-start; margin: 6px 0; font-size: 13px; color: #8b949e; }
  .dot-g { color: #3fb950; margin-right: 8px; }
  .dot-r { color: #f85149; margin-right: 8px; }
  .dot-a { color: #e3b341; margin-right: 8px; }
  .dot-b { color: #58a6ff; margin-right: 8px; }
  strong { color: #e6edf3; }

  /* Risk badges */
  .badge { display: inline-block; font-size: 10px; font-weight: 700; padding: 3px 9px; border-radius: 20px; letter-spacing: 0.5px; }
  .badge-extreme { background: #3d1f1f; color: #f85149; }
  .badge-high { background: #2d2008; color: #e3b341; }
  .badge-medium { background: #1a2438; color: #58a6ff; }
  .badge-low { background: #162217; color: #3fb950; }

  /* Section headers */
  .section-header {
    background: linear-gradient(90deg, #161b22, #0d1117);
    border-left: 4px solid #58a6ff;
    padding: 12px 16px;
    border-radius: 0 8px 8px 0;
    margin: 20px 0 14px;
  }
  .section-title { font-size: 16px; font-weight: 700; color: #e6edf3; margin: 0; }
  .section-sub { font-size: 12px; color: #8b949e; margin: 2px 0 0; }

  /* Divider */
  .divider { border-top: 1px solid #30363d; margin: 16px 0; }

  /* Streamlit overrides */
  .stMetric { background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 12px; }
  div[data-testid="metric-container"] { background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 12px; }
  .stSelectbox label, .stMultiSelect label { color: #8b949e !important; }
  .stDataFrame { border: 1px solid #30363d; border-radius: 8px; }
  [data-testid="stTabsContent"] { padding-top: 16px; }
  .stTabs [data-baseweb="tab"] { background: transparent; color: #8b949e; border-radius: 8px 8px 0 0; }
  .stTabs [aria-selected="true"] { background: #161b22; color: #e6edf3 !important; border-top: 2px solid #58a6ff; }

  /* Plotly chart bg */
  .js-plotly-plot .plotly { background: transparent; }
</style>
""", unsafe_allow_html=True)

# ── Data loading ─────────────────────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

@st.cache_data
def load_all_data():
    def path(f): return os.path.join(DATA_DIR, f)

    # NIFTY 50 watchlist
    nw = pd.read_csv(path("MW-NIFTY-50-28-Mar-2026.csv"))
    nw.columns = [c.strip().replace("\n","").strip() for c in nw.columns]
    nw = nw[nw["SYMBOL"].notna()].copy()
    nw = nw[~nw["SYMBOL"].str.contains("NIFTY 50", na=False)].copy()
    for col in ["OPEN","HIGH","LOW","PREV. CLOSE","LTP","CHNG","%CHNG","52W H","52W L","30 D   %CHNG","365 D   %CHNG"]:
        if col in nw.columns:
            nw[col] = pd.to_numeric(nw[col].astype(str).str.replace(",","").str.strip(), errors="coerce")
    nw = nw.dropna(subset=["LTP"]).reset_index(drop=True)
    nw["SYMBOL"] = nw["SYMBOL"].str.strip()

    stocks  = pd.read_csv(path("01_stock_prices_mar27_2026.csv"))
    fii     = pd.read_csv(path("02_fii_dii_flows.csv"))
    macro   = pd.read_csv(path("03_macro_indicators.csv"))
    sector  = pd.read_csv(path("04_sector_performance.csv"))
    risk    = pd.read_csv(path("05_risk_metrics.csv"))
    hist    = pd.read_csv(path("06_daily_price_history.csv"))
    hist["Date"] = pd.to_datetime(hist["Date"])
    hist = hist.sort_values("Date").reset_index(drop=True)
    corr    = pd.read_csv(path("07_correlation_matrix.csv"), index_col=0)
    top10   = pd.read_csv(path("top10nifty50_270326.csv"))
    top10.columns = [c.strip() for c in top10.columns]
    indices = pd.read_csv(path("ind_close_all_27032026.csv"))
    indices.columns = [c.strip() for c in indices.columns]

    lm = pd.read_csv(path("NIFTY_LARGEMIDCAP_250-28-09-2025-to-28-03-2026.csv"))
    lm.columns = [c.strip() for c in lm.columns]
    lm["Date"] = pd.to_datetime(lm["Date"], format="%d-%b-%Y", errors="coerce")
    lm = lm.dropna(subset=["Date"]).sort_values("Date").reset_index(drop=True)

    nx = pd.read_csv(path("NIFTY_NEXT_50-28-09-2025-to-28-03-2026.csv"))
    nx.columns = [c.strip() for c in nx.columns]
    nx["Date"] = pd.to_datetime(nx["Date"], format="%d-%b-%Y", errors="coerce")
    nx = nx.dropna(subset=["Date"]).sort_values("Date").reset_index(drop=True)

    return dict(nifty_watch=nw, stocks=stocks, fii=fii, macro=macro,
                sector=sector, risk=risk, hist=hist, corr=corr,
                top10=top10, indices=indices, largemidcap=lm, nifty_next50=nx)

# ── Analytics helpers ────────────────────────────────────────────────────────
def cagr(s, n=252):
    s = s.dropna()
    return (s.iloc[-1]/s.iloc[0])**(n/len(s)) - 1 if len(s)>1 else np.nan

def sharpe(ret, rf=0.0525, n=252):
    rf_d = (1+rf)**(1/n)-1
    ex = ret - rf_d
    return (ex.mean()/ex.std())*np.sqrt(n) if ex.std()!=0 else np.nan

def sortino(ret, rf=0.0525, n=252):
    rf_d = (1+rf)**(1/n)-1
    ex = ret - rf_d
    dn = ret[ret<0].std()
    return (ex.mean()/dn)*np.sqrt(n) if dn!=0 else np.nan

def max_dd(s):
    return ((s - s.cummax())/s.cummax()).min()

def var95(ret):
    return np.percentile(ret.dropna(), 5)

def beta(stock_ret, mkt_ret):
    df = pd.concat([stock_ret, mkt_ret], axis=1).dropna()
    if len(df)<10: return np.nan
    c = np.cov(df.iloc[:,0], df.iloc[:,1])
    return c[0,1]/c[1,1] if c[1,1]!=0 else np.nan

def rsi(s, w=14):
    d = s.diff()
    g = d.clip(lower=0).rolling(w).mean()
    l = (-d.clip(upper=0)).rolling(w).mean()
    r = g/l.replace(0,np.nan)
    return 100-(100/(1+r))

def drawdown_series(s):
    return (s-s.cummax())/s.cummax()*100

def rolling_corr(s1, s2, w=63):
    r1 = s1.pct_change().dropna()
    r2 = s2.pct_change().dropna()
    return r1.rolling(w).corr(r2)

# ── Plotly theme helpers ─────────────────────────────────────────────────────
LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#8b949e", family="Segoe UI"),
    xaxis=dict(gridcolor="#21262d", zeroline=False, tickfont=dict(color="#8b949e")),
    yaxis=dict(gridcolor="#21262d", zeroline=False, tickfont=dict(color="#8b949e")),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#8b949e")),
    margin=dict(l=40, r=20, t=40, b=40),
)
PAL = ["#58a6ff","#3fb950","#e3b341","#f85149","#bc8cff","#79c0ff","#ffa657","#d2a8ff"]

def kpi(label, value, sub="", color="kpi-neutral"):
    return f"""<div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value {color}">{value}</div>
        <div class="kpi-sub {color}">{sub}</div>
    </div>"""

def section(title, sub=""):
    return f"""<div class="section-header">
        <p class="section-title">{title}</p>
        <p class="section-sub">{sub}</p>
    </div>"""

# ── Load data ────────────────────────────────────────────────────────────────
D = load_all_data()
nw       = D["nifty_watch"]
stocks   = D["stocks"]
fii      = D["fii"]
macro    = D["macro"]
sector   = D["sector"]
risk_df  = D["risk"]
hist     = D["hist"]
corr     = D["corr"]
top10    = D["top10"]
indices  = D["indices"]
lm_hist  = D["largemidcap"]
nx_hist  = D["nifty_next50"]

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""<div style='padding:12px 0 8px;'>
        <div style='font-size:20px;font-weight:700;color:#e6edf3;'>📊 Market Intel</div>
        <div style='font-size:11px;color:#8b949e;margin-top:2px;'>India Portfolio Analytics</div>
        <div style='font-size:10px;color:#3fb950;margin-top:2px;'>● Live Data · March 28, 2026</div>
    </div>""", unsafe_allow_html=True)

    st.divider()

    page = st.radio("Navigation", [
        "🏠 Executive Summary",
        "📈 Return Analysis",
        "⚠️ Risk Analysis",
        "🧩 Portfolio Structure",
        "🔗 Correlation & Diversification",
        "📉 Drawdown & Stress",
        "🌍 Macro & Sentiment",
        "🤖 Predictive Signals",
        "📰 News Intelligence",
    ], label_visibility="collapsed")

    st.divider()

    # Stock selector for analysis
    stock_cols = [c for c in hist.columns if c != "Date"]
    selected_stocks = st.multiselect(
        "Stocks for analysis",
        options=stock_cols,
        default=["NIFTY50","TCS","HDFC Bank","ICICI Bank","BEL"],
        max_selections=8,
    )
    if not selected_stocks:
        selected_stocks = ["NIFTY50"]

    st.divider()
    st.markdown("<div style='font-size:10px;color:#484f58;padding-top:8px;'>Not investment advice.<br>Data: NSE / BSE / NSDL<br>© India Market Intel 2026</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — EXECUTIVE SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
if "Executive Summary" in page:
    st.markdown('<h1 style="font-size:28px;font-weight:700;color:#e6edf3;margin-bottom:2px;">India Market Intelligence Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#8b949e;font-size:14px;margin-bottom:20px;">CFO / Director-level Portfolio Analytics · March 28, 2026 · Data as of March 27, 2026 Close</p>', unsafe_allow_html=True)

    # Top KPI strip
    c1,c2,c3,c4,c5,c6,c7 = st.columns(7)
    c1.markdown(kpi("NIFTY 50","22,819","-486 pts (-2.09%)","kpi-down"), unsafe_allow_html=True)
    c2.markdown(kpi("SENSEX","73,583","-1,690 pts (-2.25%)","kpi-down"), unsafe_allow_html=True)
    c3.markdown(kpi("BRENT CRUDE","$109.9/bbl","+1.72% ↑ DANGER","kpi-down"), unsafe_allow_html=True)
    c4.markdown(kpi("USD/INR","₹94.82","All-time low","kpi-down"), unsafe_allow_html=True)
    c5.markdown(kpi("INDIA VIX","24.64","Elevated (norm: 12-18)","kpi-warn"), unsafe_allow_html=True)
    c6.markdown(kpi("NIFTY P/E","17.5x","Below 5Y avg 19.6x","kpi-neutral"), unsafe_allow_html=True)
    c7.markdown(kpi("GOLD","$4,457/oz","+1.10% Safe haven","kpi-up"), unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Market context + index table side by side
    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.markdown(section("Index Performance Snapshot", "March 27, 2026 — All major indices"), unsafe_allow_html=True)
        key_indices = ["Nifty 50","Nifty Bank","Nifty IT","Nifty Auto","Nifty Metal",
                       "Nifty Pharma","Nifty FMCG","Nifty PSU Bank","NIFTY Midcap 100","NIFTY Smallcap 100"]
        idx_sub = indices[indices["Index Name"].isin(key_indices)].copy()
        idx_sub = idx_sub[["Index Name","Closing Index Value","Change(%)","P/E","P/B","Div Yield"]].copy()
        idx_sub["Change(%)"] = pd.to_numeric(idx_sub["Change(%)"], errors="coerce")

        def color_pct(val):
            color = "#3fb950" if val > 0 else "#f85149"
            return f'<span style="color:{color};font-weight:600;">{val:+.2f}%</span>'

        idx_sub["Change"] = idx_sub["Change(%)"].apply(color_pct)
        idx_sub["Index"] = idx_sub["Index Name"]
        idx_sub["Close"] = idx_sub["Closing Index Value"].apply(lambda x: f"{float(str(x).replace(',','')):,.2f}" if pd.notna(x) else "")
        disp = idx_sub[["Index","Close","Change","P/E","P/B","Div Yield"]].rename(columns={"Div Yield":"Div Yld"})
        st.markdown(disp.to_html(index=False, escape=False,
            classes="",
            border=0,
            justify="left",
        ).replace('<table','<table style="width:100%;border-collapse:collapse;font-size:12px;color:#8b949e;"'
        ).replace('<th>','<th style="padding:6px 10px;background:#161b22;color:#e6edf3;font-size:11px;text-align:left;border-bottom:1px solid #30363d;">'
        ).replace('<td>','<td style="padding:5px 10px;border-bottom:1px solid #21262d;">'),
        unsafe_allow_html=True)

    with col_right:
        st.markdown(section("FII vs DII Flows", "12-month capital flow dynamics"), unsafe_allow_html=True)
        fig_fii = go.Figure()
        colors_fii = ["#f85149" if v < 0 else "#3fb950" for v in fii["FII_Net_Cr"]]
        fig_fii.add_trace(go.Bar(x=fii["Month"], y=fii["FII_Net_Cr"], name="FII Net",
                                  marker_color=colors_fii, opacity=0.85))
        fig_fii.add_trace(go.Bar(x=fii["Month"], y=fii["DII_Net_Cr"], name="DII Net",
                                  marker_color="#58a6ff", opacity=0.75))
        fig_fii.update_layout(**LAYOUT, height=280, barmode="group",
                               title=dict(text="FII / DII Monthly Flows (₹ Crore)", font=dict(color="#e6edf3",size=13)))
        fig_fii.add_hline(y=0, line_color="#484f58", line_width=1)
        st.plotly_chart(fig_fii, use_container_width=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Sector performance + top movers
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown(section("Sector Returns — FY26 Budget-to-Date"), unsafe_allow_html=True)
        sec_plot = sector.dropna(subset=["FY26_BtD_Return_Pct"]).copy()
        sec_plot = sec_plot.sort_values("FY26_BtD_Return_Pct")
        colors_sec = ["#3fb950" if v > 0 else "#f85149" for v in sec_plot["FY26_BtD_Return_Pct"]]
        fig_sec = go.Figure(go.Bar(
            x=sec_plot["FY26_BtD_Return_Pct"],
            y=sec_plot["Sector"],
            orientation="h",
            marker_color=colors_sec,
            text=[f"{v:+.1f}%" for v in sec_plot["FY26_BtD_Return_Pct"]],
            textposition="outside",
            textfont=dict(size=10, color="#8b949e"),
        ))
        fig_sec.update_layout(**LAYOUT, height=380, xaxis_title="Return %",
                               title=dict(text="Sector Performance vs NIFTY Benchmark (+7.5%)", font=dict(color="#e6edf3",size=12)))
        fig_sec.add_vline(x=7.5, line_dash="dash", line_color="#e3b341", annotation_text="NIFTY 7.5%",
                          annotation_font_color="#e3b341", annotation_font_size=10)
        st.plotly_chart(fig_sec, use_container_width=True)

    with col_b:
        st.markdown(section("NIFTY 50 Top Movers — March 27"), unsafe_allow_html=True)
        nw_plot = nw.dropna(subset=["%CHNG"]).copy()
        nw_plot = nw_plot.sort_values("%CHNG")
        bottom5 = nw_plot.head(5)
        top5 = nw_plot.tail(5)
        movers = pd.concat([bottom5, top5])
        fig_mv = go.Figure(go.Bar(
            x=movers["%CHNG"],
            y=movers["SYMBOL"],
            orientation="h",
            marker_color=["#3fb950" if v > 0 else "#f85149" for v in movers["%CHNG"]],
            text=[f"{v:+.1f}%" for v in movers["%CHNG"]],
            textposition="outside",
            textfont=dict(size=10),
        ))
        fig_mv.update_layout(**LAYOUT, height=380,
                              title=dict(text="Top 5 Gainers & Losers (March 27, 2026)", font=dict(color="#e6edf3",size=12)))
        fig_mv.add_vline(x=0, line_color="#484f58", line_width=1)
        st.plotly_chart(fig_mv, use_container_width=True)

    # Key Insights box
    st.markdown(section("🔥 Key Analyst Insights — March 28, 2026"), unsafe_allow_html=True)
    ins_cols = st.columns(3)
    with ins_cols[0]:
        st.markdown("""<div class='insight-box'>
            <div class='insight-title'>📉 Risk Signals</div>
            <div class='insight-row'><span class='dot-r'>●</span><span>FII outflows <strong>₹88,180 Cr in March</strong> — 2nd highest ever. YTD crosses ₹1 lakh Cr</span></div>
            <div class='insight-row'><span class='dot-r'>●</span><span>Rupee at <strong>₹94.82 all-time low</strong> — 4% depreciation since Iran conflict began</span></div>
            <div class='insight-row'><span class='dot-r'>●</span><span><strong>Brent $109.9/bbl</strong> after brief $98 relief — Iran rejected ceasefire</span></div>
            <div class='insight-row'><span class='dot-r'>●</span><span>HDFC Bank down <strong>26% from 52W high</strong> — governance probe ongoing</span></div>
        </div>""", unsafe_allow_html=True)
    with ins_cols[1]:
        st.markdown("""<div class='insight-box'>
            <div class='insight-title'>✅ Opportunity Signals</div>
            <div class='insight-row'><span class='dot-g'>●</span><span>NIFTY PE at <strong>17.5x below 5-year avg 19.6x</strong> — oversold zone</span></div>
            <div class='insight-row'><span class='dot-g'>●</span><span><strong>DII buying ₹42,840 Cr</strong> in March prevents capitulation</span></div>
            <div class='insight-row'><span class='dot-g'>●</span><span>IT sector <strong>rupee tailwind</strong> — only sector to gain on March 27</span></div>
            <div class='insight-row'><span class='dot-g'>●</span><span><strong>Q3 FY26 PAT +9% YoY</strong> — highest earnings growth in 7 quarters</span></div>
        </div>""", unsafe_allow_html=True)
    with ins_cols[2]:
        st.markdown("""<div class='insight-box'>
            <div class='insight-title'>🎯 Decision Triggers</div>
            <div class='insight-row'><span class='dot-a'>●</span><span><strong>April 6</strong>: Trump Iran deadline — binary event. Ceasefire = Nifty +10-15%</span></div>
            <div class='insight-row'><span class='dot-a'>●</span><span><strong>April 8</strong>: RBI MPC meeting — rate hold expected; tone on inflation critical</span></div>
            <div class='insight-row'><span class='dot-a'>●</span><span><strong>April 9-18</strong>: Q4 FY26 earnings begin (TCS, Infosys, HDFC Bank)</span></div>
            <div class='insight-row'><span class='dot-b'>●</span><span>Analyst consensus: NIFTY <strong>27,200–28,500 by Dec 2026</strong> (J.P. Morgan: 30,000)</span></div>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — RETURN ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif "Return Analysis" in page:
    st.markdown('<h2 style="color:#e6edf3;">📈 Return Analysis</h2>', unsafe_allow_html=True)
    st.caption("Total Return · CAGR · Rolling Returns · Benchmark Comparison · Normalized Performance")

    if selected_stocks:
        sub_hist = hist[["Date"] + [s for s in selected_stocks if s in hist.columns]].copy().dropna()

        # Compute metrics per stock
        metrics = []
        for stock in selected_stocks:
            if stock not in sub_hist.columns: continue
            s = sub_hist[stock].dropna()
            ret = s.pct_change().dropna()
            total_ret = (s.iloc[-1]/s.iloc[0] - 1)*100
            cagr_val = cagr(s)*100
            ytd_ret = (s.iloc[-1]/s.iloc[min(60,len(s)-1)] - 1)*100 if len(s) > 60 else total_ret
            sharpe_val = sharpe(ret)
            vol = ret.std()*np.sqrt(252)*100
            mdd = max_dd(s)*100
            metrics.append({
                "Stock": stock,
                "Total Return %": round(total_ret, 1),
                "CAGR %": round(cagr_val, 1),
                "YTD (est) %": round(ytd_ret, 1),
                "Sharpe Ratio": round(sharpe_val, 2) if pd.notna(sharpe_val) else "N/A",
                "Volatility %": round(vol, 1),
                "Max Drawdown %": round(mdd, 1),
            })
        mdf = pd.DataFrame(metrics)

        # KPI row
        cols = st.columns(len(metrics))
        for i, row in mdf.iterrows():
            color = "kpi-up" if row["Total Return %"] > 0 else "kpi-down"
            cols[i].markdown(kpi(row["Stock"], f"{row['Total Return %']:+.1f}%",
                             f"CAGR: {row['CAGR %']:+.1f}%", color), unsafe_allow_html=True)

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        # Metrics table
        st.markdown(section("Performance Metrics Comparison"), unsafe_allow_html=True)
        styled_mdf = mdf.set_index("Stock")

        def color_val(v):
            try:
                v = float(v)
                c = "#3fb950" if v > 0 else "#f85149"
                return f'<span style="color:{c};font-weight:600;">{v:+.1f}</span>'
            except: return f'<span style="color:#8b949e;">{v}</span>'

        st.dataframe(styled_mdf, use_container_width=True,
                     column_config={
                         "Total Return %": st.column_config.NumberColumn(format="%.1f%%"),
                         "CAGR %": st.column_config.NumberColumn(format="%.1f%%"),
                         "Sharpe Ratio": st.column_config.NumberColumn(format="%.2f"),
                         "Volatility %": st.column_config.NumberColumn(format="%.1f%%"),
                         "Max Drawdown %": st.column_config.NumberColumn(format="%.1f%%"),
                     })

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(section("Normalized Price Performance (Base = 100)"), unsafe_allow_html=True)
            fig_norm = go.Figure()
            for i, stock in enumerate(selected_stocks):
                if stock not in sub_hist.columns: continue
                s = sub_hist[stock].dropna()
                norm = s / s.iloc[0] * 100
                fig_norm.add_trace(go.Scatter(
                    x=sub_hist["Date"][:len(norm)], y=norm,
                    name=stock, line=dict(color=PAL[i % len(PAL)], width=2),
                ))
            fig_norm.add_hline(y=100, line_dash="dash", line_color="#484f58")
            fig_norm.update_layout(**LAYOUT, height=380,
                                   title=dict(text="Normalized Price (Base=100)", font=dict(color="#e6edf3",size=13)))
            st.plotly_chart(fig_norm, use_container_width=True)

        with col2:
            st.markdown(section("Rolling 63-Day (Quarterly) Returns"), unsafe_allow_html=True)
            fig_roll = go.Figure()
            for i, stock in enumerate(selected_stocks):
                if stock not in sub_hist.columns: continue
                s = sub_hist[stock]
                roll_ret = s.pct_change(63).dropna() * 100
                fig_roll.add_trace(go.Scatter(
                    x=sub_hist["Date"][63:], y=roll_ret,
                    name=stock, line=dict(color=PAL[i % len(PAL)], width=2),
                ))
            fig_roll.add_hline(y=0, line_color="#484f58", line_width=1)
            fig_roll.update_layout(**LAYOUT, height=380, yaxis_ticksuffix="%",
                                   title=dict(text="63-Day Rolling Return (%)", font=dict(color="#e6edf3",size=13)))
            st.plotly_chart(fig_roll, use_container_width=True)

        # Benchmark comparison
        st.markdown(section("Benchmark Comparison vs NIFTY 50"), unsafe_allow_html=True)
        if "NIFTY50" in sub_hist.columns:
            bench_ret = sub_hist["NIFTY50"].pct_change().dropna()
            alpha_data = []
            for stock in selected_stocks:
                if stock == "NIFTY50" or stock not in sub_hist.columns: continue
                s = sub_hist[stock]
                sr = s.pct_change().dropna()
                alpha = (sr.mean() - bench_ret.mean()) * 252 * 100
                b_val = beta(sr, bench_ret)
                alpha_data.append({"Stock": stock, "Alpha (ann.)": round(alpha,2),
                                    "Beta": round(b_val,2) if pd.notna(b_val) else "N/A",
                                    "Outperformance vs NIFTY (Total %)": round((s.iloc[-1]/s.iloc[0] - sub_hist["NIFTY50"].iloc[-1]/sub_hist["NIFTY50"].iloc[0])*100, 1)})
            if alpha_data:
                adf = pd.DataFrame(alpha_data)
                st.dataframe(adf.set_index("Stock"), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — RISK ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif "Risk Analysis" in page:
    st.markdown('<h2 style="color:#e6edf3;">⚠️ Risk Analysis</h2>', unsafe_allow_html=True)
    st.caption("Volatility · Sharpe · Sortino · Beta · Max Drawdown · VaR · Risk-Adjusted Returns")

    # Top risk KPIs from the CSV data
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.markdown(kpi("INDIA VIX","24.64","Elevated — caution zone","kpi-warn"), unsafe_allow_html=True)
    c2.markdown(kpi("NIFTY MAX DD","-13.5%","From Dec 26,326 peak","kpi-down"), unsafe_allow_html=True)
    c3.markdown(kpi("FII MONTHLY","-₹88,180 Cr","Record sell streak","kpi-down"), unsafe_allow_html=True)
    c4.markdown(kpi("PUT-CALL RATIO","0.78","Bearish options tilt","kpi-down"), unsafe_allow_html=True)
    c5.markdown(kpi("RBI REPO","5.25%","On hold — inflation risk","kpi-warn"), unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(section("Risk Metrics by Stock"), unsafe_allow_html=True)
        risk_show = risk_df.copy()
        st.dataframe(risk_show.set_index("Stock"), use_container_width=True,
                     column_config={
                         "Daily_Vol_Pct": st.column_config.NumberColumn("Daily Vol %", format="%.2f%%"),
                         "Annual_Vol_Pct": st.column_config.NumberColumn("Annual Vol %", format="%.1f%%"),
                         "Beta": st.column_config.NumberColumn(format="%.2f"),
                         "Max_DD_Pct": st.column_config.NumberColumn("Max DD %", format="%.1f%%"),
                         "Sharpe": st.column_config.NumberColumn(format="%.2f"),
                         "Sortino": st.column_config.NumberColumn(format="%.2f"),
                         "VaR_95_Pct": st.column_config.NumberColumn("VaR 95%", format="%.2f%%"),
                         "Alpha_Pct": st.column_config.NumberColumn("Alpha %", format="%.1f%%"),
                         "Corr_NIFTY": st.column_config.NumberColumn("Corr NIFTY", format="%.2f"),
                     })

    with col2:
        st.markdown(section("Sharpe vs Volatility — Risk-Return Scatter"), unsafe_allow_html=True)
        risk_scatter = risk_df.dropna(subset=["Sharpe","Annual_Vol_Pct","Max_DD_Pct"]).copy()
        fig_scatter = px.scatter(
            risk_scatter,
            x="Annual_Vol_Pct", y="Sharpe",
            size=risk_scatter["Max_DD_Pct"].abs(),
            color="Sharpe",
            color_continuous_scale=["#f85149","#e3b341","#3fb950"],
            hover_name="Stock",
            hover_data={"Annual_Vol_Pct":":.1f","Sharpe":":.2f","Max_DD_Pct":":.1f"},
            labels={"Annual_Vol_Pct":"Annualized Volatility (%)","Sharpe":"Sharpe Ratio"},
            text="Stock",
        )
        fig_scatter.update_traces(textposition="top center", textfont_size=10, textfont_color="#8b949e")
        fig_scatter.add_hline(y=1.0, line_dash="dash", line_color="#e3b341",
                              annotation_text="Sharpe = 1 threshold", annotation_font_color="#e3b341")
        fig_scatter.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  font=dict(color="#8b949e"), height=380,
                                  coloraxis_showscale=False, showlegend=False,
                                  xaxis=dict(gridcolor="#21262d",ticksuffix="%"),
                                  yaxis=dict(gridcolor="#21262d"),
                                  margin=dict(l=40,r=20,t=40,b=40))
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Computed risk for selected stocks
    if selected_stocks:
        st.markdown(section("Computed VaR & Drawdown from Price History"), unsafe_allow_html=True)
        var_data = []
        for stock in selected_stocks:
            if stock not in hist.columns: continue
            s = hist[stock].dropna()
            ret = s.pct_change().dropna()
            if len(ret) < 20: continue
            var_data.append({
                "Stock": stock,
                "VaR 95% (Daily)": f"{var95(ret)*100:.2f}%",
                "VaR 99% (Daily)": f"{np.percentile(ret,1)*100:.2f}%",
                "Sharpe (computed)": f"{sharpe(ret):.2f}",
                "Sortino (computed)": f"{sortino(ret):.2f}",
                "Volatility (ann.)": f"{ret.std()*np.sqrt(252)*100:.1f}%",
                "Max Drawdown": f"{max_dd(s)*100:.1f}%",
                "Beta vs NIFTY50": f"{beta(ret, hist['NIFTY50'].pct_change().dropna()):.2f}" if "NIFTY50" in hist.columns else "N/A",
            })
        if var_data:
            st.dataframe(pd.DataFrame(var_data).set_index("Stock"), use_container_width=True)

    # Volatility bar chart
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown(section("Annualized Volatility Comparison"), unsafe_allow_html=True)
    risk_sorted = risk_df.sort_values("Annual_Vol_Pct", ascending=True)
    fig_vol = go.Figure(go.Bar(
        x=risk_sorted["Annual_Vol_Pct"],
        y=risk_sorted["Stock"],
        orientation="h",
        marker_color=["#3fb950" if v < 16 else "#e3b341" if v < 22 else "#f85149" for v in risk_sorted["Annual_Vol_Pct"]],
        text=[f"{v:.1f}%" for v in risk_sorted["Annual_Vol_Pct"]],
        textposition="outside", textfont=dict(size=10, color="#8b949e"),
    ))
    fig_vol.add_vline(x=12.4, line_dash="dash", line_color="#58a6ff",
                     annotation_text="NIFTY 50 Vol 12.4%", annotation_font_color="#58a6ff")
    fig_vol.update_layout(**LAYOUT, height=380, xaxis_ticksuffix="%",
                          title=dict(text="Annualized Volatility — Higher = More Risk", font=dict(color="#e6edf3",size=13)))
    st.plotly_chart(fig_vol, use_container_width=True)

    # Key risk insight
    st.markdown("""<div class='insight-box' style='border-left:4px solid #f85149;'>
        <div class='insight-title' style='color:#f85149;'>⚠️ Risk Intelligence Summary</div>
        <div class='insight-row'><span class='dot-r'>●</span><span><strong>Tata Motors</strong> shows worst risk profile — Sharpe 0.72, Max DD -34.8%, Beta 1.48. Avoid in current environment.</span></div>
        <div class='insight-row'><span class='dot-r'>●</span><span><strong>HDFC Bank</strong> governance risk adds idiosyncratic risk on top of systemic pressure. 6.4% NIFTY weight = systemic concern.</span></div>
        <div class='insight-row'><span class='dot-g'>●</span><span><strong>TCS & HUL</strong> have best Sharpe ratios (1.42 & 1.28). Low beta + stable earnings = defensive anchors.</span></div>
        <div class='insight-row'><span class='dot-g'>●</span><span><strong>Gold ETF</strong> — Sharpe 0.92 + correlation 0.05 with NIFTY — best portfolio risk reducer right now.</span></div>
        <div class='insight-row'><span class='dot-a'>●</span><span><strong>BEL & HAL</strong> show higher volatility but strong alpha (+18.4% / +14.8%) — accept risk only with long horizon.</span></div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — PORTFOLIO STRUCTURE
# ══════════════════════════════════════════════════════════════════════════════
elif "Portfolio Structure" in page:
    st.markdown('<h2 style="color:#e6edf3;">🧩 Portfolio Structure & Allocation</h2>', unsafe_allow_html=True)
    st.caption("Asset Allocation · Sector Exposure · Top Holdings · Concentration Risk")

    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(kpi("FINANCIALS WEIGHT","33.5%","Dominant — concentration risk","kpi-warn"), unsafe_allow_html=True)
    c2.markdown(kpi("IT WEIGHT","13.8%","After -11.5% decline","kpi-warn"), unsafe_allow_html=True)
    c3.markdown(kpi("OIL & GAS WEIGHT","12.1%","High crude sensitivity","kpi-down"), unsafe_allow_html=True)
    c4.markdown(kpi("TOP 5 CONC.","47.5%","NIFTY top 5 weightage","kpi-warn"), unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(section("NIFTY 50 Sector Weights"), unsafe_allow_html=True)
        sector_weights = {
            "Financial Svcs": 33.5, "IT": 13.8, "Oil & Gas": 12.1,
            "Automobile": 8.4, "Consumer Goods": 8.0, "Metals": 6.2,
            "Pharma": 5.5, "Telecom": 5.0, "Others": 7.5,
        }
        fig_pie = go.Figure(go.Pie(
            labels=list(sector_weights.keys()),
            values=list(sector_weights.values()),
            hole=0.55,
            marker=dict(colors=PAL, line=dict(color="#0d1117", width=2)),
            textinfo="label+percent",
            textfont=dict(size=10, color="#e6edf3"),
        ))
        fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              showlegend=False, height=320, margin=dict(l=10,r=10,t=10,b=10),
                              annotations=[dict(text="NIFTY 50<br>Weights", x=0.5, y=0.5,
                                               font=dict(size=12,color="#e6edf3"), showarrow=False)])
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.markdown(section("Top 10 NIFTY 50 Holdings"), unsafe_allow_html=True)
        top10_clean = top10.copy()
        top10_clean.columns = [c.strip() for c in top10_clean.columns]
        fig_top10 = go.Figure(go.Bar(
            x=top10_clean["WEIGHTAGE(%)"],
            y=top10_clean["SYMBOL"],
            orientation="h",
            marker_color=PAL[:len(top10_clean)],
            text=[f"{v:.2f}%" for v in top10_clean["WEIGHTAGE(%)"]],
            textposition="outside", textfont=dict(size=10, color="#8b949e"),
        ))
        fig_top10.update_layout(**LAYOUT, height=320,
                                title=dict(text="Index Weightage (%)", font=dict(color="#e6edf3",size=12)))
        st.plotly_chart(fig_top10, use_container_width=True)

    with col3:
        st.markdown(section("Asset Class Mix (Suggested Portfolio)"), unsafe_allow_html=True)
        portfolio_alloc = {
            "Large-cap Equity": 40, "Mid-cap Equity": 15,
            "Defence PSU": 12, "Gold ETF": 15,
            "Pharma/IT Export": 10, "Debt/Liquid": 8,
        }
        fig_alloc = go.Figure(go.Pie(
            labels=list(portfolio_alloc.keys()),
            values=list(portfolio_alloc.values()),
            hole=0.5,
            marker=dict(colors=PAL, line=dict(color="#0d1117", width=2)),
            textinfo="label+percent",
            textfont=dict(size=9, color="#e6edf3"),
        ))
        fig_alloc.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                showlegend=False, height=320, margin=dict(l=10,r=10,t=10,b=10),
                                annotations=[dict(text="Balanced<br>Portfolio", x=0.5, y=0.5,
                                                 font=dict(size=11,color="#e6edf3"), showarrow=False)])
        st.plotly_chart(fig_alloc, use_container_width=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Full stock list
    st.markdown(section("NIFTY 50 Stocks — Live Watchlist March 28, 2026"), unsafe_allow_html=True)
    nw_disp = nw[["SYMBOL","LTP","%CHNG","52W H","52W L","30 D   %CHNG","365 D   %CHNG"]].copy()
    nw_disp.columns = ["Symbol","LTP","Day %","52W High","52W Low","30D %","1Y %"]
    st.dataframe(nw_disp, use_container_width=True,
                 column_config={
                     "Day %": st.column_config.NumberColumn(format="%.2f%%"),
                     "30D %": st.column_config.NumberColumn(format="%.2f%%"),
                     "1Y %": st.column_config.NumberColumn(format="%.2f%%"),
                 }, height=400)

    # Concentration risk insight
    st.markdown("""<div class='insight-box' style='border-left:4px solid #e3b341;'>
        <div class='insight-title' style='color:#e3b341;'>🧩 Portfolio Structure Intelligence</div>
        <div class='insight-row'><span class='dot-r'>●</span><span><strong>Financial services at 33.5%</strong> — any RBI policy surprise or FII exit hits the index disproportionately</span></div>
        <div class='insight-row'><span class='dot-a'>●</span><span><strong>Top 5 stocks = 47.5% of NIFTY</strong> — high concentration risk. Reliance alone is 10.17%</span></div>
        <div class='insight-row'><span class='dot-g'>●</span><span><strong>IT at 13.8%</strong> after -11.5% decline — compressed valuations make this a contrarian opportunity sector</span></div>
        <div class='insight-row'><span class='dot-g'>●</span><span>Suggested balanced portfolio: 15% Gold ETF reduces drawdown by ~8% without sacrificing significant return</span></div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — CORRELATION & DIVERSIFICATION
# ══════════════════════════════════════════════════════════════════════════════
elif "Correlation" in page:
    st.markdown('<h2 style="color:#e6edf3;">🔗 Correlation & Diversification Analysis</h2>', unsafe_allow_html=True)
    st.caption("Correlation Matrix · Diversification Ratio · Portfolio Correlation · Rolling Correlation")

    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(kpi("NIFTY-BANKING","0.88","Highly correlated","kpi-down"), unsafe_allow_html=True)
    c2.markdown(kpi("NIFTY-GOLD ETF","0.05","Near-zero — ideal hedge","kpi-up"), unsafe_allow_html=True)
    c3.markdown(kpi("NIFTY-USD/INR","-0.61","Natural hedge","kpi-up"), unsafe_allow_html=True)
    c4.markdown(kpi("NIFTY-IT","0.72","High positive","kpi-warn"), unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown(section("Asset Class Correlation Heatmap"), unsafe_allow_html=True)
        corr_mat = corr.values
        labels = list(corr.columns)
        fig_heat = go.Figure(go.Heatmap(
            z=corr_mat,
            x=labels, y=labels,
            colorscale=[[0,"#f85149"],[0.3,"#ff9800"],[0.5,"#21262d"],[0.7,"#1c6bc4"],[1,"#0d47a1"]],
            zmid=0, zmin=-1, zmax=1,
            text=[[f"{v:.2f}" for v in row] for row in corr_mat],
            texttemplate="%{text}",
            textfont=dict(size=11, color="#e6edf3"),
            hovertemplate="<b>%{y} vs %{x}</b><br>Correlation: %{z:.2f}<extra></extra>",
            showscale=True,
            colorbar=dict(tickfont=dict(color="#8b949e"), title=dict(text="Corr", font=dict(color="#8b949e")))
        ))
        fig_heat.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                               font=dict(color="#8b949e"), height=480,
                               xaxis=dict(tickangle=45, tickfont=dict(size=11)),
                               yaxis=dict(tickfont=dict(size=11)),
                               margin=dict(l=120,r=60,t=30,b=120))
        st.plotly_chart(fig_heat, use_container_width=True)

    with col2:
        st.markdown(section("Correlation Legend & Interpretation"), unsafe_allow_html=True)
        legend_data = [
            ("#0d47a1","#79c0ff","≥ 0.7","HIGH POSITIVE","Move together — no diversification benefit"),
            ("#1c6bc4","#79c0ff","0.5–0.7","MOD POSITIVE","Similar movement — limited benefit"),
            ("#21262d","#8b949e","0.1–0.5","LOW POSITIVE","Acceptable diversification"),
            ("#21262d","#8b949e","-0.1–0.1","NEAR ZERO","Ideal — move independently"),
            ("#7a1f1f","#fca5a5","-0.5–-0.1","NEG CORRELATION","Partial hedge — reduces risk"),
            ("#ff0000","#fca5a5","< -0.5","STRONG INVERSE","Excellent hedge — move opposite"),
        ]
        for bg, tc, rng, label, desc in legend_data:
            st.markdown(f"""<div style='background:{bg};border-radius:6px;padding:8px 12px;margin:4px 0;'>
                <span style='color:{tc};font-weight:700;font-size:11px;'>{rng} — {label}</span>
                <div style='color:#8b949e;font-size:11px;margin-top:2px;'>{desc}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""<div class='insight-box'>
            <div class='insight-title'>🔥 Key Correlation Insights</div>
            <div class='insight-row'><span class='dot-r'>●</span><span><strong>Banking & NIFTY: 0.88</strong> — one sector drives a third of index, creates systemic risk</span></div>
            <div class='insight-row'><span class='dot-g'>●</span><span><strong>Gold ETF: 0.05 with NIFTY</strong> — best portfolio hedge; 15% allocation reduces drawdown by ~8%</span></div>
            <div class='insight-row'><span class='dot-g'>●</span><span><strong>USD/INR: -0.61</strong> — currency is a natural hedge; FX ETF provides protection in war scenarios</span></div>
            <div class='insight-row'><span class='dot-a'>●</span><span><strong>Defence (0.48) + Pharma (0.42)</strong> — moderate correlation with NIFTY, genuine diversification</span></div>
        </div>""", unsafe_allow_html=True)

    # Rolling correlation
    if len(selected_stocks) >= 2 and all(s in hist.columns for s in selected_stocks[:2]):
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown(section("Rolling 63-Day Correlation Between Selected Stocks"), unsafe_allow_html=True)
        s1_name, s2_name = selected_stocks[0], selected_stocks[1]
        rc = rolling_corr(hist[s1_name], hist[s2_name])
        fig_rc = go.Figure(go.Scatter(
            x=hist["Date"], y=rc,
            fill="tozeroy",
            fillcolor="rgba(88,166,255,0.1)",
            line=dict(color="#58a6ff", width=2),
            name=f"{s1_name} vs {s2_name}",
        ))
        fig_rc.add_hline(y=0, line_color="#484f58")
        fig_rc.add_hline(y=0.7, line_dash="dash", line_color="#e3b341",
                         annotation_text="0.7 threshold", annotation_font_color="#e3b341")
        fig_rc.update_layout(**LAYOUT, height=280, yaxis=dict(range=[-1,1],gridcolor="#21262d"),
                             title=dict(text=f"63-Day Rolling Correlation: {s1_name} vs {s2_name}",
                                        font=dict(color="#e6edf3",size=13)))
        st.plotly_chart(fig_rc, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — DRAWDOWN & STRESS
# ══════════════════════════════════════════════════════════════════════════════
elif "Drawdown" in page:
    st.markdown('<h2 style="color:#e6edf3;">📉 Drawdown & Stress Analysis</h2>', unsafe_allow_html=True)
    st.caption("Drawdown Curves · Worst Loss Periods · Recovery Analysis · Stress Scenarios")

    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(kpi("NIFTY MAX DD (FY26)","-13.5%","From 26,326 Dec peak","kpi-down"), unsafe_allow_html=True)
    c2.markdown(kpi("HDFC BANK DD","-26%","From 52W high ₹1,020","kpi-down"), unsafe_allow_html=True)
    c3.markdown(kpi("RECOVERY THRESHOLD","23,500","Decisive close needed","kpi-warn"), unsafe_allow_html=True)
    c4.markdown(kpi("FY26 NIFTY MTD","-8.5%","March month-to-date","kpi-down"), unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    if selected_stocks:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(section("Drawdown Curves — Selected Stocks"), unsafe_allow_html=True)
            fig_dd = go.Figure()
            for i, stock in enumerate(selected_stocks):
                if stock not in hist.columns: continue
                s = hist[stock].dropna()
                dd = drawdown_series(s)
                fig_dd.add_trace(go.Scatter(
                    x=hist["Date"][:len(dd)], y=dd,
                    name=stock, fill="tozeroy" if i == 0 else None,
                    fillcolor=f"rgba({int(PAL[i%len(PAL)][1:3],16)},{int(PAL[i%len(PAL)][3:5],16)},{int(PAL[i%len(PAL)][5:7],16)},0.1)" if i==0 else None,
                    line=dict(color=PAL[i % len(PAL)], width=2),
                ))
            fig_dd.add_hline(y=-10, line_dash="dash", line_color="#e3b341",
                             annotation_text="-10% threshold", annotation_font_color="#e3b341")
            fig_dd.add_hline(y=-20, line_dash="dash", line_color="#f85149",
                             annotation_text="-20% danger zone", annotation_font_color="#f85149")
            fig_dd.update_layout(**LAYOUT, height=380, yaxis_ticksuffix="%",
                                 title=dict(text="Drawdown from Peak (%)", font=dict(color="#e6edf3",size=13)))
            st.plotly_chart(fig_dd, use_container_width=True)

        with col2:
            st.markdown(section("NIFTY 50 Index — 6-Month Price History"), unsafe_allow_html=True)
            lm_r = lm_hist.copy()
            fig_lm = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3],
                                   vertical_spacing=0.05)
            fig_lm.add_trace(go.Candlestick(
                x=lm_r["Date"], open=lm_r["Open"], high=lm_r["High"],
                low=lm_r["Low"], close=lm_r["Close"],
                increasing_line_color="#3fb950", decreasing_line_color="#f85149",
                name="LargeMidcap 250",
            ), row=1, col=1)
            if "Shares Traded" in lm_r.columns:
                fig_lm.add_trace(go.Bar(
                    x=lm_r["Date"], y=lm_r["Shares Traded"],
                    marker_color="#58a6ff", opacity=0.5, name="Volume",
                ), row=2, col=1)
            fig_lm.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                 font=dict(color="#8b949e"), height=380, showlegend=False,
                                 xaxis=dict(gridcolor="#21262d", rangeslider_visible=False),
                                 yaxis=dict(gridcolor="#21262d"),
                                 xaxis2=dict(gridcolor="#21262d"),
                                 yaxis2=dict(gridcolor="#21262d"),
                                 margin=dict(l=40,r=20,t=30,b=40))
            st.plotly_chart(fig_lm, use_container_width=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Stress scenario table
    st.markdown(section("Stress Scenario Analysis — Portfolio Impact"), unsafe_allow_html=True)
    stress_data = {
        "Scenario": ["Ceasefire (Bull)", "Diplomatic stalemate (Base)", "Hormuz blockade (Bear)", "RBI Emergency Hike", "FII Exit ₹2L Cr"],
        "Probability": ["25-35%","50-55%","15-25%","10-15%","20-30%"],
        "Brent Crude": ["$75-90","$95-110","$120-140","$105-115","$105-115"],
        "USD/INR": ["₹88-91","₹92-96","₹98-104","₹95-98","₹96-100"],
        "NIFTY Impact": ["+15% to +22%","-2% to +2%","-15% to -25%","-8% to -12%","-10% to -15%"],
        "Key Beneficiary": ["Banking, Auto, Aviation","IT, Pharma defensive","Gold, IT exports","Nothing","Gold ETF, IT"],
        "Key Loser": ["Gold ETF","OMCs, Aviation","Banking, Auto, Cement","Real Estate, NBFCs","Banking, Midcaps"],
    }
    st.dataframe(pd.DataFrame(stress_data), use_container_width=True, hide_index=True)

    st.markdown("""<div class='insight-box' style='border-left:4px solid #f85149;'>
        <div class='insight-title' style='color:#f85149;'>📉 Drawdown Intelligence</div>
        <div class='insight-row'><span class='dot-r'>●</span><span>Historically NIFTY falls <strong>10-15% every year</strong> from highs. Current -13.5% is within normal range. Midcap -15-25% historically.</span></div>
        <div class='insight-row'><span class='dot-r'>●</span><span><strong>IndiGo worst performer</strong> in March: -22% MTD due to ATF cost surge + airspace disruptions. ICRA cut outlook to Negative.</span></div>
        <div class='insight-row'><span class='dot-g'>●</span><span>DII buying ₹42,840 Cr prevented deeper correction. <strong>SIP floor at ₹26,000 Cr/month</strong> acts as automatic market support.</span></div>
        <div class='insight-row'><span class='dot-a'>●</span><span>NIFTY needs decisive close above <strong>23,500</strong> to confirm recovery. Failure = retest of 22,500 or lower.</span></div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 7 — MACRO & SENTIMENT
# ══════════════════════════════════════════════════════════════════════════════
elif "Macro" in page:
    st.markdown('<h2 style="color:#e6edf3;">🌍 Macro & Sentiment Dashboard</h2>', unsafe_allow_html=True)
    st.caption("VIX · Interest Rates · Inflation · Oil Prices · FII/DII · News Sentiment Score")

    # Macro KPIs
    macro_kpis = [
        ("Brent Crude","$109.9","DANGER — $110 threshold", "kpi-down"),
        ("USD/INR","₹94.82","All-time low record", "kpi-down"),
        ("India VIX","24.64","Caution zone >18", "kpi-warn"),
        ("RBI Repo","5.25%","On hold — inflation risk", "kpi-warn"),
        ("CPI Inflation","3.84%","Low but rising risk", "kpi-up"),
        ("GDP Forecast","7.3% (IMF)","GS cut to 5.9%", "kpi-warn"),
        ("Gold","$4,457/oz","Safe haven active", "kpi-up"),
        ("US 10Y Yield","4.42%","Rising — EM pressure", "kpi-down"),
    ]
    cols = st.columns(8)
    for i, (label, val, sub, col) in enumerate(macro_kpis):
        cols[i].markdown(kpi(label, val, sub, col), unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(section("FII DII Flows vs NIFTY"), unsafe_allow_html=True)
        fig_macro = make_subplots(specs=[[{"secondary_y": True}]])
        colors_fii2 = ["#f85149" if v < 0 else "#3fb950" for v in fii["FII_Net_Cr"]]
        fig_macro.add_trace(go.Bar(x=fii["Month"], y=fii["FII_Net_Cr"], name="FII Flow",
                                    marker_color=colors_fii2, opacity=0.8), secondary_y=False)
        fig_macro.add_trace(go.Bar(x=fii["Month"], y=fii["DII_Net_Cr"], name="DII Flow",
                                    marker_color="#58a6ff", opacity=0.6), secondary_y=False)
        fig_macro.add_trace(go.Scatter(x=fii["Month"], y=fii["NIFTY_Close"], name="NIFTY",
                                        line=dict(color="#e3b341", width=2.5)), secondary_y=True)
        fig_macro.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                font=dict(color="#8b949e"), height=340, barmode="group",
                                legend=dict(bgcolor="rgba(0,0,0,0)"),
                                xaxis=dict(gridcolor="#21262d"),
                                yaxis=dict(gridcolor="#21262d",title=dict(text="₹ Crore",font=dict(color="#8b949e"))),
                                yaxis2=dict(title=dict(text="NIFTY Level",font=dict(color="#e3b341")),
                                           tickfont=dict(color="#e3b341")),
                                margin=dict(l=50,r=60,t=30,b=40))
        st.plotly_chart(fig_macro, use_container_width=True)

    with col2:
        st.markdown(section("Macro Indicators Table"), unsafe_allow_html=True)
        macro_disp = macro[["Indicator","Value","Unit","Change","Signal"]].copy()

        def signal_badge(s):
            color_map = {"Bullish":"#3fb950","Bearish":"#f85149","Caution":"#e3b341",
                         "Watch":"#e3b341","Neutral":"#8b949e","Low (for now)":"#3fb950",
                         "Rising":"#f85149","Safe haven":"#3fb950","On Hold":"#e3b341",
                         "DANGER":"#f85149","Still Expanding":"#3fb950"}
            c = color_map.get(str(s), "#8b949e")
            return f'<span style="color:{c};font-weight:700;">{s}</span>'

        macro_disp["Signal_fmt"] = macro_disp["Signal"].apply(signal_badge)
        html_table = macro_disp[["Indicator","Value","Unit","Change","Signal_fmt"]].to_html(
            index=False, escape=False,
            classes="",
        ).replace('<table','<table style="width:100%;border-collapse:collapse;font-size:11px;color:#8b949e;"'
        ).replace('<th>','<th style="padding:5px 8px;background:#161b22;color:#e6edf3;font-size:10px;border-bottom:1px solid #30363d;">'
        ).replace('<td>','<td style="padding:4px 8px;border-bottom:1px solid #21262d;">')
        st.markdown(html_table, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # News sentiment score
    st.markdown(section("News Sentiment Score by Category"), unsafe_allow_html=True)
    sentiment_data = {
        "Category": ["Iran Conflict","FII Flows","Rupee/Currency","Earnings Quality","Valuation Level",
                     "RBI Policy","DII Flows","GDP Growth","Gold Price","IPL / Consumption"],
        "Score (0-10)": [2, 2, 2, 7, 8, 5, 8, 6, 9, 7],
        "Direction": ["Bearish","Bearish","Bearish","Bullish","Bullish","Neutral","Bullish","Bullish","Bullish","Bullish"],
    }
    sent_df = pd.DataFrame(sentiment_data).sort_values("Score (0-10)")
    colors_sent = ["#3fb950" if d == "Bullish" else "#f85149" if d == "Bearish" else "#e3b341"
                   for d in sent_df["Direction"]]
    fig_sent = go.Figure(go.Bar(
        x=sent_df["Score (0-10)"],
        y=sent_df["Category"],
        orientation="h",
        marker_color=colors_sent,
        text=[f"{v}/10" for v in sent_df["Score (0-10)"]],
        textposition="outside", textfont=dict(size=10, color="#8b949e"),
    ))
    fig_sent.add_vline(x=5, line_dash="dash", line_color="#484f58",
                       annotation_text="Neutral", annotation_font_color="#8b949e")
    fig_sent.update_layout(**LAYOUT, height=340, xaxis=dict(range=[0,11],gridcolor="#21262d"),
                           title=dict(text="Sentiment Score: 0=Extreme Bear, 10=Extreme Bull",
                                      font=dict(color="#e6edf3",size=12)))
    st.plotly_chart(fig_sent, use_container_width=True)

    st.markdown("""<div class='insight-box' style='border-left:4px solid #e3b341;'>
        <div class='insight-title' style='color:#e3b341;'>🌍 Macro Intelligence Summary</div>
        <div class='insight-row'><span class='dot-r'>●</span><span><strong>Rising US 10Y yields (4.42%)</strong> + Fed pause = global EM capital outflow continues. India not immune.</span></div>
        <div class='insight-row'><span class='dot-r'>●</span><span><strong>Rupee at ₹94.82</strong> — 4% fall since conflict. Each ₹1 depreciation = $1.5bn extra import bill annually.</span></div>
        <div class='insight-row'><span class='dot-g'>●</span><span><strong>India CPI at 3.84%</strong> — lowest in years but Iran-crude spike may push to 4.5-5% in March data.</span></div>
        <div class='insight-row'><span class='dot-g'>●</span><span><strong>SIP inflows ₹26,000 Cr/month</strong> — structural floor. India's retail investor base provides market resilience.</span></div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 8 — PREDICTIVE SIGNALS
# ══════════════════════════════════════════════════════════════════════════════
elif "Predictive" in page:
    st.markdown('<h2 style="color:#e6edf3;">🤖 Predictive Signals & Technical Indicators</h2>', unsafe_allow_html=True)
    st.caption("Moving Averages · RSI · Trend Signal · Volatility Forecast · Momentum")

    if selected_stocks:
        # Signal cards
        sig_cols = st.columns(min(len(selected_stocks), 5))
        for i, stock in enumerate(selected_stocks[:5]):
            if stock not in hist.columns: continue
            s = hist[stock].dropna()
            if len(s) < 20: continue
            ma50 = s.rolling(50).mean().iloc[-1] if len(s) >= 50 else None
            ma200 = s.rolling(200).mean().iloc[-1] if len(s) >= 200 else None
            rsi_val = rsi(s).iloc[-1]
            cur = s.iloc[-1]
            if ma200 and cur > ma200 and rsi_val > 50:
                sig, sc = "BULLISH", "kpi-up"
            elif ma200 and cur < ma200 and rsi_val < 50:
                sig, sc = "BEARISH", "kpi-down"
            else:
                sig, sc = "NEUTRAL", "kpi-warn"
            sig_cols[i % 5].markdown(kpi(stock, sig, f"RSI: {rsi_val:.1f}", sc), unsafe_allow_html=True)

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        # MA charts
        st.markdown(section("Moving Averages — 20, 50, 200 Day"), unsafe_allow_html=True)
        sel = st.selectbox("Select stock for MA analysis", options=selected_stocks)
        if sel in hist.columns:
            s = hist[sel].dropna()
            dates = hist["Date"][:len(s)]
            fig_ma = go.Figure()
            fig_ma.add_trace(go.Scatter(x=dates, y=s, name=sel,
                                        line=dict(color="#e6edf3", width=1.5), opacity=0.9))
            if len(s) >= 20:
                fig_ma.add_trace(go.Scatter(x=dates, y=s.rolling(20).mean(), name="20 DMA",
                                            line=dict(color="#3fb950", width=1.5, dash="dot")))
            if len(s) >= 50:
                fig_ma.add_trace(go.Scatter(x=dates, y=s.rolling(50).mean(), name="50 DMA",
                                            line=dict(color="#e3b341", width=2)))
            if len(s) >= 200:
                fig_ma.add_trace(go.Scatter(x=dates, y=s.rolling(200).mean(), name="200 DMA",
                                            line=dict(color="#f85149", width=2)))
            fig_ma.update_layout(**LAYOUT, height=380,
                                 title=dict(text=f"{sel} — Price with Moving Averages",
                                            font=dict(color="#e6edf3",size=13)))
            st.plotly_chart(fig_ma, use_container_width=True)

        # RSI + Rolling Volatility
        col1, col2 = st.columns(2)
        with col1:
            if sel in hist.columns:
                st.markdown(section("RSI — Momentum Indicator"), unsafe_allow_html=True)
                s = hist[sel].dropna()
                rsi_series = rsi(s)
                fig_rsi = go.Figure()
                fig_rsi.add_trace(go.Scatter(x=hist["Date"][:len(rsi_series)], y=rsi_series,
                                             name="RSI(14)", line=dict(color="#bc8cff", width=2)))
                fig_rsi.add_hline(y=70, line_dash="dash", line_color="#f85149",
                                  annotation_text="Overbought 70", annotation_font_color="#f85149")
                fig_rsi.add_hline(y=30, line_dash="dash", line_color="#3fb950",
                                  annotation_text="Oversold 30", annotation_font_color="#3fb950")
                fig_rsi.add_hline(y=50, line_dash="dot", line_color="#484f58")
                fig_rsi.update_layout(**LAYOUT, height=280, yaxis=dict(range=[0,100],gridcolor="#21262d"),
                                      title=dict(text=f"RSI(14) — {sel}", font=dict(color="#e6edf3",size=12)))
                st.plotly_chart(fig_rsi, use_container_width=True)

        with col2:
            if sel in hist.columns:
                st.markdown(section("Rolling 30-Day Volatility (Annualized)"), unsafe_allow_html=True)
                s = hist[sel].dropna()
                roll_vol = s.pct_change().rolling(30).std() * np.sqrt(252) * 100
                fig_rv = go.Figure()
                fig_rv.add_trace(go.Scatter(
                    x=hist["Date"][:len(roll_vol)], y=roll_vol,
                    fill="tozeroy", fillcolor="rgba(248,81,73,0.1)",
                    line=dict(color="#f85149", width=2), name="30D Ann. Vol",
                ))
                fig_rv.update_layout(**LAYOUT, height=280, yaxis_ticksuffix="%",
                                     title=dict(text=f"Rolling Volatility — {sel}",
                                                font=dict(color="#e6edf3",size=12)))
                st.plotly_chart(fig_rv, use_container_width=True)

        # Summary signal table
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown(section("Technical Signal Summary — All Selected Stocks"), unsafe_allow_html=True)
        sig_rows = []
        for stock in selected_stocks:
            if stock not in hist.columns: continue
            s = hist[stock].dropna()
            if len(s) < 50: continue
            ret = s.pct_change().dropna()
            cur = s.iloc[-1]
            ma50_v = s.rolling(50).mean().iloc[-1]
            ma200_v = s.rolling(200).mean().iloc[-1] if len(s) >= 200 else None
            rsi_v = rsi(s).iloc[-1]
            roll_v = ret.rolling(30).std().iloc[-1] * np.sqrt(252) * 100
            above200 = "✅ Above" if ma200_v and cur > ma200_v else "❌ Below"
            above50 = "✅ Above" if cur > ma50_v else "❌ Below"
            rsi_sig = "Overbought" if rsi_v > 70 else "Oversold" if rsi_v < 30 else "Neutral"
            trend = "BULLISH" if (ma200_v and cur > ma200_v and rsi_v > 50) else "BEARISH" if (ma200_v and cur < ma200_v and rsi_v < 50) else "NEUTRAL"
            sig_rows.append({
                "Stock": stock, "vs 200DMA": above200, "vs 50DMA": above50,
                "RSI(14)": round(rsi_v, 1), "RSI Signal": rsi_sig,
                "30D Vol %": round(roll_v, 1), "Trend": trend,
            })
        if sig_rows:
            st.dataframe(pd.DataFrame(sig_rows).set_index("Stock"), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 9 — NEWS INTELLIGENCE
# ══════════════════════════════════════════════════════════════════════════════
elif "News" in page:
    st.markdown('<h2 style="color:#e6edf3;">📰 Market News Intelligence & Sensitivity</h2>', unsafe_allow_html=True)
    st.caption("Latest news events · Impact analysis · Stock sensitivity scoring · Risk ratings")

    # Sensitivity KPIs
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.markdown(kpi("CRUDE SENSITIVITY","EXTREME","Primary market driver","kpi-down"), unsafe_allow_html=True)
    c2.markdown(kpi("FII FLOW SIGNAL","BEARISH","Every March day sold","kpi-down"), unsafe_allow_html=True)
    c3.markdown(kpi("GOVERNANCE RISK","HIGH","HDFC Bank probe","kpi-warn"), unsafe_allow_html=True)
    c4.markdown(kpi("VALUATION SIGNAL","ATTRACTIVE","17.5x < 5Y avg 19.6x","kpi-up"), unsafe_allow_html=True)
    c5.markdown(kpi("OVERALL SENTIMENT","5.1/10","Mixed — event-driven","kpi-warn"), unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # News cards
    news_items = [
        ("🔴 CRASH", "#f85149", "Sensex -1,690 Points | Nifty -487 | ₹8L Cr Wiped Out",
         "March 27, 2026 | Business Standard / BusinessToday",
         "Iran rejected Trump ceasefire. Brent rebounds to $109.9. Rupee hits ₹94.82 all-time low. Reliance -4.55%, IndiGo -4.54%, Bajaj Finance -4.11% led losses. Only IT sector (+0.9%) bucked trend due to rupee tailwind. 14 of 15 sector indices in red."),

        ("🔴 GEOPOLITICAL", "#f85149", "US-Iran Standoff Intensifies — Trump Extends April 6 Deadline",
         "March 26-27, 2026 | Reuters / BusinessToday",
         "Iran dismissed 15-point US ceasefire proposal. Trump extends strike pause to April 6. Iran FM confirms 'messages through intermediaries' but denies formal talks. Hormuz non-hostile transit reiterated. Binary event on April 6 — ceasefire = Nifty +10%, no deal = Nifty retest 22,000."),

        ("🔴 GOVERNANCE", "#f85149", "HDFC Bank Crisis — Chairman Resigns, AT1 Bond Probe, SEBI Review",
         "March 18-27, 2026 | Business Standard / Screener",
         "Chairman Atanu Chakraborty resigned citing ethical concerns. Three senior employees terminated for alleged mis-selling of Credit Suisse AT1 bonds to NRI clients. SEBI reviewing for rule breaches. Stock: ₹1,020 → ₹756 (-26%). With 6.4% NIFTY weight, this creates systemic index risk beyond individual stock story."),

        ("🔴 FLOWS", "#f85149", "FII Outflows ₹88,180 Cr in March — YTD Crosses ₹1 Lakh Crore",
         "March 1-27, 2026 | NSDL / Trade Brains",
         "FIIs sold every single trading day in March. Total $11 billion outflow — 2nd highest ever (Oct'24: $10.8bn). Feedback loop: crude up → INR down → FII returns worse → more selling. DII bought ₹42,840 Cr to cushion. SIP floor ₹26,000 Cr/month prevents capitulation."),

        ("🟡 MACRO", "#e3b341", "Goldman Sachs Cuts India GDP to 5.9% — CPI Raised 70bps",
         "March 24-27, 2026 | Goldman Sachs Research",
         "GDP cut from 7.3% to 5.9% — most aggressive downgrade. Every $10/bbl sustained crude increase reduces India GDP ~0.3-0.4%, widens CAD $15bn, pushes CPI +0.3%. IMF maintains 7.3%. Domestic brokerages maintain 7%+ predicated on ceasefire resolution by April 2026."),

        ("🟢 VALUATION", "#3fb950", "NIFTY PE at 17.5x — Below 5-Year Average — ICICIdirect Says Buy",
         "March 25-26, 2026 | ICICIdirect Research",
         "NIFTY now at 17.5x fwd PE vs 5Y avg 19.6x and 10Y avg 18.6x. Sentiment indicator in oversold zone. Q3 FY26 PAT +9% YoY — highest in 7 quarters. Recommendation: staggered buying on every 200-300 point NIFTY dip below 23,000. Long-term entry zone confirmed."),

        ("🟡 CURRENCY", "#e3b341", "Rupee Breaches ₹94 — Record Low — Analysts See ₹98 Risk",
         "March 27, 2026 | NDTV Business / Zerodha Pulse",
         "₹94.82 record low. 4% depreciation since conflict. Winners: IT (dollar revenues), Pharma (API exports), Auto exporters. Losers: OMCs, Aviation (ATF costs), companies with USD debt. G Chokkalingam (Equinomics): rupee returns to ₹90 post-ceasefire. Analysts: risk of ₹98 if conflict persists past June."),

        ("🟢 POSITIVE", "#3fb950", "Govt Cuts Fuel Excise — OMCs Gain ₹1,500 Cr — IPL 2026 Begins",
         "March 27-28, 2026 | NDTV / BCCI",
         "Excise duty cut provides ₹1,500 Cr relief to BPCL, HPCL, IOC. Govt takes ₹7,000 Cr revenue hit per fortnight. IPL 2026 opens March 28 — RCB vs SRH. Food delivery (Zomato), consumer FMCG, media stocks benefit from IPL season. Blinkit: 2,100+ dark stores, contribution-profitable."),
    ]

    for tag, tcolor, headline, meta, body in news_items:
        st.markdown(f"""<div class='news-card' style='border-left-color:{tcolor};border-color:{tcolor};'>
            <div><span class='news-tag' style='background:{tcolor}22;color:{tcolor};'>{tag}</span></div>
            <div class='news-headline'>{headline}</div>
            <div class='news-meta'>{meta}</div>
            <div class='news-body'>{body}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Sensitivity table
    st.markdown(section("Stock Sensitivity to News Events — Scenario Matrix"), unsafe_allow_html=True)
    sens_data = [
        ["Reliance Industries","Iran/Crude","DOWN","EXTREME","-9%","-4%","+7%","O2C margin compression"],
        ["IndiGo Aviation","Crude + Airspace","DOWN","EXTREME","-12%","-5%","+10%","ATF = 30-35% costs"],
        ["HDFC Bank","Governance probe","DOWN","HIGH","-8%","-2%","+5%","SEBI enforcement risk"],
        ["SBI / PSU Banks","FII selling","DOWN","HIGH","-7%","-3%","+8%","High FII ownership"],
        ["TCS / Infosys","Rupee depreciation","UP","LOW","+1%","+2%","+5%","Dollar revenue tailwind"],
        ["Sun Pharma","Rupee + US recovery","UP","LOW","+2%","+3%","+6%","API export earnings"],
        ["NTPC","Rate cycle + energy","MIXED","LOW","-2%","0%","+5%","Regulated cash flows"],
        ["BEL / HAL","Defence demand surge","UP","MEDIUM","+3%","+5%","+10%","Budget + geopolitical"],
        ["HUL / ITC","Rural demand + GST","MIXED","MEDIUM","-3%","+1%","+4%","Input costs vs volume"],
        ["Gold ETF","Safe haven + rupee","UP","HIGH","+8%","+3%","-3%","Ceasefire unwinds gains"],
    ]
    sens_df = pd.DataFrame(sens_data, columns=["Stock","Primary Driver","Direction","Sensitivity","Bear","Base","Bull","Key Mechanism"])

    def badge_html(sensitivity):
        cls = {"EXTREME":"badge-extreme","HIGH":"badge-high","MEDIUM":"badge-medium","LOW":"badge-low"}.get(sensitivity,"badge-medium")
        return f'<span class="badge {cls}">{sensitivity}</span>'
    def dir_html(d):
        c = "#3fb950" if d=="UP" else "#f85149" if d=="DOWN" else "#e3b341"
        return f'<span style="color:{c};font-weight:700;">{d}</span>'

    sens_df["Sensitivity"] = sens_df["Sensitivity"].apply(badge_html)
    sens_df["Direction"] = sens_df["Direction"].apply(dir_html)
    html_sens = sens_df.to_html(index=False, escape=False).replace(
        '<table','<table style="width:100%;border-collapse:collapse;font-size:12px;color:#8b949e;"'
    ).replace('<th>','<th style="padding:7px 10px;background:#161b22;color:#e6edf3;font-size:11px;border-bottom:1px solid #30363d;text-align:left;">'
    ).replace('<td>','<td style="padding:6px 10px;border-bottom:1px solid #21262d;">')
    st.markdown(html_sens, unsafe_allow_html=True)

    # Final composite risk chart
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown(section("Overall Market Risk Dashboard — Composite Gauge"), unsafe_allow_html=True)
    risk_cats = ["Geopolitical","FII Flow","Currency","Volatility (VIX)","Earnings","Valuation","DII Support","Sentiment"]
    risk_scores = [8, 8, 8, 6, 5, 3, 3, 5]  # 10=max risk/bearish
    colors_r = ["#f85149" if v >= 7 else "#e3b341" if v >= 5 else "#3fb950" for v in risk_scores]
    fig_risk = go.Figure()
    fig_risk.add_trace(go.Bar(
        x=risk_scores, y=risk_cats, orientation="h",
        marker_color=colors_r,
        text=[f"{v}/10" for v in risk_scores],
        textposition="outside", textfont=dict(size=11, color="#8b949e"),
    ))
    fig_risk.add_vline(x=5, line_dash="dash", line_color="#484f58",
                       annotation_text="Neutral (5)", annotation_font_color="#8b949e")
    fig_risk.update_layout(**LAYOUT, height=340,
                           xaxis=dict(range=[0,11],gridcolor="#21262d"),
                           title=dict(text="Risk Score: 10=Extreme Bear, 1=Extreme Bull",
                                      font=dict(color="#e6edf3",size=12)))
    st.plotly_chart(fig_risk, use_container_width=True)
