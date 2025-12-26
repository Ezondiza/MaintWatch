import streamlit as st
import pandas as pd

if "df" not in st.session_state:
    st.warning("Please upload or load data from the Home page.")
    st.stop()

df = st.session_state["df"]

st.title("Pilot Performance")

pilot_summary = df.groupby(["pilot_name", "rank"]).agg(
    total_flights=("anomaly", "count"),
    anomalies=("anomaly", "sum"),
    avg_experience=("experience_years", "mean")
).reset_index()

pilot_summary["anomaly_rate (%)"] = (pilot_summary["anomalies"] / pilot_summary["total_flights"] * 100).round(1)

st.dataframe(pilot_summary.sort_values("anomaly_rate (%)", ascending=False))
