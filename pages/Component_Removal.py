# /pages/Component_Removal.py
import pandas as pd
import streamlit as st
from forms.component_removal_form import component_removal_form
from utils.gsheet_loader import connect_to_sheet

st.set_page_config(page_title="Component Removal", layout="wide")

st.title("Component Removal")

# 1. Render the Form
component_removal_form()

# ---------------------------------------------------------
# 2. NEW DEBUG SECTION: View Live Google Sheet Data
# ---------------------------------------------------------
st.divider()
st.subheader("☁️ Live Google Sheet Data")

# We use a button so it doesn't slow down the app on every load
if st.button("Refresh Google Sheet Data"):
    try:
        # Connect to the cloud
        sheet = connect_to_sheet()
        
        # specific command to get all data as a list of dictionaries
        data = sheet.get_all_records()
        
        if data:
            # Convert to a readable table
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.success(f"✅ Successfully loaded {len(df)} rows from Google Sheets.")
        else:
            st.warning("⚠️ The Google Sheet is currently empty.")
            
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
