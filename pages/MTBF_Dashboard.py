# /pages/MTBF_Dashboard.py

import streamlit as st
from utils.removal_events_loader import load_removal_events
from utils.mtbf_calculator import (
    calculate_mtbf_by_component,
    calculate_mtbf_by_ata
)

st.set_page_config(page_title="MTBF Dashboard", layout="wide")

st.title("MTBF Dashboard")
st.caption("MTBF calculated using unscheduled component removals only")

df = load_removal_events()

if df.empty:
    st.info("No removal data available. Enter component removals first.")
    st.stop()

col1, col2, col3 = st.columns(3)
col1.metric("Total Removal Records", len(df))
col2.metric(
    "Unscheduled Failures",
    len(df[df["removal_reason"] == "Unscheduled Failure"])
)
col3.metric("Distinct Components", df["component_code"].nunique())

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("MTBF by Component")

    mtbf_comp = calculate_mtbf_by_component(df)

    if mtbf_comp.empty:
        st.info("Not enough repeated failures to compute MTBF.")
    else:
        st.dataframe(mtbf_comp, use_container_width=True)

        st.caption("Lower MTBF indicates higher reliability concern")

        chart_df = mtbf_comp.set_index("component_name")[["mtbf_fh"]]
        st.bar_chart(chart_df)

with right:
    st.subheader("MTBF by ATA Chapter")

    mtbf_ata = calculate_mtbf_by_ata(df)

    if mtbf_ata.empty:
        st.info("Not enough repeated failures to compute MTBF.")
    else:
        st.dataframe(mtbf_ata, use_container_width=True)

        chart_ata = mtbf_ata.set_index("ata_chapter")[["mtbf_fh"]]
        st.bar_chart(chart_ata)
