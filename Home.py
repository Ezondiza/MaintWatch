import streamlit as st
from utils.navbar import create_header
from utils.footer import render_footer

# 1. Page Config
st.set_page_config(
    page_title="MaintWatch", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. Render Navbar
create_header(current_page="Home")

# 3. Main Content
st.title("🛠️ Maintenance Watch")
st.subheader("Component Reliability & MTBF Tracking")
st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(
        """
        ### Welcome to MaintWatch
        
        This platform supports aircraft maintenance reliability analysis.
        Use the **Navigation Bar** above to access all modules:
        
        * **➕ New Entry:** Record daily component removals.
        * **📊 Dashboard:** Analyze fleet reliability and trends.
        * **📥 Data Upload:** Import historical CSV data.
        * **🛠️ Admin Tools:** Configure fleet, system references, and **Generate Test Data**.
        """
    )

with col2:
    st.info(
        """
        **System Status**
        * **Database:** Connected
        * **User:** CEO-LAPTOP
        * **Version:** v1.1.0
        """
    )

# 4. Footer
render_footer()
