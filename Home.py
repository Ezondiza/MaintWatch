# /Home.py
import streamlit as st
from utils.navbar import create_header

# 1. Page Config (Must be the very first command in the script)
st.set_page_config(
    page_title="MaintWatch", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. Render Navbar
create_header(current_page="Home")

# 3. Main Landing Content
st.title("🛠️ Maintenance Watch")
st.subheader("Component Reliability and MTBF Tracking")
st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(
        """
        **Welcome to MaintWatch.**
        
        MaintWatch supports aircraft maintenance reliability analysis using component removal history.
        
        **Core Modules:**
        * **📊 Dashboard:** Analyze Mean Time Between Failures (MTBF) and fleet trends.
        * **📝 Data Upload:** Bulk import historical CSV data for backfilling.
        * **🛠️ Admin Tools:** Manage aircraft fleet details and ATA chapters.
        """
    )

with col2:
    st.info(
        """
        **System Status**
        * **Database:** Connected
        * **User:** CEO-LAPTOP
        * **Version:** v1.0.3
        """
    )

# 4. Quick Action Buttons
st.markdown("### Quick Actions")
c1, c2, c3 = st.columns(3)

with c1:
    # Links to the Daily Entry page (hidden from top menu, but accessible here)
    if st.button("➕ New Removal Event", use_container_width=True):
        st.switch_page("pages/Component_Removal.py")

with c2:
    # Links to the Dashboard
    if st.button("📈 View Reliability", use_container_width=True):
        st.switch_page("pages/MTBF_Dashboard.py")

with c3:
    # Links to the Data Upload page
    if st.button("📥 Upload History", use_container_width=True):
        st.switch_page("pages/Data_Upload.py")

# 5. Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: grey;'>MaintWatch © 2025 | Developed by Ghanshyam Acharya</div>", 
    unsafe_allow_html=True
)
