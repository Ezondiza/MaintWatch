# /pages/Component_Removal.py

import streamlit as st
from forms.component_removal_form import component_removal_form

st.set_page_config(page_title="Component Removal", layout="wide")

st.title("Component Removal")

component_removal_form()

# Add this at the very bottom of pages/Component_Removal.py

st.divider()
st.subheader("🔍 Debug: View Saved Data")

import os

if os.path.exists("data/removal_events.csv"):
    try:
        debug_df = pd.read_csv("data/removal_events.csv")
        st.dataframe(debug_df)  # This shows the actual live data
        
        # Add a download button so you can save it to your computer
        csv = debug_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download Live CSV",
            csv,
            "removal_events.csv",
            "text/csv",
            key='download-csv'
        )
    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.warning("File data/removal_events.csv does not exist yet.")
