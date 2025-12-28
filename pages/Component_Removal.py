import streamlit as st
import pandas as pd
from datetime import date
from utils.navbar import create_header
from utils.data_loader import load_data

# 1. Page Configuration
st.set_page_config(page_title="New Removal", layout="wide", initial_sidebar_state="collapsed")

# 2. Render Navbar (Highlighted as 'Home' since this is a sub-feature of daily work)
create_header(current_page="Home")

st.title("➕ New Component Removal")
st.markdown("Record an unscheduled component removal event.")

# 3. Load Reference Data
try:
    components, technicians, pilots = load_data()
except Exception as e:
    st.error(f"Error loading reference data: {e}")
    st.stop()

# 4. Form Interface
with st.form("removal_entry_form"):
    st.subheader("Event Details")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        event_date = st.date_input("Date of Removal", value=date.today())
    with c2:
        # You might want to make this a dropdown if you have a fleet list later
        aircraft_reg = st.text_input("Aircraft Registration", placeholder="e.g., 9N-AHA") 
    with c3:
        ata_chapter = st.text_input("ATA Chapter", placeholder="e.g., 32-40")

    st.subheader("Component Details")
    c4, c5 = st.columns(2)
    with c4:
        # Dropdown for Component Name
        comp_name = st.selectbox("Component Name", options=components)
    with c5:
        # If your components list is just names, we let them type the P/N, 
        # or if 'components' is a dict, you can auto-fill this.
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

    # 5. Form Submission Logic
    submitted = st.form_submit_button("💾 Save Removal Event", type="primary")

    if submitted:
        if not aircraft_reg or not serial_off:
            st.error("⚠️ Please fill in at least Aircraft Registration and Serial Number.")
        else:
            # Create a dictionary for the new row
            new_entry = {
                "Date": event_date,
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
            
            # --- SAVING LOGIC ---
            # 1. Update Session State (Immediate reflection in Dashboard)
            if "df" in st.session_state:
                # Append to existing dataframe
                new_df = pd.DataFrame([new_entry])
                st.session_state["df"] = pd.concat([st.session_state["df"], new_df], ignore_index=True)
            else:
                # Create new if doesn't exist
                st.session_state["df"] = pd.DataFrame([new_entry])
            
            # 2. Append to CSV (Persistence)
            # Note: On Streamlit Cloud, this CSV resets when the app reboots unless committed to Git.
            # Ideally, you would append to a database here.
            try:
                # Assuming your main data file is 'maintenance_data.csv'
                # Check if file exists to determine if we need a header
                file_path = "maintenance_data.csv"
                pd.DataFrame([new_entry]).to_csv(file_path, mode='a', header=False, index=False)
                st.success(f"✅ Event recorded for Component: {comp_name}")
            except Exception as e:
                st.warning(f"Data saved to session but failed to write to CSV: {e}")
