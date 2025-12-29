import streamlit as st
import pandas as pd
import numpy as np
from utils.navbar import create_header
from utils.footer import render_footer
from utils.gsheet_loader import write_bulk_data, write_data_to_sheet

st.set_page_config(page_title="Admin Tools", layout="wide", initial_sidebar_state="collapsed")
create_header(current_page="Admin Tools")

st.title("🛠️ Admin Tools")

# --- SECURITY GATE ---
# Simple password protection to prevent unauthorized access
# In a real production app, use st.secrets for the password.
# For now, let's hardcode a default password for testing: "admin123"

# check if we are already logged in via session state
if "admin_access" not in st.session_state:
    st.session_state["admin_access"] = False

if not st.session_state["admin_access"]:
    st.warning("🔒 Restricted Access: Administrator privileges required.")
    
    password = st.text_input("Enter Admin Password", type="password")
    
    if st.button("Login"):
        # YOU CAN CHANGE "admin123" TO WHATEVER PASSWORD YOU WANT
        if password == "admin123":
            st.session_state["admin_access"] = True
            st.success("Access Granted.")
            st.rerun()
        else:
            st.error("❌ Incorrect Password.")
    
    # Stop the script here if not logged in
    st.stop()

# =========================================================
# IF CODE REACHES HERE, THE USER IS LOGGED IN
# =========================================================

if st.button("🔒 Logout"):
    st.session_state["admin_access"] = False
    st.rerun()

st.markdown("System configuration, fleet management, and testing utilities.")

# Create Tabs
tab1, tab2, tab3, tab4 = st.tabs(["✈️ Aircraft Fleet", "📚 ATA Chapters", "🧪 Testing Data", "⚠️ Danger Zone"])

# --- TAB 1: AIRCRAFT FLEET ---
with tab1:
    st.subheader("Manage Fleet Details")
    st.markdown("Add new aircraft to the fleet database.")
    
    with st.form("fleet_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            reg = st.text_input("Aircraft Registration", placeholder="e.g., 9N-AHA")
            msn = st.text_input("Manufacturer Serial No. (MSN)", placeholder="e.g., 12345")
        with col2:
            fh = st.number_input("Current Flight Hours (FH)", min_value=0.0, step=0.1)
            fc = st.number_input("Current Flight Cycles (FC)", min_value=0, step=1)
            
        submitted_fleet = st.form_submit_button("💾 Save Aircraft")
        
        if submitted_fleet:
            if reg and msn:
                data = {"Registration": reg, "MSN": msn, "FH": fh, "FC": fc}
                with st.spinner("Saving to Google Sheet..."):
                    if write_data_to_sheet(data, "aircraft_fleet"):
                        st.success(f"✅ Aircraft {reg} added successfully!")
            else:
                st.error("⚠️ Registration and MSN are required.")

# --- TAB 2: ATA CHAPTERS ---
with tab2:
    st.subheader("Manage ATA References")
    
    with st.form("ata_form", clear_on_submit=True):
        col1, col2 = st.columns([1, 3])
        with col1:
            ata_code = st.text_input("ATA Chapter Code", placeholder="e.g., 32")
        with col2:
            ata_desc = st.text_input("Description", placeholder="e.g., Landing Gear")
            
        submitted_ata = st.form_submit_button("💾 Save ATA Chapter")
        
        if submitted_ata:
            if ata_code and ata_desc:
                data = {"Chapter": ata_code, "Description": ata_desc}
                with st.spinner("Saving to Google Sheet..."):
                    if write_data_to_sheet(data, "ata_chapters"):
                        st.success(f"✅ ATA {ata_code} added successfully!")
            else:
                st.error("⚠️ Both Code and Description are required.")

# --- TAB 3: DUMMY DATA ---
with tab3:
    st.subheader("Generate & Sync Dummy Data")
    
    if st.button("🔄 Generate 50 Records & Sync to Cloud"):
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
        
        with st.spinner("Syncing to Google Sheet..."):
            success = write_bulk_data(df_demo)
            
        if success:
            st.session_state["df"] = df_demo
            st.success("✅ Google Sheet Updated successfully.")
        else:
            st.error("⚠️ Failed to write to Google Sheet.")

# --- TAB 4: DANGER ZONE ---
with tab4:
    st.subheader("Database Maintenance")
    st.error("⚠️ **Critical Actions**")
    st.markdown("These actions affect the local session memory immediately.")

    with st.form("danger_zone_form"):
        st.warning("Are you sure you want to wipe the session data?")
        wipe_confirm = st.form_submit_button("🗑️ Yes, Wipe All Session Data", type="primary")
        
        if wipe_confirm:
            st.session_state.clear()
            st.success("System memory cleared! Please refresh the page.")
            st.rerun()

render_footer()
