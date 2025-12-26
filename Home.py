import streamlit as st
from utils.data_loader import load_data, load_maintenance, merge_data, detect_anomalies

st.set_page_config(page_title="MaintWatch", layout="wide")
st.title("🛠️ MaintWatch: Maintenance Anomaly Explorer")

st.markdown("Upload your maintenance log or use the sample dataset to begin exploring flagged anomalies and performance insights.")

uploaded_file = st.file_uploader("📤 Upload maintenance CSV", type="csv")

# Load and merge data
components, technicians, pilots = load_data()
df = load_maintenance(uploaded_file)
df = merge_data(df, components, technicians, pilots)
df = detect_anomalies(df)

# Store in session state
st.session_state["df"] = df

st.success("✅ Data loaded and anomalies detected. Use the sidebar to explore insights.")
