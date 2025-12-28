# pages/Admin_Tools.py
import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import gspread
from google.oauth2.service_account import Credentials
from utils.gsheet_loader import connect_to_sheet

st.set_page_config(page_title="Admin Tools", layout="wide", page_icon="🛠️")

st.title("🛠️ Admin & Developer Tools")

# --- 1. SIMPLE AUTHENTICATION (Placeholder) ---
# Later, we will replace this with real user accounts.
admin_password = st.sidebar.text_input("Enter Admin Password", type="password")

if admin_password != "admin123":  # You can change this password
    st.info("🔒 This area is restricted to System Administrators.")
    st.stop()

st.sidebar.success("✅ Admin Access Granted")

# --- 2. TABS FOR TOOLS ---
tab1, tab2, tab3 = st.tabs(["🔌 Connection Test", "⚡ Data Generator", "🗑️ Wipe Data"])

# ==========================================
# TAB 1: CONNECTION TESTER
# ==========================================
with tab1:
    st.header("Google Sheet Connection Test")
    if st.button("Run Diagnostics"):
        try:
            # Check Secrets
            if "gcp_service_account" not in st.secrets:
                st.error("❌ No Secrets found!")
            else:
                st.success("✅ Secrets found in environment.")
                
            # Connect
            sheet = connect_to_sheet()
            if sheet:
                st.success(f"✅ Successfully connected to Sheet: '{sheet.title}'")
                st.info(f"Current Row Count: {len(sheet.get_all_values())}")
            else:
                st.error("❌ Connection returned None.")
                
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ==========================================
# TAB 2: DUMMY DATA GENERATOR
# ==========================================
with tab2:
    st.header("Generate Dummy Data")
    st.warning("⚠️ This will append random data to your live Google Sheet.")
    
    # Input for how many rows
    num_rows = st.number_input("Number of rows to generate", min_value=1, max_value=50, value=10)
    
    if st.button(f"🚀 Generate {num_rows} Rows"):
        sheet = connect_to_sheet()
        if sheet:
            # Configuration
            aircraft_list = ["9N-AHB", "9N-AHC", "9N-AHD", "9N-AHE"]
            components = [
                {"code": "C001", "name": "Fuel Pump", "ata": "28", "mean_fh": 1200},
                {"code": "C002", "name": "Hydraulic Pump", "ata": "29", "mean_fh": 2500},
                {"code": "C003", "name": "Starter Generator", "ata": "24", "mean_fh": 800},
                {"code": "C004", "name": "Altimeter", "ata": "34", "mean_fh": 5000},
                {"code": "C005", "name": "Main Wheel Assembly", "ata": "32", "mean_fh": 400},
            ]
            reasons = ["Leaking", "Vibration high", "Internal short", "Bearing noise", "Fluctuating output", "Hard landing check"]
            
            dummy_rows = []
            
            with st.spinner("Simulating maintenance history..."):
                for _ in range(int(num_rows)):
                    comp = random.choice(components)
                    ac = random.choice(aircraft_list)
                    
                    # 15% chance of anomaly (early failure)
                    is_anomaly = random.random() < 0.15 
                    if is_anomaly:
                        fh = random.randint(50, int(comp["mean_fh"] * 0.3)) 
                    else:
                        fh = random.randint(int(comp["mean_fh"] * 0.8), int(comp["mean_fh"] * 1.2))
                    
                    fc = int(fh / 0.8)
                    days_ago = random.randint(0, 365)
                    event_date = (datetime.today() - timedelta(days=days_ago)).strftime("%Y-%m-%d")

                    row = [
                        ac, comp["code"], comp["name"], 
                        f"PN-{random.randint(1000,9999)}", 
                        f"SN-{random.randint(10000,99999)}", 
                        comp["ata"], event_date, fh, fc, 
                        "Unscheduled", random.choice(reasons)
                    ]
                    dummy_rows.append(row)

                try:
                    sheet.append_rows(dummy_rows)
                    st.success(f"✅ Successfully added {len(dummy_rows)} rows!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Error uploading: {e}")

# ==========================================
# TAB 3: DANGER ZONE (Wipe Data)
# ==========================================
with tab3:
    st.header("Danger Zone")
    st.markdown("Use this to clear all test data before going live.")
    
    if st.button("⚠️ DELETE ALL DATA (Keep Headers)"):
        confirm = st.checkbox("I am sure I want to delete all data rows.")
        if confirm:
            sheet = connect_to_sheet()
            if sheet:
                # Clear rows starting from row 2 (keeping headers)
                # Note: 'resize' or 'clear' methods vary, simplistic approach:
                all_values = sheet.get_all_values()
                if len(all_values) > 1:
                    sheet.batch_clear([f"A2:L{len(all_values)}"])
                    st.warning("All data rows cleared.")
                else:
                    st.info("Sheet is already empty.")
