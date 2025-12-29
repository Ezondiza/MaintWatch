import streamlit as st
import pandas as pd
import numpy as np
from utils.navbar import create_header
from utils.footer import render_footer
from utils.gsheet_loader import write_bulk_data, write_data_to_sheet, clear_worksheet_data, fetch_all_data

# 1. Page Config
st.set_page_config(page_title="Admin Tools", layout="wide", initial_sidebar_state="collapsed")
create_header(current_page="Admin Tools")

st.title("🛠️ Admin Tools")
st.markdown("System configuration, fleet management, and testing utilities.")

# Create Tabs
tab1, tab2, tab3, tab4 = st.tabs(["✈️ Aircraft Fleet", "📚 ATA Chapters", "🧪 Testing Data", "⚠️ Danger Zone"])

# --- TAB 1: AIRCRAFT FLEET CONFIGURATION ---
with tab1:
    st.subheader("Manage Fleet Details")
    
    col_form, col_view = st.columns([1, 1])
    
    # LEFT: Input Form
    with col_form:
        st.markdown("##### Add New Aircraft")
        with st.form("fleet_form", clear_on_submit=True):
            reg = st.text_input("Aircraft Registration", placeholder="e.g., 9N-AHA")
            msn = st.text_input("Manufacturer Serial No. (MSN)", placeholder="e.g., 12345")
            fh = st.number_input("Current Flight Hours (FH)", min_value=0.0, step=0.1)
            fc = st.number_input("Current Flight Cycles (FC)", min_value=0, step=1)
            
            if st.form_submit_button("💾 Save Aircraft"):
                if reg and msn:
                    data = {"Registration": reg, "MSN": msn, "FH": fh, "FC": fc}
                    with st.spinner("Saving to Google Sheet..."):
                        if write_data_to_sheet(data, "aircraft_fleet"):
                            st.success(f"✅ {reg} added!")
                            st.rerun() # Refresh to show new data in table
                else:
                    st.error("⚠️ Registration and MSN are required.")

    # RIGHT: Live View of Google Sheet
    with col_view:
        st.markdown("##### Current Fleet List (Live from Cloud)")
        df_fleet = fetch_all_data("aircraft_fleet")
        if not df_fleet.empty:
            st.dataframe(df_fleet, use_container_width=True)
        else:
            st.info("No aircraft found in database.")

# --- TAB 2: ATA CHAPTERS CONFIGURATION ---
with tab2:
    st.subheader("Manage ATA References")
    
    col_form, col_view = st.columns([1, 1])
    
    # LEFT: Input Form
    with col_form:
        st.markdown("##### Add ATA Chapter")
        with st.form("ata_form", clear_on_submit=True):
            ata_code = st.text_input("ATA Chapter Code", placeholder="e.g., 32")
            ata_desc = st.text_input("Description", placeholder="e.g., Landing Gear")
            
            if st.form_submit_button("💾 Save ATA Chapter"):
                if ata_code and ata_desc:
                    data = {"Chapter": ata_code, "Description": ata_desc}
                    with st.spinner("Saving to Google Sheet..."):
                        if write_data_to_sheet(data, "ata_chapters"):
                            st.success(f"✅ ATA {ata_code} added!")
                            st.rerun() # Refresh to show new data
                else:
                    st.error("⚠️ Code and Description required.")

    # RIGHT: Live View
    with col_view:
        st.markdown("##### Current ATA List (Live from Cloud)")
        df_ata = fetch_all_data("ata_chapters")
        if not df_ata.empty:
            st.dataframe(df_ata, use_container_width=True)
        else:
            st.info("No ATA chapters found.")

# --- TAB 3: DUMMY DATA GENERATOR (SMART VERSION) ---
with tab3:
    st.subheader("Generate & Sync Dummy Data")
    st.markdown("Generate 50 realistic rows where **Flight Hours increase over time**.")

    if st.button("🔄 Generate 50 Smart Records"):
        dates = pd.date_range(start="2024-01-01", periods=50)
        
        # 1. Create Base Arrays
        data = []
        
        # We need to track the "Current FH" for each aircraft so it increases logically
        # Starting FH for each plane
        current_fh = {"9N-AHA": 1200, "9N-AHB": 2500, "9N-AIC": 5000}
        current_fc = {"9N-AHA": 600,  "9N-AHB": 1100, "9N-AIC": 2200}

        for d in dates:
            # Pick a random aircraft
            ac = np.random.choice(["9N-AHA", "9N-AHB", "9N-AIC"])
            
            # Simulate that the plane flew 4-8 hours since the last entry
            flight_time = np.random.randint(4, 9) 
            cycles = np.random.randint(1, 4)
            
            # Update the counters
            current_fh[ac] += flight_time
            current_fc[ac] += cycles
            
            # Build the row
            row = {
                "aircraft_reg": ac,
                "component_code": "C-123",
                "component_name": np.random.choice(["Main Wheel", "Starter Gen", "Brake Unit", "Fuel Pump"], p=[0.4, 0.2, 0.2, 0.2]),
                "part_number": "PN-DEMO-123",
                "component_type": np.random.choice(["On Condition (OC)", "Life Limited (LL)"]),
                "serial_number": f"SN-{np.random.randint(100,999)}",
                "ata_chapter": np.random.choice(["32", "24", "21", "73", "27"]),
                "removal_date": d,
                "aircraft_fh": current_fh[ac], # Uses the increasing number
                "aircraft_fc": current_fc[ac],
                "removal_type": "Unscheduled",
                "removal_reason": np.random.choice(["Wear", "Leaking", "Vibration", "Electrical Fault"])
            }
            data.append(row)

        df_demo = pd.DataFrame(data)
        
        with st.spinner("Syncing to Google Sheet..."):
            success = write_bulk_data(df_demo)
        
        if success:
            st.session_state["df"] = df_demo
            st.success("✅ Smart Data Generated! Go to Dashboard to see correct MTBF.")
        else:
            st.error("⚠️ Failed to write to Google Sheet.")
# --- TAB 4: DANGER ZONE ---
with tab4:
    st.subheader("Database Maintenance")
    st.error("⚠️ **Critical Actions**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 1. Clear Session")
        if st.button("🗑️ Wipe RAM"):
            st.session_state.clear()
            st.rerun()

    with col2:
        st.markdown("##### 2. Wipe Historical Data")
        st.caption("Clears 'removal_events' tab only. Keeps Fleet/ATA data safe.")
        
        confirm_wipe = st.checkbox("I confirm I want to delete historical removal data.")
        
        if st.button("🔥 Wipe Removal Events", type="primary", disabled=not confirm_wipe):
            with st.spinner("Wiping 'removal_events'..."):
                if clear_worksheet_data("removal_events"):
                    st.toast("History cleared!", icon="🧹")
                    st.success("✅ 'removal_events' tab cleared.")
                    st.session_state.clear()

render_footer()
