import streamlit as st
from utils.data_loader import load_data, load_maintenance, merge_data

st.set_page_config(page_title="MaintWatch", layout="wide")

st.title("🛠️ MaintWatch")
st.subheader("Component Reliability and MTBF Tracking")

st.markdown(
    """
    MaintWatch supports aircraft maintenance reliability analysis based on
    component removal history.

    Use this application to:
    • Record component removals in a structured way  
    • Analyze reliability trends and MTBF  
    • Support maintenance planning and spares forecasting  

    Start with **Component Removal** for new data entry.
    Use CSV upload only for historical backfill.
    """
)

st.divider()

st.markdown("### Historical Data Import")

uploaded_file = st.file_uploader(
    "Upload historical maintenance or removal data (CSV)",
    type="csv",
    help="Use this only to import legacy or historical records"
)

components, technicians, pilots = load_data()

if uploaded_file:
    df = load_maintenance(uploaded_file)
    df = merge_data(df, components, technicians, pilots)

    st.session_state["df"] = df

    st.success("Historical data loaded successfully. Reliability views updated.")
else:
    st.info(
        "No file uploaded. Use the Component Removal page to begin recording removals."
    )
