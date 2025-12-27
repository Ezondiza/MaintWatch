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
st.subheader("Forecasting Hook")
st.caption(
    "Simple planning estimate based on fleet hours divided by MTBF. "
    "Use this for spares sizing and maintenance planning."
)

colf1, colf2 = st.columns(2)
fleet_hours = colf1.number_input(
    "Fleet hours for the forecast period",
    min_value=0.0,
    step=10.0,
    value=300.0
)
show_top = colf2.number_input(
    "Show top items",
    min_value=5,
    step=5,
    value=15
)

if not mtbf_comp.empty and fleet_hours > 0:

    forecast_df = mtbf_comp.copy()
    forecast_df = forecast_df[forecast_df["mtbf_fh"] > 0]

    forecast_df["expected_failures"] = (
        fleet_hours / forecast_df["mtbf_fh"]
    ).round(2)

    out = forecast_df[
        [
            "component_code",
            "component_name",
            "criticality",
            "mtbf_fh",
            "failure_count",
            "expected_failures"
        ]
    ].head(int(show_top))

    st.dataframe(out, use_container_width=True)

    chart_df = out.set_index("component_name")[["expected_failures"]]
    st.bar_chart(chart_df)

else:
    st.info("Forecast requires MTBF data and fleet hours.")
