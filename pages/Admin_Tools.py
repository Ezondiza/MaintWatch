import streamlit as st
import pandas as pd
import numpy as np
from utils.navbar import create_header
from utils.footer import render_footer

st.set_page_config(page_title="Admin Tools", layout="wide", initial_sidebar_state="collapsed")
create_header(current_page="Admin Tools")

st.title("🛠️ Admin Tools")
st.markdown("System configuration, fleet management, and testing utilities.")

# Create Tabs
tab1, tab2, tab3, tab4 = st.tabs(["✈️ Aircraft Fleet", "📚 ATA Chapters", "🧪 Testing Data", "⚠️ Danger Zone"])

# --- TAB 1: AIRCRAFT ---
with tab1:
    st.subheader("Manage Fleet Details")
    st.info("Feature coming soon: Add/Edit Aircraft Registrations and MSN.")

# --- TAB 2: ATA ---
with tab2:
    st.subheader("Manage ATA Chapter References")
    st.info("Feature coming soon: Add/Edit ATA Chapter descriptions.")

# --- TAB 3: DUMMY DATA GENERATOR (New) ---
with tab3:
    st.subheader("Generate Dummy Data for Testing")
    st.markdown("Use this tool to populate the dashboard with random data to verify charts and KPIs.")
    
    if st.button("🔄 Generate 50 Random Records"):
        # Create random data
        dates = pd.date_range(start="2024-01-01", periods=50)
        data = {
            "Date": dates,
            "Aircraft": np.random.choice(["9N-AHA", "9N-AHB", "9N-AIC", "9N-XYZ"], 50),
            "ATA": np.random.choice(["32", "24", "21", "73", "27", "29"], 50),
            "Component": np.random.choice(["Main Wheel", "Starter Gen", "Brake Unit", "Fuel Pump", "Altimter"], 50),
            "Reason": np.random.choice(["Wear", "Leaking", "Vibration", "Electrical Fault", "Cracked"], 50),
            "Part Number": "PN-DEMO-123",
            "Serial Number Off": "SN-999",
            "Serial Number On": "SN-888",
            "Technician": "Test User",
            "Pilot": "Test Pilot"
        }
        df_demo = pd.DataFrame(data)
        
        # Load into Session State
        st.session_state["df"] = df_demo
        st.success(f"✅ Generated {len(df_demo)} records. Go to 'Dashboard' to view them.")
        st.dataframe(df_demo.head())

# --- TAB 4: DANGER ZONE ---
with tab4:
    st.subheader("Database Maintenance")
    st.error("⚠️ **Critical Actions**")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Wipe All Data", type="primary"):
            st.session_state.clear()
            st.toast("System memory cleared!", icon="🧹")
            st.rerun()

# Footer
render_footer()
