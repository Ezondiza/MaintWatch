import streamlit as st
import pandas as pd
from datetime import date
from utils.navbar import create_header
from utils.footer import render_footer
from utils.gsheet_loader import append_removal_event_gsheet, fetch_all_data

# 1. Page Config
st.set_page_config(page_title="New Removal", layout="wide", initial_sidebar_state="collapsed")
create_header(current_page="New Entry")

st.title("➕ New Component Removal")

# --- 2. SMART DROPDOWN LOGIC (CACHED) ---
@st.cache_data(ttl=300) # Cache for 5 minutes automatically
def load_reference_data():
    """
    Fetches Fleet and ATA data from Google Sheets to populate dropdowns.
    """
    # Fetch DataFrames
    df_fleet = fetch_all_data("aircraft_fleet")
    df_ata = fetch_all_data("ata_chapters")
    
    # Process Fleet List
    if not df_fleet.empty and "Registration" in df_fleet.columns:
        fleet_list = sorted(df_fleet["Registration"].astype(str).unique().tolist())
    else:
        fleet_list = ["9N-AHA", "9N-AHB", "9N-AIC"] # Fallback
        
    # Process ATA List (Combine Code + Description)
    if not df_ata.empty and "Chapter" in df_ata.columns:
        # If description exists, combine them: "32 | Landing Gear"
        if "Description" in df_ata.columns:
            # Helper to format
            def fmt_ata(row):
                return f"{row['Chapter']} | {row['Description']}"
            ata_list = sorted(df_ata.apply(fmt_ata, axis=1).tolist())
        else:
            ata_list = sorted(df_ata["Chapter"].astype(str).unique().tolist())
    else:
        ata_list = ["21 | Air Conditioning", "32 | Landing Gear", "73 | Engine Fuel"] # Fallback

    return fleet_list, ata_list

# Refresh Button (To clear cache if you just added a new plane)
col_title, col_refresh = st.columns([4, 1])
with col_refresh:
    if st.button("🔄 Refresh Lists"):
        load_reference_data.clear() # Clears the cache
        st.toast("Reference lists refreshed from Cloud!", icon="☁️")

# Load the data
aircraft_options, ata_options = load_reference_data()

# --- 3. THE FORM ---
st.markdown("Record an unscheduled component removal event.")

with st.form("removal_entry_form"):
    st.subheader("Event Details")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        event_date = st.date_input("Date of Removal", value=date.today())
    with c2:
        # SMART DROPDOWN: Aircraft
        aircraft_reg = st.selectbox("Aircraft Registration", options=aircraft_options) 
    with c3:
        # SMART DROPDOWN: ATA Chapter
        ata_selection = st.selectbox("ATA Chapter", options=ata_options)
        # Extract just the number (e.g. "32") for saving
        ata_chapter = ata_selection.split(" | ")[0] if "|" in ata_selection else ata_selection

    st.subheader("Component Details")
    c4, c5 = st.columns(2)
    with c4:
        comp_name = st.text_input("Component Name", placeholder="e.g., Main Wheel")
    with c5:
        part_number = st.text_input("Part Number (P/N)")

    # Component Type
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
    
    m1, m2 = st.columns(2)
    with m1:
        aircraft_fh = st.number_input("Aircraft FH (at removal)", min_value=0.0, step=0.1, format="%.1f")
    with m2:
        aircraft_fc = st.number_input("Aircraft FC (at removal)", min_value=0, step=1)

    removal_reason = st.text_area("Reason for Removal / Defect Description")
    
    c8, c9 = st.columns(2)
    with c8:
        tech_name = st.text_input("Technician Name")
    with c9:
        pilot_name = st.text_input("Pilot Name")

    # 4. Form Submission Logic
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
                "ata_chapter": ata_chapter, # We save just the code "32"
                "removal_date": pd.to_datetime(event_date),
                "aircraft_fh": aircraft_fh,
                "aircraft_fc": aircraft_fc,
                "removal_type": "Unscheduled",
                "removal_reason": removal_reason
            }
            
            # Save to Google Sheet
            with st.spinner("Saving to Cloud Database..."):
                if append_removal_event_gsheet(new_entry):
                    st.success(f"✅ Event recorded for {comp_name} on {aircraft_reg}")
                    st.balloons()

render_footer()
