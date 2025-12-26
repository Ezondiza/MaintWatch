import streamlit as st
import pandas as pd

if "df" not in st.session_state:
    st.warning("Please upload or load data from the Home page.")
    st.stop()

df = st.session_state["df"]

st.title("ATA Chapter Summary")

ata_summary = df.groupby("ata_chapter").agg(
    total_events=("anomaly", "count"),
    anomalies=("anomaly", "sum")
).reset_index()

ata_summary["anomaly_rate (%)"] = (ata_summary["anomalies"] / ata_summary["total_events"] * 100).round(1)

st.dataframe(ata_summary.sort_values("anomaly_rate (%)", ascending=False))
