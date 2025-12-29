import streamlit as st
import pandas as pd
import numpy as np
from utils.navbar import create_header
from utils.footer import render_footer
from utils.gsheet_loader import write_bulk_data, write_data_to_sheet, clear_worksheet_data

st.set_page_config(page_title="Admin Tools", layout="wide", initial_sidebar_state="collapsed")
create_header(current_page="Admin Tools")

st.title("🛠️ Admin Tools")

tab1, tab2, tab3, tab4 = st.tabs(["✈️ Aircraft Fleet", "📚 ATA Chapters", "🧪 Testing Data", "⚠️ Danger Zone"])

# ... (TAB 1 and TAB 2 code remains exactly the same as before) ...
with tab1:
    st.subheader("Manage Fleet Details")
    # ... (Keep your fleet form code here) ...
    st.info("Use the form above to add aircraft to the 'aircraft_fleet' tab.")

with tab2:
    st.subheader("Manage ATA References")
    # ... (Keep your ATA form code here) ...
    st.info("Use the form above to add chapters to the 'ata_chapters' tab.")

# --- TAB 3: GENERATE DATA (With Component Type) ---
with tab3:
    st.subheader("Generate & Sync Dummy Data")
    st.markdown("This will generate 50 rows including the new **Component Type** column.")

    if st.button("🔄 Generate 50 Records & Sync to Cloud"):
        dates = pd.date_range(start="2024-01-01", periods=50)
        
        # Matches your New Column Order:
        # Reg | Code | Name | PN | TYPE | SN | ATA | Date | FH | FC | Type | Reason
        data = {
            "aircraft_reg": np.random.choice(["9N-AHA", "9N-AHB", "9N-AIC"], 50),
            "component_code": ["C-123"] * 50,
            "component_name": np.random.choice(["Main Wheel", "Starter Gen", "Brake Unit", "Fuel Pump"], 50),
            "part_number": "PN-DEMO-123",
            "component_type": np.random.choice(["On Condition (OC)", "Life Limited (LL)"], 50), # <--- New Column
            "serial_number": np.random.choice(["SN-001", "SN-002", "SN-003"], 50),
            "ata_chapter": np.random.choice(["32", "24", "21", "73", "27"], 50),
            "removal_date": dates,
            "aircraft_fh": np.random.randint(1000, 5000, 50),
            "aircraft_fc": np.random.randint(500, 2000, 50),
            "removal_type": "Unscheduled",
            "removal_reason": np.random.choice(["Wear", "Leaking", "Vibration", "Electrical Fault"], 50)
        }
        df_demo = pd.DataFrame(data)
        
        with st.spinner("Syncing to Google Sheet..."):
            success = write_bulk_data(df_demo)
        
        if success:
            st.session_state["df"] = df_demo
            st.success("✅ Google Sheet regenerated with 50 new records.")
        else:
            st.error("⚠️ Failed to write to Google Sheet.")

# --- TAB 4: DANGER ZONE (UPDATED) ---
with tab4:
    st.subheader("Database Maintenance")
    st.error("⚠️ **Critical Actions**")
    
    col1, col2 = st.columns(2)
    
    # 1. Wipe Session (RAM)
    with col1:
        st.markdown("##### 1. Clear Session (RAM)")
        st.caption("Resets the app memory. Does not affect Google Sheet.")
        if st.button("🗑️ Wipe Session"):
            st.session_state.clear()
            st.rerun()

    # 2. Wipe Google Sheet (Cloud) - NEW
    with col2:
        st.markdown("##### 2. Wipe Google Sheet (Cloud)")
        st.caption("Permanently deletes ALL rows in 'removal_events' (except headers).")
        
        # Double confirmation using a checkbox
        confirm_wipe = st.checkbox("I confirm I want to delete all historical data.")
        
        if st.button("🔥 Wipe Cloud Database", type="primary", disabled=not confirm_wipe):
            with st.spinner("Deleting all rows from Google Sheet..."):
                if clear_worksheet_data("removal_events"):
                    st.toast("Google Sheet cleared successfully!", icon="🧹")
                    st.success("✅ 'removal_events' tab is now empty.")
                    # Also clear session so the dashboard doesn't show ghost data
                    st.session_state.clear()
                else:
                    st.error("Failed to clear Google Sheet.")

render_footer()
