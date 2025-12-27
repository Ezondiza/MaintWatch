# /pages/MTBF_Dashboard.py

import streamlit as st
import pandas as pd

from utils.removal_events_loader import load_removal_events
from utils.mtbf_calculator import calculate_mtbf_by_component, calculate_mtbf_by_ata


st.set_page_config(page_title="MTBF Dashboard", layout="wide")

st.title("MTBF Dashboard")
st.caption("MTBF uses unscheduled component removals only. Values are based on aircraft FH deltas between repeated removals of the same serial number.")

df = load_removal_events()

if df.empty:
    st.info("No removal events found. Use Component Removal to enter removals.")
    st.stop()

required_cols = {"component_code", "component_name", "serial_number", "aircraft_reg", "removal_date", "aircraft_fh", "removal_reason"}
missing = sorted(list(required_cols - set(df.columns)))

if missing:
    st.error("Removal dataset is missing required columns: " + ", ".join(missing))
    st.caption("Open data/removal_events.csv and confirm the header matches the current schema.")
    st.dataframe(pd.DataFrame({"available_columns": list(df.columns)}), use_container_width=True)
    st.stop()

unsched_df = df[df["removal_reason"] == "Unscheduled Failure"]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Records", len(df))
col2.metric("Unscheduled Failures", len(unsched_df))
col3.metric("Distinct Components", df["component_code"].nunique())
col4.metric("Distinct Aircraft", df["aircraft_reg"].nunique())

with st.expander("Data columns seen by the app"):
    st.dataframe(pd.DataFrame({"columns": list(df.columns)}), use_container_width=True)

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("MTBF by Component")

    mtbf_comp = calculate_mtbf_by_component(df)

    if mtbf_comp.empty:
        st.info("Not enough repeated unscheduled removals to compute MTBF yet.")
    else:
        show_cols = [c for c in ["component_code", "component_name", "category", "criticality", "mtbf_fh", "failure_count"] if c in mtbf_comp.columns]
        st.dataframe(mtbf_comp[show_cols], use_container_width=True)

        top_n = st.slider("Top components to chart", 5, 30, 10)
        chart_source = mtbf_comp.head(top_n).copy()

        if "component_name" in chart_source.columns and "mtbf_fh" in chart_source.columns:
            st.bar_chart(chart_source.set_index("component_name")[["mtbf_fh"]])

with right:
    st.subheader("MTBF by ATA")

    mtbf_ata = calculate_mtbf_by_ata(df)

    if mtbf_ata.empty:
        st.info("Not enough repeated unscheduled removals to compute MTBF yet.")
    else:
        show_cols_ata = [c for c in ["ata_chapter", "mtbf_fh", "failure_count"] if c in mtbf_ata.columns]
        st.dataframe(mtbf_ata[show_cols_ata], use_container_width=True)

        top_n_ata = st.slider("Top ATA chapters to chart", 5, 30, 10)
        chart_ata = mtbf_ata.head(top_n_ata).copy()

        if "ata_chapter" in chart_ata.columns and "mtbf_fh" in chart_ata.columns:
            st.bar_chart(chart_ata.set_index("ata_chapter")[["mtbf_fh"]])

st.divider()

st.subheader("Forecasting Hook")
st.caption("Estimate expected removals using fleet hours divided by MTBF. This is a planning number, not a prediction.")

if "mtbf_comp" not in locals() or mtbf_comp.empty:
    st.info("Forecasting requires MTBF values. Add repeated unscheduled removals for the same serial number.")
    st.stop()

colf1, colf2 = st.columns(2)
fleet_hours = colf1.number_input("Fleet hours for the forecast period", min_value=0.0, step=10.0, value=300.0)
show_top = colf2.number_input("Show top items", min_value=5, step=5, value=15)

forecast_df = mtbf_comp.copy()

if "mtbf_fh" not in forecast_df.columns:
    st.error("MTBF table missing mtbf_fh. Check mtbf_calculator outputs.")
    st.dataframe(pd.DataFrame({"mtbf_columns": list(forecast_df.columns)}), use_container_width=True)
    st.stop()

forecast_df = forecast_df[forecast_df["mtbf_fh"] > 0].copy()
forecast_df["expected_failures"] = (fleet_hours / forecast_df["mtbf_fh"]).round(2)

display_cols = [c for c in ["component_code", "component_name", "criticality", "mtbf_fh", "failure_count", "expected_failures"] if c in forecast_df.columns]
out = forecast_df[display_cols].head(int(show_top))

st.dataframe(out, use_container_width=True)

if "component_name" in out.columns:
    st.bar_chart(out.set_index("component_name")[["expected_failures"]])
