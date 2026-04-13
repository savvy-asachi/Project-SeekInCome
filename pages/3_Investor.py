import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import requests
import time
from sidebar import render_sidebar
import numpy as np
import plotly.graph_objects as go


render_sidebar()



st.set_page_config(
    page_title="Investor Dashboard",
    layout="wide"
)



conn = sqlite3.connect("sql.db")

df = pd.read_sql("SELECT * FROM company_data", conn)

conn.close()






API_KEY=st.secrets["FMP_API"]

st.write("API LOADED",API_KEY is not None)



def get_live_changes_batch(ticker_list):
    try:
        symbols = ",".join(ticker_list)

        url = f"https://financialmodelingprep.com/api/v3/quote/{symbols}?apikey={API_KEY}"
        response = requests.get(url, timeout=8)
          

        if response.status_code != 200:
            return {}

        data = response.json()

        # Create dictionary: {ticker: changePercentage}
        return {
            item["symbol"]: item.get("changePercentage",item.get("changesPercentage",0)) 
            for item in data
        }

    except:
        return {}


@st.cache_data(ttl=300)
def update_live_data(df):
    df_live = df.copy()



    ticker_list = df_live["Ticker"].tolist()

    
    live_changes = get_live_changes_batch(ticker_list)
   

   
    df_live["currently"] = df_live["Ticker"].map(live_changes).fillna(0)

    return df_live



df_live = update_live_data(df)



# #  Calculate Emerging Score AFTER live update
# df_live["Emerging Score"] = (
#     df_live["currently"] * 0.7 +
#     (1 / df_live["Market cap"].replace(0, 1)) * 1e12 * 0.3
# )




st.markdown("""
<style>
section[data-testid="stSidebar"] nav {
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

/* Sidebar labels only */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
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

            

            /* css for calculator button*/

/*  Force slider filled portion BLUE */
div[data-baseweb="slider"] div[class*="track"] {
    background-color: #1f77ff !important;
}

/*  Force active filled rail BLUE */
div[data-baseweb="slider"] div[class*="innerTrack"] {
    background-color: #1f77ff !important;
}

/*  Make slider handle BLUE */
div[data-baseweb="slider"] div[role="slider"] {
    background-color: #1f77ff !important;
    border-color: #1f77ff !important;
}

/*  Keep metric values WHITE */
[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-weight: 700 !important;
}


    /*kpi*/

   .kpi-card {
    background: linear-gradient(135deg, #1f2937, #111827);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    color: white;
    border: 1px solid rgba(59,130,246,0.4);
    box-shadow: 0 0 15px rgba(59,130,246,0.5);
    transition: 0.3s ease-in-out;
}

.kpi-card:hover {
    box-shadow: 0 0 25px rgba(59,130,246,0.9);
    transform: translateY(-5px);
}

.kpi-title {
    font-size: 16px;
    opacity: 0.8;
}

.kpi-value {
    font-size: 28px;
    font-weight: bold;
    margin-top: 10px;
}     

/*colour button*/
            /* Selected multiselect tags */
/* Multiselect selected tags */
span[data-baseweb="tag"] {
    background-color: #1f77ff !important;
    color: white !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}


/* Emerging Picks Cards */
.emerging-card {
    background: linear-gradient(135deg, #111827, #0f172a);
    padding: 18px;              /* reduced from 25px */
    border-radius: 12px;
    text-align: center;
    color: white;
    border: 1px solid rgba(59,130,246,0.4);
    box-shadow: 0 0 12px rgba(59,130,246,0.6);
    transition: 0.3s ease-in-out;
    min-height: 120px;          /* keeps it compact */
}

.emerging-card:hover {
    box-shadow: 0 0 20px rgba(59,130,246,0.9);
    transform: translateY(-4px);
}

.emerging-title {
    font-size: 18px;            /* was too large */
    font-weight: 600;
    margin-bottom: 8px;
    color: #ffffff;             /* force white */
}

.emerging-score {
    font-size: 16px;            /* smaller */
    font-weight: 500;
    color: #60a5fa;             /* clean blue */
}  


            /* drop down*/

/* Select input box */
div[data-baseweb="select"] > div {
    background-color: #1f2937 !important;
    color: white !important;
}

/* Dropdown menu background */
div[data-baseweb="menu"] {
    background-color: #1f2937 !important;
}

/* Each dropdown option */
div[data-baseweb="menu"] ul li {
    background-color: #1e1e1e !important;
    color: #ffffff !important;
    font-weight: 500 !important;
}

/* Hover state */
div[data-baseweb="menu"] ul li:hover {
    background-color: #374151 !important;
    color: #ffffff !important;
}

/* Selected tags */
span[data-baseweb="tag"] {
    background-color: #1f77ff !important;
    color: white !important;
}
 /* Make metric values light blue (works in both themes) */
[data-testid="stMetricValue"] {
    color: #60a5fa !important;   /* clean light blue */
    font-weight: 700 !important;
}

/* Optional: metric label slightly lighter */
[data-testid="stMetricLabel"] {
    color: #cbd5e1 !important;
}
            
            /*comparion calculator */


            

            
</style>
            


""", unsafe_allow_html=True)







if "theme" not in st.session_state:
    st.session_state.theme = "🌙"


col1, col2 = st.columns([17,1])

with col2:
    st.markdown(
        '<div style="margin-top:45px;">',
        unsafe_allow_html=True
    )

    with st.popover("⚙️"):
        st.markdown("")
        selected_theme = st.radio(
            "",
            ["🌙", "☀️"],
            index=0 if st.session_state.theme == "🌙" else 1
        )
        st.session_state.theme = selected_theme

    st.markdown("</div>", unsafe_allow_html=True)


#  APPLY THEME

if st.session_state.theme == "🌙":
    bg_color = "linear-gradient(135deg, #0f172a, #1e293b)"
    text_color = "#e5e7eb"
    popover_text = "#e5e7eb"
    popover_bg = "#1e293b"
else:
    bg_color = "#f8fafc"
    text_color = "#111827"
    popover_text = "#111827"
    popover_bg = "#ffffff"

st.markdown(f"""
<style>

.stApp {{
    background: {bg_color};
}}

.block-container {{
    padding-top: 2rem;
}}

h1, h2, h3, h4, h5, h6, p, label {{
    color: {text_color} !important;
}}

/* Proper Popover Styling */
div[data-baseweb="popover"] {{
    background: {popover_bg} !important;
    border-radius: 16px !important;
    box-shadow: 0 15px 40px rgba(0,0,0,0.25) !important;
}}

div[data-baseweb="popover"] * {{
    color: {popover_text} !important;
}}



</style>
""", unsafe_allow_html=True)



# PAGE CONTENT

st.title("📊 Investor Dashboard")
st.write("Welcome to the investor view.")

# ---------------- KPI SECTION ---------------- #

total_market_cap = df["Market cap"].sum()
total_market_cap_trillion = round(total_market_cap / 1e12, 2)

largest_company = df.loc[df["Market cap"].idxmax(), "Company_Name"]
top_gainer = df_live.loc[df_live["currently"].idxmax(), "Company_Name"]
avg_daily_move = round(df["currently"].mean(), 2)

col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"""
<div class="kpi-card">
    <div class="kpi-title">Total Market Cap</div>
    <div class="kpi-value">${total_market_cap_trillion} T</div>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class="kpi-card">
    <div class="kpi-title">Largest Company</div>
    <div class="kpi-value">{largest_company}</div>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div class="kpi-card">
    <div class="kpi-title">Top Gainer</div>
    <div class="kpi-value">{top_gainer}</div>
</div>
""", unsafe_allow_html=True)

col4.markdown(f"""
<div class="kpi-card">
    <div class="kpi-title">Avg Daily Move</div>
    <div class="kpi-value">{avg_daily_move}%</div>
</div>
""", unsafe_allow_html=True)


#  INLINE FILTER 

def classify_market_cap(cap):
    if cap >= 1e12:
        return "Mega Cap (1T+)"
    elif cap >= 5e11:
        return "Large Cap (500B - 1T)"
    else:
        return "Mid Cap"

df["Cap Category"] = df["Market cap"].apply(classify_market_cap)

st.divider()

st.markdown("###  Filter by Market Cap Category")

cap_filter = st.multiselect(
    "Select Category",
    options=df["Cap Category"].unique(),
    default=df["Cap Category"].unique()
)

filtered_df = df[df["Cap Category"].isin(cap_filter)]


# CHART SECTION 

st.markdown("###  Top 10 Companies by Market Cap")

top10 = filtered_df.sort_values(
    by="Market cap",
    ascending=False
).head(10)

fig = px.bar(
    top10,
    x="Company_Name",
    y="Market cap",
    color="Market cap",
    title="Top 10 by Market Capitalization"
)


fig.update_layout(
    template="plotly_dark",
    height=350,       
    width=900,
    xaxis_title="Company",
    yaxis_title="Market Cap"
)
  

num_companies = len(top10)

if num_companies <= 3:
    fig.update_traces(width=0.25)
elif num_companies <= 6:
    fig.update_traces(width=0.45)
else:
    fig.update_traces(width=0.6)
st.plotly_chart(fig, use_container_width=True)









st.markdown("##  Emerging Growth Opportunities")





# Use LIVE dataframe (important)
max_cap = df_live["Market cap"].max()

df_live["Emerging Score"] = (
    (df_live["currently"] * 5) +                 
    ((max_cap - df_live["Market cap"]) / max_cap * 10)
)



# Sort by Emerging Score
emerging_top = df_live.sort_values(
    by="Emerging Score",
    ascending=False
).head(7)

# Chart 

fig_emerging = px.bar(
    emerging_top,
    x="Company_Name",
    y="Emerging Score",
    color="Emerging Score",
    title="Top Emerging Growth Picks",
)

fig_emerging.update_layout(
    template="plotly_dark",
    height=380,
    bargap=0.5,
    xaxis_title="Company",
    yaxis_title="Emerging Growth Score"
)

fig_emerging.update_traces(width=0.4)

st.plotly_chart(fig_emerging, use_container_width=True)

st.caption(
    "Emerging Score is calculated using momentum and relative market size. "
    "Higher score indicates higher short-term growth potential."
)





top2 = emerging_top.head(2)

st.markdown("###  Top 2 Emerging Picks")

col1, col2 = st.columns(2)

for i, (_, row) in enumerate(top2.iterrows()):
    card_html = f"""
    <div class="emerging-card">
        <div class="emerging-title">Emerging Pick #{i+1}</div>
        <div class="emerging-company">{row['Company_Name']}</div>
        <div class="emerging-score">Score: {round(float(row['Emerging Score']),2)}</div>
    </div>
    """

    if i == 0:
        col1.markdown(card_html, unsafe_allow_html=True)
    else:
        col2.markdown(card_html, unsafe_allow_html=True)




st.markdown("---")

st.markdown("##  SIP Investment Calculator")




# Input Section

col1, col2, col3 = st.columns(3)

with col1:
    monthly_investment = st.number_input(
        "Monthly Investment (₹)",
        min_value=500,
        value=5000,
        step=500,
        key="sip_monthly"
    )

with col2:
    annual_return = st.slider(
        "Expected Annual Return (%)",
        min_value=5,
        max_value=25,
        value=12,
        key="sip_return"
    )

with col3:
    years = st.slider(
        "Investment Duration (Years)",
        min_value=1,
        max_value=30,
        value=10,
        key="sip_years"
    )


# SIP Calculation Function

def calculate_sip(monthly, annual_return, years):
    r = annual_return / 100 / 12
    n = years * 12

    maturity = monthly * (((1 + r) ** n - 1) / r) * (1 + r)
    invested = monthly * n
    wealth = maturity - invested

    return invested, wealth, maturity


# Calculate
invested, wealth, maturity = calculate_sip(
    monthly_investment,
    annual_return,
    years
)


# Results Section

st.markdown("###  Investment Summary")

res1, res2, res3 = st.columns(3)

with res1:
    st.metric("Total Invested", f"₹ {invested:,.0f}")

with res2:
    st.metric("Wealth Gained", f"₹ {wealth:,.0f}")

with res3:
    st.metric("Maturity Value", f"₹ {maturity:,.0f}")



# Growth Breakdown Chart


st.markdown("# SIP Growth Breakdown")

months = years * 12
monthly_rate = annual_return / 100 / 12

portfolio_values = []
invested_values = []

current_value = 0

for month in range(1, months + 1):
    current_value = (current_value + monthly_investment) * (1 + monthly_rate)
    portfolio_values.append(current_value)
    invested_values.append(monthly_investment * month)

df_chart = pd.DataFrame({
    "Month": range(1, months + 1),
    "Invested Amount": invested_values,
    "Portfolio Value": portfolio_values
})

st.line_chart(
    df_chart.set_index("Month"),
    height=320,
    use_container_width=True
)

st.caption("The gap between invested amount and portfolio value represents wealth created through compounding.")


st.markdown("###  Portfolio Composition")

import plotly.graph_objects as go

fig = go.Figure()

# Invested Amount (Base)
fig.add_trace(go.Bar(
    name="Total Invested",
    x=["Portfolio Value"],
    y=[invested],
    text=[f"₹ {invested:,.0f}"],
    textposition="inside"
))

# Wealth Gained (Stacked on top)
fig.add_trace(go.Bar(
    name="Wealth Gained",
    x=["Portfolio Value"],
    y=[wealth],
    text=[f"₹ {wealth:,.0f}"],
    textposition="inside"
))

fig.update_layout(
    barmode="stack",
    height=400,
    yaxis_title="Amount (₹)",
    xaxis_title="",
)

st.plotly_chart(fig, use_container_width=True)
st.divider()

st.markdown("#  SIP Risk Comparison")


# Realistic Risk Mapping

investment_options = {
    "Fixed Deposit (Low Risk)": {
        "default_return": 6,
        "opposite": "Small Cap Fund (High Risk)"
    },
    "Large Cap Fund": {
        "default_return": 11,
        "opposite": "Small Cap Fund (High Risk)"
    },
    "Index Fund": {
        "default_return": 11,
        "opposite": "Mid Cap Fund"
    },
    "Mid Cap Fund": {
        "default_return": 14,
        "opposite": "Large Cap Fund"
    },
    "Small Cap Fund (High Risk)": {
        "default_return": 17,
        "opposite": "Fixed Deposit (Low Risk)"
    }
}

col1, col2 = st.columns(2)


# Scenario A – User Strategy

with col1:
    st.markdown("### 🔹 Your Investment Strategy")

    type_a = st.selectbox(
        "Select Investment Type",
        list(investment_options.keys())
    )

    monthly = st.number_input(
        "Monthly Investment (₹)",
        min_value=500,
        value=5000,
        step=500
    )

    years = st.slider(
        "Investment Duration (Years)",
        1,
        30,
        10
    )

    # Allow user to adjust expected return
    return_a = st.slider(
        "Adjust Expected Annual Return (%)",
        5,
        25,
        investment_options[type_a]["default_return"]
    )


# Scenario B  Opposite Strategy

with col2:
    st.markdown("### ⚖ Opposite Risk Strategy")

    type_b = investment_options[type_a]["opposite"]
    return_b = investment_options[type_b]["default_return"]

    st.info(f"Opposite Strategy: {type_b}")
    st.write(f"Assumed Return: {return_b}%")


# SIP Calculation

def calculate_sip(monthly, annual_return, years):
    r = annual_return / 100 / 12
    n = years * 12

    invested = monthly * n
    current_value = 0
    values = []

    for _ in range(n):
        current_value = (current_value + monthly) * (1 + r)
        values.append(current_value)

    maturity = values[-1]
    wealth = maturity - invested

    return invested, wealth, maturity, values

# Calculate both strategies
invested_a, wealth_a, maturity_a, values_a = calculate_sip(monthly, return_a, years)
invested_b, wealth_b, maturity_b, values_b = calculate_sip(monthly, return_b, years)


# Results Comparison

st.markdown("###  Results Comparison")

res1, res2 = st.columns(2)

with res1:
    st.markdown("#### 🔹 Your Strategy")
    st.metric("Total Invested", f"₹ {invested_a:,.0f}")
    st.metric("Wealth Created", f"₹ {wealth_a:,.0f}")
    st.metric("Maturity Value", f"₹ {maturity_a:,.0f}")

with res2:
    st.markdown("#### ⚖ Opposite Strategy")
    st.metric("Total Invested", f"₹ {invested_b:,.0f}")
    st.metric("Wealth Created", f"₹ {wealth_b:,.0f}")
    st.metric("Maturity Value", f"₹ {maturity_b:,.0f}")


# Growth Visualization

st.markdown("###  Growth Comparison")

months = years * 12
invested_progress = [monthly * i for i in range(1, months + 1)]

chart_data = pd.DataFrame({
    "Month": range(1, months + 1),
    "Invested Amount": invested_progress,
    "Your Strategy Value": values_a,
    "Opposite Strategy Value": values_b
})

st.line_chart(chart_data.set_index("Month"))

st.caption("The gap between invested amount and portfolio value represents wealth created through compounding.")





# Contribution vs Wealth Created

st.markdown("### Contribution vs Wealth Created")

fig = go.Figure()


fig.add_bar(
    name="Total Invested",
    x=["Your Strategy", "Opposite Strategy"],
    y=[invested_a, invested_b],
    marker_color="#1f77b4"   
)

# Wealth Created
fig.add_bar(
    name="Wealth Created",
    x=["Your Strategy", "Opposite Strategy"],
    y=[wealth_a, wealth_b],
    marker_color="#87CEEB"   
)

fig.update_layout(
    barmode="stack",
    height=420,
    yaxis_title="Amount (₹)",
    legend_title="Breakdown",
    template="plotly_white",
    margin=dict(l=20, r=20, t=40, b=20)
)

fig.update_yaxes(tickprefix="₹ ", separatethousands=True)

st.plotly_chart(fig, use_container_width=True)

st.caption(
    "Each bar represents final portfolio value split into invested amount (base) and wealth created (top)."
)


# Professional Disclaimer

st.info(
    "Returns shown are assumed average annual returns for comparison purposes. "
    "Actual market returns vary and higher returns generally involve higher risk and volatility."
)



# Intelligent Strategy Insight


difference = maturity_b - maturity_a

st.markdown("### 🧠 Strategic Insight")

if difference > 0:
    better_strategy = "Opposite Strategy"
    better_value = maturity_b
    better_wealth = wealth_b
    gap = difference
else:
    better_strategy = "Your Strategy"
    better_value = maturity_a
    better_wealth = wealth_a
    gap = abs(difference)

if difference != 0:
    st.success(
        f"{better_strategy} may generate ₹ {gap:,.0f} more over {years} years."
    )
    
    st.info(
        f"Portfolio Value: ₹ {better_value:,.0f} | "
        f"Wealth Created: ₹ {better_wealth:,.0f}"
    )
else:
    st.info("Both stratergy have similar results no major change")