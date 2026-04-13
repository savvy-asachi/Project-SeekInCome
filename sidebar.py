import streamlit as st



def render_sidebar():
    with st.sidebar:
        st.image("assets/seekincome.svg", use_container_width=True)
        st.markdown("---")

        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("pages/0_Home.py")

        if st.button("👤 Job Seeker", use_container_width=True):
            st.switch_page("pages/1_Job_Seeker.py")

        if st.button("🏢 Company", use_container_width=True):
            st.switch_page("pages/2_Company.py")

        if st.button("💼 Investor", use_container_width=True):
            st.switch_page("pages/3_Investor.py")