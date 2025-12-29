import streamlit as st
import pandas as pd
from datetime import date
from utils.navbar import create_header
from utils.gsheet_loader import append_removal_event_gsheet

# 1. Page Config
st.set_page_config(page_title="New Removal", layout="wide", initial_sidebar_state="collapsed")
create_header(current_page="New Entry")

st.title("➕ New Component Removal")
st.markdown("Record an unscheduled component removal event.")

# 2. Form Interface
with st.form("removal_entry_form"):
    st.subheader("Event Details")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        event_date = st.date_input("Date of Removal", value=date.today())
    with c2:
        aircraft_reg = st.text_input("Aircraft Registration", placeholder="e.g., 9N-AHA") 
    with c3:
        ata_chapter = st.text_input("ATA Chapter", placeholder="e.g., 32")

    st.subheader("Component Details")
    c4, c5 = st.columns(2)
    with c4:
        comp_name = st.text_input("Component Name", placeholder="e.g., Main Wheel")
    with c5:
        part_number = st.text_input("Part Number (P/N)")

    # Component Type Selection
    st.markdown("##### Component Life Type")
    comp_type = st.radio(
        "Select Type:",
        options=["On Condition (OC)", "Life Limited (LL)"],
        horizontal=True
    )

    c6, c7 = st.columns(2)
    with c6:
        serial_off = st.text_input("Serial Number OFF")
    with c7:
        serial_on = st.text_input("Serial Number ON")

    st.subheader("Maintenance Data")
    
    # --- MISSING FIELDS ADDED HERE ---
    m1, m2 = st.columns(2)
    with m1:
        aircraft_fh = st.number_input("Aircraft FH (at removal)", min_value=0.0, step=0.1, format="%.1f")
    with m2:
        aircraft_fc = st.number_input("Aircraft FC (at removal)", min_value=0, step=1)
    # ---------------------------------

    removal_reason = st.text_area("Reason for Removal / Defect Description")
    
    c8, c9 = st.columns(2)
    with c8:
        tech_name = st.text_input("Technician Name")
    with c9:
        pilot_name = st.text_input("Pilot Name")

    # 3. Form Submission Logic
    submitted = st.form_submit_button("💾 Save Removal Event", type="primary")

    if submitted:
        if not aircraft_reg or not serial_off:
            st.error("⚠️ Please fill in at least Aircraft Registration and Serial Number.")
        else:
            # Create dictionary matching EXACT Google Sheet Headers
            new_entry = {
                "aircraft_reg": aircraft_reg,
                "component_code": "N/A", 
                "component_name": comp_name,
                "part_number": part_number,
                "component_type": comp_type,
                "serial_number": serial_off,
                "ata_chapter": ata_chapter,
                "removal_date": pd.to_datetime(event_date),
                "aircraft_fh": aircraft_fh,  # Now included
                "aircraft_fc": aircraft_fc,  # Now included
                "removal_type": "Unscheduled",
                "removal_reason": removal_reason
            }
            
            # Save to Google Sheet
            with st.spinner("Saving to Cloud Database..."):
                if append_removal_event_gsheet(new_entry):
                    st.success(f"✅ Event recorded for {comp_name} ({comp_type})")
                    st.balloons()
