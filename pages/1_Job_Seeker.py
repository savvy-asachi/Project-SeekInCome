import streamlit as st
from sidebar import render_sidebar
import sqlite3
import pandas as pd
import plotly.express as px
import yfinance as yf 
st.markdown("""
<style>
            

.dashboard-card {
    background: linear-gradient(
        180deg,
        rgba(15, 23, 42, 0.95),
        rgba(2, 6, 23, 0.95)
    );
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 26px 28px;
    margin-bottom: 28px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.45);
}

/* Section title */
.section-title {
    font-size: 28px;
    font-weight: 700;
    color: #e5e7eb;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 10px;
}
            



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
            

            
       /* Selected multiselect pills */
span[data-baseweb="tag"] {
    background-color: #6366f1 !important;  /* Indigo / graph blue */
    color: white !important;
    border-radius: 8px !important;
    font-weight: 500;
}

/* Remove 'x' button background */
span[data-baseweb="tag"] svg {
    color: white !important;
}

/* Hover effect */
span[data-baseweb="tag"]:hover {
    background-color: #4f46e5 !important;
} 
                
         

</style>
""", unsafe_allow_html=True)
         



# ---------------- SIDEBAR (SINGLE CALL ONLY) ----------------
st.set_page_config(
    page_title="Job Seeker Dashboard",
    layout="wide"
)

render_sidebar()

# import streamlit as st
# import sqlite3
# import pandas as pd
# import plotly.express as px

# ----------------------------
# Page config
# ----------------------------


st.markdown(
    """
    <div class="dashboard-card">
        <div class="section-title">🎯 Job Seeker Insights</div>
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Database connection
# ----------------------------
conn = sqlite3.connect("sql.db")

df = pd.read_sql(
    "SELECT * FROM job_placement",    

    conn)
job_switch_df=pd.read_sql(
    "SELECT * FROM job_switch_data",
    conn)
salary_df=pd.read_sql(
    "SELECT * FROM salary_hike_experience",
    conn)
   
   


conn.close()

# ----------------------------
# Filters (TOP, not sidebar)
# ----------------------------
col1, col2 ,col3= st.columns(3)

with col1:
    work_type_filter = st.multiselect(
        "Select Work Type",
        options=df["work_type"].unique(),
        default=df["work_type"].unique()
    )

with col2:
    status_filter = st.selectbox(
        "Placement Status",
        options=["Placed", "Not Placed"],
        index=0
    )
with col3:
    salary_filter = st.multiselect(
        "Salary Band",
        options=df["salary_band"].unique(),
        default=df["salary_band"].unique()
    )    

# ----------------------------
# Apply filters
# ----------------------------
filtered_df = df[
    (df["work_type"].isin(work_type_filter)) &
    (df["status"] == status_filter) &
    (df["salary_band"].isin(salary_filter))
]
if status_filter == "Not Placed":
    st.info(
        "Work type distribution is shown only for placed candidates. "
        "Not placed candidates represent job seekers."
    )



# ----------------------------
# KPI row
# ----------------------------
k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Candidates", len(filtered_df))

if status_filter == "Placed":
    k2.metric("Hybrid Jobs", (filtered_df["work_type"] == "Hybrid").sum())
    k3.metric("Remote Jobs", (filtered_df["work_type"] == "Remote").sum())
    k4.metric("Offline Jobs", (filtered_df["work_type"] == "Offline").sum())
else:
    k2.metric("Job Seekers", len(filtered_df))
    k3.metric("—", "")
    k4.metric("—", "")



st.divider()

# ----------------------------
# Work Type Graph (SLIM & CLEAN)
# ----------------------------
# ----------------------------
# Work Type Graph (SLIM & CLEAN)
# ----------------------------
# Job Opportunities by Work Type (Placed Only)
# =========================================================
def apply_professional_style(fig, y_title):
    fig.update_traces(
        marker_color="#8b5cf6",   # purple
        width=0.12,
        textposition="outside",
        textfont=dict(size=12)
    )

    fig.update_layout(
        plot_bgcolor="#0f172a",
        paper_bgcolor="#0f172a",
        font_color="#e5e7eb",
        title_font=dict(size=18, color="#e5e7eb"),
        height=420,
        bargap=0.75,
        title_x=0.3,
        xaxis_title=None,
        yaxis_title=y_title,
        margin=dict(l=40, r=40, t=60, b=40)
    )

    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.08)",
        zeroline=False
    )

    fig.update_xaxes(
        gridcolor="rgba(255,255,255,0.05)",
        type="category"
    )

    return fig

# ----------------------------
# Job Opportunities by Work Type
# ----------------------------
if status_filter == "Placed":

    work_counts = filtered_df["work_type"].value_counts().reset_index()
    work_counts.columns = ["Work Type", "Count"]

    fig = px.bar(
        work_counts,
        x="Work Type",
        y="Count",
        text="Count",
        title="Job Opportunities by Work Type"
    )

    fig = apply_professional_style(
        fig,
        y_title="Number of Candidates"
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Work type distribution is available only for placed candidates.")


# Salary Growth by Work Type

if status_filter == "Placed":

    hike_df = filtered_df[
        (filtered_df["work_experience"] == "Yes") &
        (filtered_df["expected_hike_percent"] > 0)
    ]

    if not hike_df.empty:

        growth_by_work = (
            hike_df.groupby("work_type")["expected_hike_percent"]
            .mean()
            .reset_index()
        )

        fig_growth = px.bar(
            growth_by_work,
            x="work_type",
            y="expected_hike_percent",
            text=growth_by_work["expected_hike_percent"].round(1).astype(str) + "%",
            title="Average Salary Growth by Work Type (Experienced Candidates)"
        )

        fig_growth = apply_professional_style(
            fig_growth,
            y_title="Average Expected Salary Growth (%)"
        )

        st.plotly_chart(fig_growth, use_container_width=True)

    else:
        st.info("No experienced candidates available for salary growth analysis.")

# Job Switcher Section (STABLE)

st.divider()
st.subheader("ℹ️Job Switch success rate")

js_col1, js_col2 = st.columns(2)

with js_col1:
    st.multiselect(
        "Previous Role (reference only)",
        options=job_switch_df["previous_role"].unique(),
        default=job_switch_df["previous_role"].unique()
    )

with js_col2:
    exp_filter = st.multiselect(
        "Experience Bucket",
        options=job_switch_df["experience_bucket"].unique(),
        default=job_switch_df["experience_bucket"].unique()
    )

# ---- Aggregate FIRST ----
success_by_exp = (
    job_switch_df
    .groupby("experience_bucket")["job_switch_success_rate"]
    .mean()
    .reset_index()
)

# ---- Apply experience filter only ----
success_by_exp = success_by_exp[
    success_by_exp["experience_bucket"].isin(exp_filter)
]

# ----------------------------
# Graph
# ----------------------------
fig_switch = px.bar(
    success_by_exp,
    x="experience_bucket",
    y="job_switch_success_rate",
    text=success_by_exp["job_switch_success_rate"].round(1),
    title="Job Switch Success Rate by Experience Level"
)

fig_switch = apply_professional_style(
    fig_switch,
    y_title="Average Job Switch Success Rate (%)"
)

st.plotly_chart(fig_switch, use_container_width=True)
st.caption(
    "Mid-level professional from 2 to 5 years show the higest job switch succes rate while seniors have selective option"


)

# Salary Hike Distribution (Experienced Employees)
# =========================================================

st.divider()
st.subheader(" Salary Hike Distribution (Experienced Employees)")

# ----------------------------
# Safety check
# ----------------------------
if salary_df.empty:
    st.error("salary_hike_experienced table is empty.")
    st.stop()

# ----------------------------
# Filters (INDEPENDENT)
# ----------------------------
f1, f2 = st.columns(2)

with f1:
    exp_filter = st.multiselect(
        "Experience Level",
        options=salary_df["Experience_Bucket"].unique(),
        default=salary_df["Experience_Bucket"].unique(),
        key="salary_exp"
    )

with f2:
    skill_filter = st.multiselect(
        "Skill Level",
        options=salary_df["Skill_Level"].unique(),
        default=salary_df["Skill_Level"].unique(),
        key="salary_skill"
    )

# ----------------------------
# Apply filters
# ----------------------------
filtered_salary = salary_df[
    (salary_df["Experience_Bucket"].isin(exp_filter)) &
    (salary_df["Skill_Level"].isin(skill_filter))
].copy()

if filtered_salary.empty:
    st.warning("No data for selected filters.")
    st.stop()

# ----------------------------
# Create hike ranges
# ----------------------------
filtered_salary["Hike_Range"] = pd.cut(
    filtered_salary["Salary_Hike_Percent"],
    bins=[0, 10, 20, 30, 40, 100],
    labels=["0–10%", "10–20%", "20–30%", "30–40%", "40%+"],
    include_lowest=True
)

# ----------------------------
# Aggregate
# ----------------------------
stack_df = (
    filtered_salary
    .groupby(["Experience_Bucket", "Hike_Range"])
    .size()
    .reset_index(name="Employee_Count")
)

# ----------------------------
# Stacked bar chart
# ----------------------------
fig_stack = px.bar(
    stack_df,
    x="Experience_Bucket",
    y="Employee_Count",
    color="Hike_Range",
    title="Salary Hike Distribution by Experience Level",
    color_discrete_sequence=[
        "#6366f1", "#8b5cf6", "#a78bfa", "#c4b5fd", "#ddd6fe"
    ]
)
fig_stack.update_layout(
    legend=dict(
        title=dict(
            text="Expected Salary Hike (%)",
            font=dict(size=13, color="#e5e7eb")
        ),
        font=dict(size=12, color="#e5e7eb"),
        orientation="v",
        x=1.02,          # push legend further right its done beacue for some reason text was not visible
        y=1,
        xanchor="left",
        yanchor="top",
        itemsizing="constant"  
    ),
    margin=dict(
        l=40,
        r=160,   
        b=40
    )
)

# ----------------------------
# Styling (SLIM & STABLE)
# ----------------------------
fig_stack.update_traces(width=0.4)

fig_stack.update_layout(
    plot_bgcolor="#0f172a",
    paper_bgcolor="#0f172a",
    font_color="#e5e7eb",
    height=360,              
    barmode="stack",
    bargap=0.45,
    bargroupgap=0.2,
    title_x=0.25,
    xaxis_title="Experience Level",
    yaxis_title="Number of Employees",
    legend_title="Expected Salary Hike (%)",
    margin=dict(l=40, r=40, t=60, b=40)
)

fig_stack.update_yaxes(
    gridcolor="rgba(255,255,255,0.08)",
    zeroline=False
)

# 🔑 Prevent single-bar stretching
n = stack_df["Experience_Bucket"].nunique()
fig_stack.update_xaxes(
    gridcolor="rgba(255,255,255,0.05)",
    type="category",
    range=[-0.5, max(1.5, n - 0.5)]
)

st.plotly_chart(fig_stack, use_container_width=True)

st.caption(
    "Employees with 2–5 years of experience dominate mid-range salary hikes, "
    "while higher experience levels show more selective growth."
)


st.markdown(
    "<h3 style='color:#93c5fd;'>Strategic Career Intelligence</h3>",
    unsafe_allow_html=True
)


companies = {
    "Apple (AAPL)": "AAPL",
    "Microsoft (MSFT)": "MSFT",
    "Exxon Mobil (XOM)": "XOM",
    "Mastercard (MA)": "MA",
    "Citi Bank (C)": "C",
    "Google (GOOGL)": "GOOGL",
    "Amazon (AMZN)": "AMZN",
    "Tesla (TSLA)": "TSLA",
    "Meta (META)": "META",
    "Nvidia (NVDA)": "NVDA",
    "Reliance (RELIANCE.NS)": "RELIANCE.NS",
    "TCS (TCS.NS)": "TCS.NS",
    "HDFC Bank (HDFCBANK.NS)": "HDFCBANK.NS"
}

selected_company = st.selectbox("Select Company", list(companies.keys()))
ticker_symbol = companies[selected_company]
ticker = yf.Ticker(ticker_symbol)
info = ticker.info

sector = info.get("sector", "N/A")
market_cap = info.get("marketCap", 0)



def get_job_roles_by_sector(sector):
    if sector == "Financial Services":
        return [
            "Investment Banking Analyst",
            "Risk & Compliance Officer",
            "Credit Risk Analyst",
            "Financial Data Analyst",
            "Treasury Operations Executive"
        ]
    elif sector == "Technology":
        return [
            "Data Scientist (AI/ML)",
            "Cloud Infrastructure Engineer",
            "Product Analyst",
            "Cybersecurity Specialist",
            "Software Development Engineer"
        ]
    elif sector == "Energy":
        return [
            "Energy Market Analyst",
            "Operations Engineer",
            "Supply Chain Analyst",
            "Sustainability Analyst",
            "Project Planning Manager"
        ]
    else:
        return [
            "Business Analyst",
            "Operations Analyst",
            "Strategy Associate",
            "Management Trainee",
            "Corporate Finance Executive"
        ]



job_roles = get_job_roles_by_sector(sector)



st.markdown("###  Recommended Job Opportunities")

if job_roles:
    for job in job_roles:
        st.markdown(f"""
        <div style="
            background:#111827;
            padding:18px;
            border-radius:12px;
            border:1px solid rgba(59,130,246,0.25);
            margin-bottom:12px;
            box-shadow:0 0 15px
            rgba(59,130,246,0.25);
                    color:#ffffff;
                    font-weight:600;
                    font-size:16px;">

        
             {job}
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No job recommendations available.")



insight = ""

if market_cap and market_cap > 500_000_000_000:
    insight += "• Large Cap Company – Offers stable long-term career growth.\n"

if "Technology" in sector:
    insight += "• Strong tech focus – High demand for AI and Cloud roles.\n"

if "Financial" in sector:
    insight += "• Financial services sector – Stable but competitive roles.\n"

if insight:
    st.success(insight)
else:
    st.info("Career insights not available.")  

st.markdown("""
<div style="
    background:rgba(34,197,94,0.08);
    padding:16px;
    border-radius:12px;
    border:1px solid rgba(34,197,94,0.35);
    margin-top:10px;
    color:#166534;
    font-size:14px;
    line-height:1.6;
">
    
<b> Career Stability Insight</b><br><br>
The above roles involve strategic decision-making, regulatory oversight,
operational control, and domain expertise. Such functions are generally
more resilient in an AI-driven economy compared to repetitive tasks.

</div>
""", unsafe_allow_html=True)      