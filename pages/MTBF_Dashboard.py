# /pages/MTBF_Dashboard.py
import streamlit as st
import pandas as pd
from utils.navbar import create_header

# 1. Page Config
st.set_page_config(page_title="Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. Render Navbar
create_header(current_page="Dashboard")

st.title("MTBF Dashboard")
st.markdown("Unscheduled component removal analysis based on aircraft FH deltas.")

# 3. Data Loading Logic
# Check if data is already in session state
if "df" not in st.session_state:
    st.warning("⚠️ No data loaded yet.")
    st.markdown(
        """
        To view the dashboard, please either:
        1. Go to **Data Upload** to import historical records.
        2. Go to **Home** and add a new removal event.
        """
    )
    # Optional: You could try to load a default file here if you have one
    # try:
    #     from utils.data_loader import load_data
    #     st.session_state["df"] = load_data()
    # except:
    #     pass
else:
    # Use the data from session state
    df = st.session_state["df"]
    
    st.success(f"Data Loaded: {len(df)} records available.")
    
    # --- YOUR DASHBOARD CODE GOES HERE ---
    # Paste your charts, metrics, and analysis code below this line.
    
    st.metric("Total Component Removals", len(df))
    st.dataframe(df.head())
