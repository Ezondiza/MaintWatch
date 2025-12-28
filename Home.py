# /Home.py
import streamlit as st
from streamlit_option_menu import option_menu
from utils.data_loader import load_data 

# 1. Page Configuration (Collapse sidebar to hide default nav)
st.set_page_config(
    page_title="MaintWatch", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. Horizontal Navigation Menu
# This replaces the sidebar. You place this at the top of every page, 
# or use a multi-page app structure where Home directs traffic.
selected = option_menu(
    menu_title=None,  # Required to hide the menu title
    options=["Home", "Dashboard", "Data Entry", "Settings"],  # Your pages
    icons=["house", "speedometer2", "pencil-square", "gear"], 
    menu_icon="cast", 
    default_index=0, 
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#f0f2f6"},
        "icon": {"color": "orange", "font-size": "25px"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#004080"},
    }
)

# 3. Logic to handle navigation (if keeping everything in one file for now)
# Ideally, in a multipage app, this menu just helps user visualize, 
# but Streamlit handles pages via the /pages folder. 
# For now, let's treat this strictly as the Landing Page view:

st.title("🛠️ Maintenance Watch")
st.markdown("#### Component Reliability & MTBF Tracking System")
st.divider()

# 4. Critical Information / Executive Summary
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(
        """
        **Welcome to MaintWatch.**
        
        This platform supports aircraft maintenance reliability analysis using component removal history.
        It provides real-time insights into fleet health and component performance.

        **Core Capabilities:**
        * **📉 Reliability Analysis:** Track Mean Time Between Failures (MTBF).
        * **⚠️ Alerting:** Identify components exceeding failure thresholds.
        * **✈️ Fleet Spares:** Support maintenance planning and forecasting.
        """
    )

with col2:
    # A placeholder for a "System Status" or "Quick Stat"
    st.info(
        """
        **System Status**
        
        * **Database:** Connected
        * **Last Update:** Today, 14:00
        * **Active User:** CEO-LAPTOP
        """
    )

# 5. Call to Action (Guiding the user)
st.divider()
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("➕ New Component Removal"):
        st.switch_page("pages/1_Data_Entry.py") # Assuming you have this page
with c2:
    if st.button("📊 View MTBF Dashboard"):
        st.switch_page("pages/2_Dashboard.py") # Assuming you have this page
with c3:
    if st.button("⚙️ Data Settings"):
        st.switch_page("pages/Settings.py") # Move the CSV upload/Migrate here

# 6. Professional Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: grey; font-size: small;'>
    MaintWatch v1.0 | Developed by Ghanshyam Acharya | © 2025 Sita Air<br>
    <i>Unauthorized access is prohibited.</i>
    </div>
    """,
    unsafe_allow_html=True
)
