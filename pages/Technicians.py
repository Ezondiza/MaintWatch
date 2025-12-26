import streamlit as st
import pandas as pd

if "df" not in st.session_state:
    st.warning("Please upload or load data from the Home page.")
    st.stop()

df = st.session_state["df"]

st.title("Technician Performance")

tech_summary = df.groupby(["technician", "certification"]).agg(
    total_tasks=("anomaly", "count"),
    anomalies=("anomaly", "sum"),
    avg_experience=("experience_years", "mean")
).reset_index()

tech_summary["anomaly_rate (%)"] = (tech_summary["anomalies"] / tech_summary["total_tasks"] * 100).round(1)

st.dataframe(tech_summary.sort_values("anomaly_rate (%)", ascending=False))
