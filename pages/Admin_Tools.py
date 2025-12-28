import streamlit as st
import pandas as pd
import numpy as np
from utils.navbar import create_header
from utils.footer import render_footer
# IMPORT THE FUNCTION FROM YOUR EXISTING LOADER
from utils.gsheet_loader import write_bulk_data 

st.set_page_config(page_title="Admin Tools", layout="wide", initial_sidebar_state="collapsed")
create_header(current_page="Admin Tools")

st.title("🛠️ Admin Tools")

# Create Tabs
tab1, tab2, tab3, tab4 = st.tabs(["✈️ Aircraft Fleet", "📚 ATA Chapters", "🧪 Testing Data", "⚠️ Danger Zone"])

# ... (Tabs 1 & 2 omitted for brevity) ...

# --- TAB 3: DUMMY DATA GENERATOR ---
with tab3:
    st.subheader("Generate & Sync Dummy Data")
    st.markdown("Generate random data and **write it directly** to the connected Google Sheet.")
    
    if st.button("🔄 Generate 50 Records & Sync to Cloud"):
        # 1. Generate Data (RAM)
        # Note: I matched these column names to be closer to what your other script expects
        dates = pd.date_range(start="2024-01-01", periods=50)
        data = {
            "aircraft_reg": np.random.choice(["9N-AHA", "9N-AHB", "9N-AIC"], 50),
            "component_code": ["C-123"] * 50,
            "component_name": np.random.choice(["Main Wheel", "Starter Gen", "Brake Unit", "Fuel Pump"], 50),
            "part_number": "PN-DEMO-123",
            "serial_number": np.random.choice(["SN-001", "SN-002", "SN-003"], 50),
            "ata_chapter": np.random.choice(["32", "24", "21", "73", "27"], 50),
            "removal_date": dates,
            "aircraft_fh": np.random.randint(1000, 5000, 50),
            "aircraft_fc": np.random.randint(500, 2000, 50),
            "removal_type": "Unscheduled",
            "removal_reason": np.random.choice(["Wear", "Leaking", "Vibration", "Electrical Fault"], 50)
        }
        df_demo = pd.DataFrame(data)
        st.session_state["df"] = df_demo
        st.info(f"Generated {len(df_demo)} records in memory...")
        
        # 2. Write to Google Sheet (Cloud) using the UPGRADED loader
        with st.spinner("Syncing to Google Sheet..."):
            success = write_bulk_data(df_demo)
            
        if success:
            st.toast("Data successfully written to Google Sheet!", icon="☁️")
            st.success("✅ Google Sheet Updated successfully.")
        else:
            st.error("⚠️ Failed to write to Google Sheet. Check the error message above.")

# ... (Tab 4 and Footer) ...
