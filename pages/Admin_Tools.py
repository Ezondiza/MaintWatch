# /pages/Admin_Tools.py
import streamlit as st
from utils.navbar import create_header

st.set_page_config(page_title="Admin Configuration", layout="wide", initial_sidebar_state="collapsed")
create_header(current_page="Admin Tools")

st.title("🛠️ System Configuration")
st.markdown("Manage system references, aircraft fleet, and database maintenance.")

# Create Tabs for the different Admin Functions
tab1, tab2, tab3 = st.tabs(["✈️ Aircraft Fleet", "📚 ATA Chapters", "⚠️ Danger Zone"])

# --- TAB 1: AIRCRAFT DETAILS ---
with tab1:
    st.subheader("Manage Fleet Details")
    st.info("Feature coming soon: Add/Edit Aircraft Registrations and MSN.")
    # Placeholder for future form
    # with st.form("add_aircraft"):
    #    st.text_input("Registration (e.g., 9N-AHA)")
    #    st.form_submit_button("Add Aircraft")

# --- TAB 2: ATA REFERENCES ---
with tab2:
    st.subheader("Manage ATA Chapter References")
    st.info("Feature coming soon: Add/Edit ATA Chapter descriptions.")
    # Placeholder for future table editor
    # st.data_editor(df_ata_codes)

# --- TAB 3: DANGER ZONE (WIPE) ---
with tab3:
    st.subheader("Database Maintenance")
    st.error("⚠️ **Critical Actions**")
    
    st.markdown("These actions are irreversible.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Wipe All Data", type="primary"):
            # Logic to clear session state or truncate DB tables
            st.session_state.clear()
            st.toast("System memory cleared!", icon="🧹")
            st.rerun()
            
    st.caption("Use 'Wipe All Data' to reset the current session for testing.")
