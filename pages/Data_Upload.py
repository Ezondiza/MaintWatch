# /pages/Data_Upload.py
import streamlit as st
from utils.navbar import create_header
from utils.data_loader import load_maintenance, merge_data, load_data

st.set_page_config(page_title="Data Upload", layout="wide", initial_sidebar_state="collapsed")
create_header(current_page="Data Upload")

st.title("📂 Historical Data Upload")
st.markdown("Use this module to bulk import historical maintenance records via CSV.")

st.info("💡 **Note:** This is for backfilling data. For daily entries, use the 'New Component Removal' button on Home.")

uploaded_file = st.file_uploader("Select CSV File", type="csv")

if uploaded_file:
    # Load reference data
    components, technicians, pilots = load_data()
    
    # Process the CSV
    try:
        df = load_maintenance(uploaded_file)
        df = merge_data(df, components, technicians, pilots)
        
        # Save to session state (or your database)
        st.session_state["df"] = df
        
        st.success(f"✅ Successfully processed {len(df)} records.")
        st.dataframe(df.head())
        
    except Exception as e:
        st.error(f"Error processing file: {e}")
