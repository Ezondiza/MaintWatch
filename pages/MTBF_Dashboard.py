# /pages/MTBF_Dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.navbar import create_header

st.set_page_config(page_title="Reliability Dashboard", layout="wide", initial_sidebar_state="collapsed")
create_header(current_page="Dashboard")

st.title("📊 Reliability Dashboard")

# 1. CHECK FOR DATA
if "df" not in st.session_state or st.session_state["df"].empty:
    st.warning("⚠️ No data found.")
    st.info("Please use 'Data Upload' to load history, or 'New Entry' to record an event.")
    st.stop()

df = st.session_state["df"]

# 2. DEBUGGER (Expand this if Plot is missing)
with st.expander("🔧 Debug: View Raw Data Columns"):
    st.write("Column Names detected:", df.columns.tolist())
    st.dataframe(df.head(3))

# 3. NORMALIZE COLUMNS (Attempt to auto-fix common name mismatches)
# This maps your possible CSV headers to standard names
column_map = {
    "Aircraft Registration": "Aircraft",
    "Registration": "Aircraft",
    "ATA Chapter": "ATA",
    "Date of Removal": "Date",
    "Component Name": "Component",
    "Removal Date": "Date"
}
df = df.rename(columns=column_map)

# 4. CONVERT DATE
try:
    df["Date"] = pd.to_datetime(df["Date"])
except Exception as e:
    st.error(f"Date Conversion Error: {e}")
    st.stop()

# 5. FILTERS
st.markdown("### 🔎 Filters")
f1, f2, f3 = st.columns(3)
with f1:
    # Handle cases where column might still be missing
    if "Aircraft" in df.columns:
        avail_ac = sorted(df["Aircraft"].astype(str).unique())
        sel_ac = st.multiselect("Aircraft", avail_ac, default=avail_ac)
    else:
        st.error("Column 'Aircraft' not found. Check Debug Data.")
        sel_ac = []

with f2:
    if "ATA" in df.columns:
        avail_ata = sorted(df["ATA"].astype(str).unique())
        sel_ata = st.multiselect("ATA Chapter", avail_ata, default=avail_ata)
    else:
        sel_ata = []

with f3:
    min_d, max_d = df["Date"].min().date(), df["Date"].max().date()
    sel_date = st.date_input("Date Range", [min_d, max_d])

# 6. APPLY FILTERS
mask = (
    df["Aircraft"].isin(sel_ac) & 
    df["ATA"].isin(sel_ata) & 
    (df["Date"].dt.date >= sel_date[0]) & 
    (df["Date"].dt.date <= sel_date[1])
)
filtered_df = df[mask]

# 7. SCATTER PLOT
if not filtered_df.empty:
    st.subheader("📅 Removal Timeline")
    
    # Check if we have the right columns for the plot
    if "Aircraft" in filtered_df.columns and "Date" in filtered_df.columns:
        fig = px.scatter(
            filtered_df,
            x="Date",
            y="Aircraft",
            color="ATA" if "ATA" in filtered_df.columns else None,
            hover_data=["Component", "Reason"] if "Component" in filtered_df.columns else None,
            title="Component Removals Timeline",
            size_max=15
        )
        fig.update_traces(marker=dict(size=14, line=dict(width=1, color='DarkSlateGrey')))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Cannot plot: Missing 'Date' or 'Aircraft' columns.")
else:
    st.info("No data matches the selected filters.")
