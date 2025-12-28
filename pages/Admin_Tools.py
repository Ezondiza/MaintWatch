import streamlit as st
from utils.navbar import create_header
from utils.data_loader import load_maintenance, merge_data, load_data
from utils.migrate_removal_events import migrate_removal_events

st.set_page_config(page_title="Admin Tools", layout="wide", initial_sidebar_state="collapsed")
create_header(current_page="Admin Tools")

st.title("🛠️ Admin Tools")

st.warning("⚠️ Restricted Area: These tools affect the core database.")

st.subheader("1. Historical Data Import")
uploaded_file = st.file_uploader("Upload historical removal data (CSV)", type="csv")

if uploaded_file:
    # Your original loading logic
    components, technicians, pilots = load_data()
    df = load_maintenance(uploaded_file)
    df = merge_data(df, components, technicians, pilots)
    st.session_state["df"] = df
    st.success(f"Successfully loaded {len(df)} records from history.")

st.divider()

st.subheader("2. Database Maintenance")
if st.button("Run Migration (Update Schema)"):
    migrate_removal_events()
    st.success("Migration complete.")
