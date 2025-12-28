# /pages/Component_Removal.py
import pandas as pd
import streamlit as st
from forms.component_removal_form import component_removal_form
from utils.gsheet_loader import connect_to_sheet

st.set_page_config(page_title="Component Removal", layout="wide")
st.title("Component Removal")

# 1. Render the Main Form
component_removal_form()

# 2. Simple "Recent Activity" Log (Cleaner than the Debug View)
st.divider()
st.subheader("📋 Recent Removal Events")

if st.button("Check Last 5 Entries"):
    try:
        sheet = connect_to_sheet()
        if sheet:
            # Fetch all records
            data = sheet.get_all_records()
            if data:
                df = pd.DataFrame(data)
                # Show only the last 5 rows
                st.dataframe(df.tail(5), use_container_width=True)
            else:
                st.info("Log is currently empty.")
    except Exception as e:
        st.error(f"Could not load history: {e}")
