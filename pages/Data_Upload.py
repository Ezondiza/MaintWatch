import streamlit as st
import pandas as pd
from utils.navbar import create_header
from utils.footer import render_footer
from utils.gsheet_loader import fetch_all_data

# 1. Page Config
st.set_page_config(page_title="Data Upload", layout="wide", initial_sidebar_state="collapsed")
create_header(current_page="Data Upload")

st.title("📂 Data Management")
st.markdown("Import historical maintenance records or sync with the cloud database.")

# 2. SELECTION: Cloud vs Local
tab1, tab2 = st.tabs(["☁️ Load from Google Sheet (Live)", "📄 Upload CSV (Legacy)"])

# --- TAB 1: GOOGLE SHEET LOAD ---
with tab1:
    st.subheader("Sync with Cloud Database")
    st.markdown("Pull the latest data from the **MaintWatch_Data** Google Sheet.")
    
    if st.button("🔄 Fetch Data from Cloud", type="primary"):
        with st.spinner("Connecting to Google Sheets..."):
            df_cloud = fetch_all_data("removal_events")
            
        if not df_cloud.empty:
            # Save to Session State
            st.session_state["df"] = df_cloud
            st.success(f"✅ Successfully loaded {len(df_cloud)} records from the cloud!")
            
            # Show Preview
            st.dataframe(df_cloud.head())
            
            # Suggest Next Step
            st.info("👉 You can now go to the **Dashboard** to view the analytics.")
        else:
            st.warning("⚠️ No data found in Google Sheet (or connection failed).")

# --- TAB 2: CSV UPLOAD ---
with tab2:
    st.subheader("Historical Data Upload")
    st.markdown("Use this for one-time bulk backfilling from Excel/CSV.")
    
    uploaded_file = st.file_uploader("Select CSV File", type="csv")

    if uploaded_file:
        try:
            df_local = pd.read_csv(uploaded_file)
            st.session_state["df"] = df_local
            st.success(f"✅ Loaded {len(df_local)} records from CSV.")
            st.dataframe(df_local.head())
        except Exception as e:
            st.error(f"Error parsing CSV: {e}")

render_footer()
