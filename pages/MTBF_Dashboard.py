# /pages/MTBF_Dashboard.py

import streamlit as st
import pandas as pd

from utils.removal_events_loader import load_removal_events
from utils.mtbf_calculator import calculate_mtbf_by_component, calculate_mtbf_by_ata
from utils.forecasting import forecast_expected_failures

st.set_page_config(page_title="MTBF Dashboard", layout="wide")

st.title("MTBF Dashboard")

df = load_removal_events()

if df.empty:
    st.info("No removal events found. Use Component Removal to start recording removals.")
    st.stop()

st.caption("MTBF is calculated using unscheduled failure removals only.")

col1, col2, col3 = st.columns(3)
total_rows = col1.metric("Total Removal Records", len(df))
unsched = df[df["removal_reason"] == "Unscheduled Failure"]
col2.metric("Unscheduled Failures", len(unsched))
col3.metric("Distinct Components", df["component_name"].nunique() if "component_name" in df.columns else 0)

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("MTBF by Component")
    mtbf_comp = calculate_mtbf_by_component(df)

    if mtbf_comp.empty:
        st.info("Not enough repeated unscheduled removals to compute MTBF yet.")
    else:
        st.dataframe(mtbf_comp, use_container_width=True)

        top_n = st.slider("Show top components", 5, 30, 10)
        chart_df = mtbf_comp.head(top_n).set_index("component_name")[["mtbf_fh"]]
        st.bar_chart(chart_df)

with right:
    st.subheader("MTBF by ATA")
    mtbf_ata = calculate_mtbf_by_ata(df)

    if mtbf_ata.empty:
        st.info("Not enough repeated unscheduled removals to compute MTBF yet.")
    else:
        st.dataframe(mtbf_ata, use_container_width=True)

        top_n_ata = st.slider("Show top ATA chapters", 5, 30, 10)
        chart_ata = mtbf_ata.head(top_n_ata).set_index("ata_chapter")[["mtbf_fh"]]
        st.bar_chart(chart_ata)

st.divider()

st.subheader("Forecasting Hook")
st.caption("This is a simple planning estimate based on fleet hours divided by MTBF. Use it to size spares and plan supply.")

colf1, colf2 = st.columns(2)
fleet_hours = colf1.number_input("Fleet hours for the forecast period", min_value=0.0, step=10.0, value=300.0)
show_forecast_n = colf2.number_input("Show top items", min_value=5, step=5, value=15)

if not mtbf_comp.empty and fleet_hours > 0:
    forecast_df = forecast_expected_failures(mtbf_comp, fleet_hours)

    if forecast_df.empty:
        st.info("Forecast not available. Check MTBF data.")
    else:
        out = forecast_df[["component_name", "mtbf_fh", "failure_count", "expected_failures"]].head(int(show_forecast_n))
        st.dataframe(out, use_container_width=True)

        chart_f = out.set_index("component_name")[["expected_failures"]]
        st.bar_chart(chart_f)
else:
    st.info("Forecast requires MTBF values and fleet hours.")
