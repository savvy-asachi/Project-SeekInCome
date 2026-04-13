
# # st.title("TYIT Project Dashboard")
# # st.write("Streamlit app is working")
# # df=pd.read_excel("case2.xlsx")
# # st.write(df)
#here
import streamlit as st
import base64




from sidebar import render_sidebar
st.markdown("""
<style>
# section[data-testid="stSidebar"] nav {
#     display: none !important;
#     height: 0 !important;
# }
# [data-testid="stSidebarNav"] {
#     display: none !important;
#     height: 0 !important;
# }
            

          
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
         
</style>
""", unsafe_allow_html=True)







# ---------------- LOAD IMAGE ----------------
def load_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img_base64 = load_image("images/image1.png")

# ---------------- GLOBAL CSS ----------------
st.markdown(
    f"""
    <style>

    /* SIDEBAR STYLE */
    [data-testid="stSidebar"] {{
        background-color: white !important;
        border-right: 1px solid #e5e7eb;
    }}

    [data-testid="stSidebar"] * {{
        color: #111827 !important;
    }}

    /* REMOVE STREAMLIT WIDTH LIMIT */
    .block-container {{
        max-width: 100% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }}

    /* REMOVE PAGE OVERFLOW */
    html, body, .stApp {{
        margin: 0 !important;
        padding: 0 !important;
        overflow-x: hidden !important;
        background-color: #0b1220;
    }}

    /* FULL WIDTH BANNER */
    .top-banner {{
        width: 100%;
        height: 260px;
        background-image: url("data:image/png;base64,{img_base64}");
        background-size: cover;
        background-position: center;
    }}

    .title {{
        text-align: center;
        font-size: 48px;
        font-weight: 900;
        color: white !important;
        margin-top: 30px;
    }}

    .subtitle {{
        text-align: center;
        font-size: 18px;
        color: lightblue;
        margin-bottom: 20px;
    }}





    </style>
    """,
    unsafe_allow_html=True
)

render_sidebar()


# TOP BANNER
st.markdown("<div class='top-banner'></div>", unsafe_allow_html=True)

#  MAIN CONTENT 
st.markdown("<h1 class='title'>Business Dashboard</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>Choose your perspective to explore insights</p>",
    unsafe_allow_html=True
)

st.markdown(
    "<hr style='width:60%; margin: 0 auto 30px auto; border: 1px solid rgba(255,255,255,0.1);'>",
    unsafe_allow_html=True
)

#  BUTTON NAVIGATION 
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("👤 Job Seeker", use_container_width=True):
        st.switch_page("pages/1_job_Seeker.py")

with col2:
    if st.button("🏢 Company", use_container_width=True):
        st.switch_page("pages/2_Company.py")

with col3:
    if st.button("💼 Investor", use_container_width=True):
        st.switch_page("pages/3_Investor.py")


st.markdown("<br>",unsafe_allow_html=True)








st.markdown("""
<div style='text-align: center; color: #94a3b8; font-size: 14px;'>

© 2026 
<span style="font-weight:800;">
<span style="color:#1f77ff;">Seek</span><span style="color:#c9a227;">Income</span>
</span>
* Built with Streamlit • Made by <b>Tushar Kotian</b>

</div>
""", unsafe_allow_html=True)


