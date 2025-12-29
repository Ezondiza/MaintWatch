import streamlit as st
import pandas as pd
import plotly.express as px
from utils.navbar import create_header
from utils.footer import render_footer

# 1. Page Config
st.set_page_config(page_title="Dashboard", layout="wide", initial_sidebar_state="collapsed")
create_header(current_page="Dashboard")

st.title("📊 Reliability & MTBF Dashboard")

# 2. CHECK FOR DATA
if "df" not in st.session_state or st.session_state["df"].empty:
    st.warning("⚠️ No data currently loaded.")
    st.info("Please go to **Data Upload** to fetch data from the cloud.")
    render_footer()
    st.stop()

df = st.session_state["df"].copy() # Work on a copy to avoid corrupting session state

# 3. NORMALIZE COLUMNS
# Map Google Sheet names to Dashboard standard names
column_map = {
    "removal_date": "Date",
    "aircraft_reg": "Aircraft",
    "ata_chapter": "ATA",
    "component_name": "Component",
    "removal_reason": "Reason"
}
df = df.rename(columns=column_map)

# --- 4. DATA TYPE FIX (THE CRITICAL STEP) ---
# Ensure these columns exist, then force them to be Strings
if "Aircraft" in df.columns:
    df["Aircraft"] = df["Aircraft"].astype(str)
    
if "ATA" in df.columns:
    df["ATA"] = df["ATA"].astype(str)

# 5. DATE CONVERSION
try:
    df["Date"] = pd.to_datetime(df["Date"])
except Exception as e:
    st.error(f"Error parsing dates: {e}")
    st.stop()

# 6. FILTERS
st.markdown("### 🔎 Filters")
f1, f2, f3 = st.columns(3)

# Filter: Aircraft
with f1:
    if "Aircraft" in df.columns:
        # Get unique values as a sorted list
        avail_ac = sorted(list(df["Aircraft"].unique()))
        sel_ac = st.multiselect("Aircraft", avail_ac, default=avail_ac)
    else:
        sel_ac = []

# Filter: ATA
with f2:
    if "ATA" in df.columns:
        # Get unique values as a sorted list
        avail_ata = sorted(list(df["ATA"].unique()))
        sel_ata = st.multiselect("ATA Chapter", avail_ata, default=avail_ata)
    else:
        sel_ata = []

# Filter: Date
with f3:
    if "Date" in df.columns and not df.empty:
        min_d = df["Date"].min().date()
        max_d = df["Date"].max().date()
        sel_date = st.date_input("Date Range", [min_d, max_d])
    else:
        sel_date = []

# 7. APPLY FILTERS
if "Aircraft" in df.columns and "ATA" in df.columns:
    mask = (df["Aircraft"].isin(sel_ac)) & (df["ATA"].isin(sel_ata))
    
    # Handle Date Filter
    if len(sel_date) == 2:
        mask = mask & (df["Date"].dt.date >= sel_date[0]) & (df["Date"].dt.date <= sel_date[1])
        
    filtered_df = df[mask]
else:
    filtered_df = df

# 8. VISUALIZATIONS
if not filtered_df.empty:
    st.divider()
    
    # KPI Metrics
    k1, k2, k3 = st.columns(3)
    k1.metric("Total Removals", len(filtered_df))
    if "Component" in filtered_df.columns:
        k2.metric("Unique Components", filtered_df["Component"].nunique())
    if "ATA" in filtered_df.columns:
        # Calculate mode safely
        mode_val = filtered_df["ATA"].mode()
        top_ata = mode_val[0] if not mode_val.empty else "N/A"
        k3.metric("Most Frequent ATA", top_ata)

    # --- CHART 1: SCATTER PLOT ---
    st.subheader("📅 Component Removal Timeline")
    
    if "Aircraft" in filtered_df.columns:
        fig = px.scatter(
            filtered_df,
            x="Date",
            y="Aircraft",
            color="ATA",
            hover_data=["Component", "Reason"] if "Component" in filtered_df.columns else None,
            title="Removal Events by Date",
            size_max=15
        )
        # Make dots bigger and add border
        fig.update_traces(marker=dict(size=14, line=dict(width=1, color='DarkSlateGrey')))
        st.plotly_chart(fig, use_container_width=True)

    # --- CHART 2: BAR CHART ---
    if "Component" in filtered_df.columns:
        st.subheader("🏆 Top Offending Components")
        top_comp = filtered_df["Component"].value_counts().nlargest(10).reset_index()
        top_comp.columns = ["Component", "Count"]
        
        fig_bar = px.bar(top_comp, x="Count", y="Component", orientation='h', text="Count")
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)

else:
    st.warning("No records match the selected filters.")
    st.write("Debug - Current Filter Selection:")
    st.write(f"Aircraft: {sel_ac}")
    st.write(f"ATA: {sel_ata}")

render_footer()
