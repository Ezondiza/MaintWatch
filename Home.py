# /Home.py

import streamlit as st
from utils.data_loader import load_data, load_maintenance, merge_data

st.set_page_config(page_title="MaintWatch", layout="wide")

st.title("🛠️ Maintenance Watch")
st.subheader("Component Reliability and MTBF Tracking")

st.markdown(
    """
    MaintWatch supports aircraft maintenance reliability analysis
    using component removal history.

    Use this system to:
    • Record component removals
    • Analyze MTBF and reliability trends
    • Support maintenance planning and spares forecasting

    Start with **Component Removal** for new data entry.
    Use CSV upload only for historical backfill.
    """
)

st.divider()

st.markdown("### Historical Data Import")

uploaded_file = st.file_uploader(
    "Upload historical removal data (CSV)",
    type="csv"
)

components, technicians, pilots = load_data()

if uploaded_file:
    df = load_maintenance(uploaded_file)
    df = merge_data(df, components, technicians, pilots)
    st.session_state["df"] = df
    st.success("Historical data loaded successfully")
else:
    st.info("No file uploaded. Use Component Removal to enter new data.")
    from utils.migrate_removal_events import migrate_removal_events

if st.sidebar.button("Migrate removal events to new schema"):
    migrate_removal_events()
    st.success("Migration complete. Reload MTBF Dashboard.")

st.markdown(
    """Developed by Ghanshyam Acharya, 2025"""

