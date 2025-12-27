# pages/MTBF_Dashboard.py

import streamlit as st
import pandas as pd

from utils.mtbf_calculator import calculate_mtbf_by_component

DATA_REMOVALS = "data/removal_events.csv"
DATA_COMPONENTS = "data/components.csv"

st.set_page_config(page_title="MTBF Dashboard", layout="wide")

st.title("MTBF Dashboard")
st.caption(
    "MTBF uses unscheduled component removals only. "
    "Values are based on aircraft FH deltas between repeated removals "
    "of the same serial number."
)

# -----------------------------
# Load data
# -----------------------------

try:
    removal_df = pd.read_csv(DATA_REMOVALS)
    components_df = pd.read_csv(DATA_COMPONENTS)
except Exception as e:
    st.error("Failed to load data files")
    st.stop()

# -----------------------------
# Validate minimum schema
# -----------------------------

required_cols = [
    "component_code",
    "serial_number",
    "aircraft_reg",
    "aircraft_fh",
    "removal_date",
    "event_type",
]

missing = [c for c in required_cols if c not in removal_df.columns]

if missing:
    st.error(
        "Removal dataset is missing required columns: "
        + ", ".join(missing)
    )
    st.dataframe(
        pd.DataFrame({"available_columns": removal_df.columns})
    )
    st.stop()

# -----------------------------
# MTBF calculation
# -----------------------------

mtbf_comp = calculate_mtbf_by_component(
    removal_df=removal_df,
    components_df=components_df,
)

if mtbf_comp.empty:
    st.info("Not enough unscheduled removals to calculate MTBF.")
    st.stop()

st.subheader("MTBF by Component")
st.dataframe(mtbf_comp, use_container_width=True)

# -----------------------------
# Forecasting hook
# -----------------------------

st.divider()
st.subheader("Forecasting Hook")
st.caption(
    "Simple planning estimate based on fleet hours divided by MTBF. "
    "Use this for spares sizing and maintenance planning."
)

col1, col2 = st.columns(2)

fleet_hours = col1.number_input(
    "Fleet hours for the forecast period",
    min_value=0.0,
    step=10.0,
    value=300.0,
)

show_top = col2.number_input(
    "Show top items",
    min_value=5,
    step=5,
    value=15,
)

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
        "expected_failures",
    ]
].head(int(show_top))

st.dataframe(out, use_container_width=True)

chart_df = out.set_index("component_name")[["expected_failures"]]
st.bar_chart(chart_df)
