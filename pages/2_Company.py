import streamlit as st
from sidebar import render_sidebar
import yfinance as yf 
import plotly.graph_objects as go
import requests
import pandas as pd

st.set_page_config(page_title="Company", layout="wide")
render_sidebar()

FRED_API_KEY = "550575063d86c0bab2304db1f270b915"

@st.cache_data(ttl=3600)
def get_fred_data(series_id):
    try:
        url = "https://api.stlouisfed.org/fred/series/observations"

        params = {
            "series_id": series_id,
            "api_key": FRED_API_KEY,
            "file_type": "json",
            "sort_order": "desc",
            "limit": 1
        }

        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        value = data["observations"][0]["value"]
        return float(value)

    except:
        return None
    
@st.cache_data(ttl=3600)
def get_inflation(country):

    if country == "United States":
        series_id = "CPIAUCSL"   # US CPI
    elif country == "India":
        series_id = "INDCPIALLMINMEI"  # India CPI
    else:
        return None

    try:
        url = "https://api.stlouisfed.org/fred/series/observations"

        params = {
            "series_id": series_id,
            "api_key": FRED_API_KEY,
            "file_type": "json",
            "sort_order": "desc",
            "limit": 13   # get 13 months (for YoY comparison)
        }

        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        observations = data["observations"]

        latest_value = float(observations[0]["value"])
        last_year_value = float(observations[12]["value"])

        inflation_rate = ((latest_value - last_year_value) / last_year_value) * 100

        latest_date = observations[0]["date"]

        return round(inflation_rate, 2), latest_date

    except:
        return None

@st.cache_data(ttl=3600)
def get_unemployment(country):

    if country == "United States":
        series_id = "UNRATE"
    elif country == "India":
        series_id = "LRUNTTTTINM156S"
    else:
        return None

    return get_fred_data(series_id)


st.markdown("""
<style>
section[data-testid="stSidebar"] nav
 {
    display: none !important;
    height: 0 !important;
}
[data-testid="stSidebarNav"] {
    display: none !important;
    height: 0 !important;
}
/* Sidebar background to match home page */
[data-testid="stSidebar"] {
    background-color: #0b1220 !important;
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Sidebar text */
[data-testid="stSidebar"] * {
    color: #e5e7eb !important;
}

/* Buttons inside sidebar */
[data-testid="stSidebar"] button {
    background-color: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: #e5e7eb !important;
    border-radius: 10px;
}

/* Hover effect */
[data-testid="stSidebar"] button:hover {
    background-color: rgba(99,102,241,0.15) !important;
    border-color: #6366f1 !important;
}

/* Hide default multipage nav (extra safety) */
section[data-testid="stSidebar"] nav {
    display: none !important;
}
[data-testid="stSidebarNav"] {
    display: none !important;
}
            


            


  /* Main Background */
[data-testid="stAppViewContainer"] {
    background-color: #0f172a !important;
}

/* Headings & Text */
h1, h2, h3, h4, h5, p, label {
    color: #ffffff !important;
}

/* KPI Cards - Investor Style */
div[data-testid="metric-container"] {
    background: #111827 !important;
    border-radius: 18px;
    padding: 24px;
    border: 1px solid rgba(59,130,246,0.35);
    box-shadow:
        0px 8px 30px rgba(0,0,0,0.7),
        0px 0px 25px rgba(59,130,246,0.45);
}

/* KPI Label */
div[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    color: #cbd5e1 !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}

/* KPI Value */
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 30px !important;
    font-weight: 800 !important;
}
            


/* title colouring for chilling */
            
            /* COMPANY DASHBOARD HEADER STYLE */
.company-header {
    background: rgba(17, 24, 39, 0.6);
    backdrop-filter: blur(8px);
    padding: 18px 28px;
    border-radius: 16px;
    border: 1px solid rgba(59,130,246,0.25);
    box-shadow: 0px 8px 20px rgba(0,0,0,0.6);
    margin-bottom: 25px;
}   

    

</style>
""", unsafe_allow_html=True)



st.title("🏢 Company Dashboard")
st.write("Welcome to Company view")


st.markdown(
    "<h2 style='color:#93c5fd; font-weight:100; text-shadow:0 0 10px rgba(59,130,246,0.4);'>Real Time Financial Metrics</h2>",
    unsafe_allow_html=True
)




companies = {
    "Apple (AAPL)": "AAPL",
    "Exxon Mobil (XOM)": "XOM",
    "Mastercard (MA)": "MA",
    "Microsoft (MSFT)": "MSFT",
    "Citi Bank (C)": "C",
    "Google (GOOGL)": "GOOGL",
    "Amazon (AMZN)": "AMZN",
    "Tesla (TSLA)": "TSLA",
    "Meta (META)": "META",
    "Nvidia (NVDA)": "NVDA",
    "Reliance (RELIANCE.NS)": "RELIANCE.NS",
    "TCS (TCS.NS)": "TCS.NS",
    "Broadcom (AVGO)": "AVGO",
    "Qualcomm (QCOM)": "QCOM",
    "AMD (AMD)": "AMD",
    "Intel (INTC)": "INTC",
    "Netflix (NFLX)": "NFLX",
    "Adobe (ADBE)": "ADBE",
    "Salesforce (CRM)": "CRM",
    "Oracle (ORCL)": "ORCL",
    "HDFC Bank (HDFCBANK.NS)": "HDFCBANK.NS"
}

selected_company = st.selectbox(
    "Select Company",
    list(companies.keys())
)



ticker_symbol = companies[selected_company]
ticker = yf.Ticker(ticker_symbol)

# Use fast_info (more stable than info)
info = ticker.fast_info


# KPI SECTION




st.markdown("###  Key Financial Indicators")

info = ticker.info

market_cap = info.get("marketCap")
current_price = info.get("currentPrice")
pe_ratio = info.get("trailingPE")
high_52 = info.get("fiftyTwoWeekHigh")
low_52 = info.get("fiftyTwoWeekLow")

def format_value(val, prefix="$", decimals=2):
    if val is None:
        return "N/A"
    if isinstance(val, (int, float)):
        if prefix == "$":
            return f"{prefix}{val:,.{decimals}f}"
        return f"{val:.{decimals}f}"
    return "N/A"

range_52 = f"{low_52} - {high_52}" if high_52 and low_52 else "N/A"

st.markdown(f"""
<style>
.kpi-row {{
    display: flex;
    gap: 20px;
    margin-top: 15px;
}}

.kpi-box {{
    flex: 1;
    background: #111827;
    padding: 24px;
    border-radius: 18px;
    border: 1px solid rgba(59,130,246,0.4);
    box-shadow: 0 0 25px rgba(59,130,246,0.35);
}}

.kpi-title {{
    font-size: 14px;
    color: #cbd5e1;
    font-weight: 600;
}}

.kpi-number {{
    font-size: 30px;
    font-weight: 800;
    color: white;
    margin-top: 8px;
}}
</style>

<div class="kpi-row">
    <div class="kpi-box">
        <div class="kpi-title">Market Cap</div>
        <div class="kpi-number">{format_value(market_cap)}</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-title">Current Price</div>
        <div class="kpi-number">{format_value(current_price)}</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-title">P/E Ratio</div>
        <div class="kpi-number">{format_value(pe_ratio, prefix="", decimals=2)}</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-title">52W Range</div>
        <div class="kpi-number">{range_52}</div>
    </div>
</div>
""", unsafe_allow_html=True)




# Company Overview 

st.markdown("<br>",unsafe_allow_html=True)
st.markdown("###  Company Overview")
country=info.get("country","N/A")
if country in ["USA","US"]:
    country="United States"

sector = info.get("sector", "N/A")
industry = info.get("industry", "N/A")
employees = info.get("fullTimeEmployees", "N/A")
description = info.get("longBusinessSummary", "No description available.")


ceo_name = "N/A"
officers = info.get("companyOfficers")

if officers and isinstance(officers, list):
    for officer in officers:
        title = officer.get("title", "")
        if "CEO" in title or "Chief Executive Officer" in title:
            ceo_name = officer.get("name", "N/A")
            break

# Layout
col1, col2 = st.columns(2)

with col1:
    st.write(f"*Sector:* {sector}")
    st.write(f"*Industry:* {industry}")

with col2:
    st.write(f"*CEO:* {ceo_name}")
    st.write(f"*Employees:* {employees:,}" if isinstance(employees, int) else f"*Employees:* {employees}")

st.markdown("---")

# Description Box
st.markdown(
    f"""
    <div style="
        background-color:#111827;
        padding:18px;
        border-radius:12px;
        border:1px solid rgba(59,130,246,0.25);
        line-height:1.6;
        font-size:14px;
        color:#e5e7eb;">
        {description[:800]}...
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>",unsafe_allow_html=True)

st.markdown(f"*Country:* {country}")


inflation_data = get_inflation(country)

if inflation_data:
    inflation_rate, inflation_date = inflation_data
    
  
    formatted_date = pd.to_datetime(inflation_date).strftime("%B %Y")
    
    st.info(
        f"{country} Inflation: {inflation_rate}% (Year-over-Year)\n\n"
        f"Latest Available Data: {formatted_date}"
    )
else:
    st.warning("Inflation data not available.")


unemployment_value = get_unemployment(country)
if unemployment_value:
    st.info(f"Unemployment Rate: {unemployment_value}%")
else:
    st.warning("Unemployment data not available.")







st.markdown("###  Select Time Range")

period = st.selectbox(
    "Choose Period",
    ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
    index=2  # default = 6mo
)

history = ticker.history(period=period)
if not history.empty:
    start_date = history.index.min()
    end_date = history.index.max()

    st.info(
        f"📅 Data Range: {start_date.strftime('%d %b %Y')} – "
        f"{end_date.strftime('%d %b %Y')} | "
        f"📡 Source: Yahoo Finance"
    )




st.markdown("<br>",unsafe_allow_html=True)
# st.markdown("### 📈 6 Month Price Trend")
st.markdown(f"###  {period.upper()} Price Trend")


if not history.empty:

    # Detect trend direction
    start_price = history["Close"].iloc[0]
    end_price = history["Close"].iloc[-1]

    if end_price >= start_price:
        line_color = "#2284c5"   # Green
        fill_color = "rgba(34,197,94,0.08)"
    else:
        line_color = "#ef4444"   # Red
        fill_color = "rgba(239,68,68,0.08)"

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=history.index,
        y=history["Close"],
        mode="lines",
        line=dict(color=line_color, width=3),
        fill="tozeroy",
        fillcolor=fill_color,
        hovertemplate="<b>Date:</b> %{x}<br><b>Price:</b> $%{y:.2f}<extra></extra>"
    ))

    fig.update_layout(
        height=380,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor="#0f172a",
        paper_bgcolor="#0f172a",
        font=dict(color="white"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)")
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("No historical data available.")






#  Risk Analysis 

st.markdown("### ⚠ Risk Analysis (6M Volatility)")

if not history.empty:

    # Calculate daily returns
    history["Returns"] = history["Close"].pct_change()

    volatility = history["Returns"].std() * (252 ** 0.5)  # Annualized

    # Risk Categorization
    if volatility < 0.2:
        risk_level = "Low Risk"
        risk_color = "#22c55e"
    elif volatility < 0.4:
        risk_level = "Moderate Risk"
        risk_color = "#facc15"
    else:
        risk_level = "High Risk"
        risk_color = "#ef4444"

    st.markdown(f"""
    <div style="
        background:#111827;
        padding:20px;
        border-radius:16px;
        border:1px solid rgba(59,130,246,0.3);
        box-shadow:0 0 20px rgba(59,130,246,0.25);
        text-align:center;
    ">
        <div style="font-size:14px; color:#94a3b8;">
            Annualized Volatility
        </div>
        <div style="font-size:28px; font-weight:800; color:white;">
            {volatility:.2f}
        </div>
        <div style="margin-top:8px; font-weight:600; color:{risk_color};">
            {risk_level}
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    st.info("Not enough data to calculate risk.")




st.markdown("<br>",unsafe_allow_html=True)

#ai
def get_company_summary(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info
    return info.get("longBusinessSummary", "")



def calculate_ai_exposure(summary_text):
    keywords = [
        "artificial intelligence",
        "ai",
        "machine learning",
        "cloud",
        "data center",
        "semiconductor",
        "automation",
        "deep learning",
        "neural"
    ]

    summary_text = summary_text.lower()
    
    score = sum(summary_text.count(word) for word in keywords)

    if score >= 5:
        return "High 🚀"
    elif score >= 2:
        return "Medium "
    else:
        return "Low"
    


summary = get_company_summary(ticker_symbol)
ai_exposure = calculate_ai_exposure(summary)

st.markdown(f"""
### 🤖 AI Exposure: *{ai_exposure}*
""")


# STRATEGIC INSIGHT 


st.markdown("### 🧠 Strategic Insight")

insight = ""

if pe_ratio:
    if pe_ratio > 30:
        insight += "• Stock appears relatively overvalued based on P/E ratio.\n"
    elif pe_ratio < 15:
        insight += "• Stock may be undervalued compared to market average.\n"
    else:
        insight += "• Stock valuation appears moderate.\n"

if market_cap:
    if market_cap > 500_000_000_000:
        insight += "• Large Cap company — generally stable with lower volatility.\n"
    elif market_cap > 50_000_000_000:
        insight += "• Mid/Large Cap — balanced growth & stability.\n"
    else:
        insight += "• Smaller cap — potentially higher growth with higher risk.\n"

if high_52 and current_price:
    if current_price > 0.9 * high_52:
        insight += "• Trading near 52-week high — bullish momentum.\n"
    elif current_price < 1.1 * low_52:
        insight += "• Trading near 52-week low — possible recovery opportunity.\n"

if insight:
    st.success(insight)
else:
    st.info("Insufficient data to generate insights.")