# maintwatch/pages/MTBF_Dashboard.py

import streamlit as st
import pandas as pd

from utils.mtb f_calculator import calculate_mtbf_by_component  # if your file name differs, fix import
from utils.data_loader import load_component_master  # assumes it returns components.csv as df

REMOVALS_PATH = "data/removal_events.csv"

st.set_page_config(page_title="MTBF Dashboard", layout="wide")
st.title("MTBF Dashboard")

st.caption(
    "MTBF uses unscheduled component removals only. "
    "Values are based on aircraft FH deltas between repeated removals of the same serial number."
)

def _read_removals():
    try:
        return pd.read_csv(REMOVALS_PATH)
    except Exception as e:
        st.error(f"Cannot read {REMOVALS_PATH}. Error: {e}")
        return pd.DataFrame()

def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    df = df.copy()
    df.columns = [c.strip() for c in df.columns]

    rename_map = {
        "aircraft_fh_at_removal": "aircraft_fh",
        "aircraft_fc_at_removal": "aircraft_fc",
    }
    for a, b in rename_map.items():
        if a in df.columns and b not in df.columns:
            df[b] = df[a]

    return df

def _required_cols_present(df: pd.DataFrame, cols: list[str]) -> bool:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        st.error("Removal dataset is missing required columns: " + ", ".join(missing))
        st.write("Available columns")
        st.dataframe(pd.DataFrame({"available_columns": df.columns.tolist()}), use_container_width=True)
        return False
    return True

rem_df = _read_removals()
rem_df = _normalize_columns(rem_df)

required = ["aircraft_reg", "component_name", "serial_number", "removal_date", "aircraft_fh", "aircraft_fc", "removal_reason"]
if not _required_cols_present(rem_df, required):
    st.stop()

# Filter for unscheduled removals for MTBF
# Your data uses either "Unscheduled" or "Unscheduled Failure". We treat both as unscheduled.
reason_series = rem_df["removal_reason"].astype(str).str.lower()
unscheduled_mask = reason_series.str.contains("unscheduled") | reason_series.str.contains("failure")
mtbf_input = rem_df[unscheduled_mask].copy()

if mtbf_input.empty:
    st.info("No unscheduled removal events found. Add unscheduled events to compute MTBF.")
    st.stop()

# Ensure proper types
mtbf_input["removal_date"] = pd.to_datetime(mtbf_input["removal_date"], errors="coerce")
mtbf_input["aircraft_fh"] = pd.to_numeric(mtbf_input["aircraft_fh"], errors="coerce")
mtbf_input["aircraft_fc"] = pd.to_numeric(mtbf_input["aircraft_fc"], errors="coerce")

mtbf_input = mtbf_input.dropna(subset=["removal_date", "aircraft_fh", "aircraft_fc", "serial_number", "component_name", "aircraft_reg"])

if mtbf_input.empty:
    st.info("After cleaning invalid rows, no usable unscheduled events remain.")
    st.stop()

# Compute MTBF
# We compute deltas per aircraft_reg + component_name + serial_number
df_sorted = mtbf_input.sort_values(["component_name", "serial_number", "aircraft_reg", "removal_date"]).copy()
df_sorted["fh_delta"] = df_sorted.groupby(["component_name", "serial_number", "aircraft_reg"])["aircraft_fh"].diff()
df_sorted["fc_delta"] = df_sorted.groupby(["component_name", "serial_number", "aircraft_reg"])["aircraft_fc"].diff()

df_valid = df_sorted.dropna(subset=["fh_delta", "fc_delta"])
df_valid = df_valid[(df_valid["fh_delta"] > 0) & (df_valid["fc_delta"] >= 0)]

if df_valid.empty:
    st.info("MTBF needs repeated removals of the same component serial number on the same aircraft. Add repeat events to see MTBF.")
    st.stop()

mtbf_comp = (
    df_valid.groupby("component_name")
    .agg(
        mtbf_fh=("fh_delta", "mean"),
        mtbf_fc=("fc_delta", "mean"),
        failure_count=("component_name", "count"),
    )
    .reset_index()
)

mtbf_comp["mtbf_fh"] = mtbf_comp["mtbf_fh"].round(1)
mtbf_comp["mtbf_fc"] = mtbf_comp["mtbf_fc"].round(1)
mtbf_comp = mtbf_comp.sort_values("mtbf_fh", ascending=False)

# Enrich with component master if available
# We try to bring component_code and criticality
try:
    comp_master = load_component_master()
    if not comp_master.empty:
        comp_master = comp_master.copy()
        comp_master.columns = [c.strip() for c in comp_master.columns]

        # If components.csv has no header, user must fix it. Still, we try a fallback.
        if "component_code" not in comp_master.columns and comp_master.shape[1] >= 6:
            comp_master.columns = ["component_code", "component_name", "category", "criticality", "inspection_interval_days", "ata_chapter"]

        join_cols = [c for c in ["component_name", "component_code", "criticality"] if c in comp_master.columns]
        if "component_name" in join_cols:
            mtbf_comp = mtbf_comp.merge(
                comp_master[["component_name"] + [c for c in ["component_code", "criticality"] if c in comp_master.columns]].drop_duplicates(),
                on="component_name",
                how="left",
            )
except Exception:
    pass

# Guarantee required display columns exist for the forecasting hook
for col, default in [("component_code", ""), ("criticality", "Unknown")]:
    if col not in mtbf_comp.columns:
        mtbf_comp[col] = default

st.subheader("MTBF by Component")
st.dataframe(
    mtbf_comp[["component_code", "component_name", "criticality", "mtbf_fh", "mtbf_fc", "failure_count"]],
    use_container_width=True
)

st.bar_chart(mtbf_comp.set_index("component_name")[["mtbf_fh"]])

# Forecasting hook
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

    forecast_df["expected_failures"] = (fleet_hours / forecast_df["mtbf_fh"]).round(2)

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

else:
    st.info("Forecast requires MTBF data and fleet hours.")
