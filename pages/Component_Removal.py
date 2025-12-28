import streamlit as st
import pandas as pd
from datetime import date
from utils.navbar import create_header
from utils.data_loader import load_data
from utils.footer import render_footer

# 1. Page Config
st.set_page_config(page_title="New Removal", layout="wide", initial_sidebar_state="collapsed")

# 2. Render Navbar (Select 'New Entry')
create_header(current_page="New Entry")

st.title("➕ New Component Removal")
st.markdown("Record an unscheduled component removal event.")

# 3. Load Reference Data (Technicians, Pilots, Components)
try:
    components, technicians, pilots = load_data()
except Exception as e:
    # Fallback if files are missing
    st.warning("Could not load reference files. Using generic lists.")
    components = ["Main Wheel", "Brake Unit", "Starter Generator", "Fuel Pump"]
    technicians = ["Tech A", "Tech B"]
    pilots = ["Capt. X", "Capt. Y"]

# 4. THE FORM
with st.form("removal_entry_form"):
    st.subheader("Event Details")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        event_date = st.date_input("Date of Removal", value=date.today())
    with c2:
        aircraft_reg = st.text_input("Aircraft Registration", placeholder="e.g., 9N-AHA") 
    with c3:
        ata_chapter = st.text_input("ATA Chapter", placeholder="e.g., 32-40")

    st.subheader("Component Details")
    c4, c5 = st.columns(2)
    with c4:
        comp_name = st.selectbox("Component Name", options=components)
    with c5:
        part_number = st.text_input("Part Number (P/N)")

    c6, c7 = st.columns(2)
    with c6:
        serial_off = st.text_input("Serial Number OFF")
    with c7:
        serial_on = st.text_input("Serial Number ON")

    st.subheader("Maintenance Data")
    removal_reason = st.text_area("Reason for Removal / Defect Description")
    
    c8, c9 = st.columns(2)
    with c8:
        tech_name = st.selectbox("Technician", options=technicians)
    with c9:
        pilot_name = st.selectbox("Pilot Reporting", options=pilots)

    # 5. SUBMIT BUTTON
    submitted = st.form_submit_button("💾 Save Removal Event", type="primary")

    if submitted:
        if not aircraft_reg or not serial_off:
            st.error("⚠️ Please fill in at least Aircraft Registration and Serial Number.")
        else:
            # Create a dictionary for the new row
            new_entry = {
                "Date": pd.to_datetime(event_date),
                "Aircraft": aircraft_reg,
                "ATA": ata_chapter,
                "Component": comp_name,
                "Part Number": part_number,
                "Serial Number Off": serial_off,
                "Serial Number On": serial_on,
                "Reason": removal_reason,
                "Technician": tech_name,
                "Pilot": pilot_name
            }
            
            # Save to Session State (so it appears on Dashboard immediately)
            if "df" in st.session_state:
                new_df = pd.DataFrame([new_entry])
                st.session_state["df"] = pd.concat([st.session_state["df"], new_df], ignore_index=True)
            else:
                st.session_state["df"] = pd.DataFrame([new_entry])
            
            st.success(f"✅ Event recorded successfully for {comp_name}")
            render_footer()
