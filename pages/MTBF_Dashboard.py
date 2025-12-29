import streamlit as st
import pandas as pd
import plotly.express as px
from utils.navbar import create_header
from utils.footer import render_footer

# 1. Page Config
st.set_page_config(page_title="Reliability Dashboard", layout="wide", initial_sidebar_state="collapsed")
create_header(current_page="Dashboard")

st.title("📉 Reliability Control Board")
st.markdown("Automated reliability analysis and CAMO alerts based on fleet performance.")

# 2. LOAD DATA
if "df" not in st.session_state or st.session_state["df"].empty:
    st.warning("⚠️ No data loaded.")
    st.info("Please go to **Data Upload** to fetch data from Cloud.")
    render_footer()
    st.stop()

df = st.session_state["df"].copy()

# 3. NORMALIZE COLUMNS
column_map = {
    "removal_date": "Date",
    "aircraft_reg": "Aircraft",
    "ata_chapter": "ATA",
    "component_name": "Component",
    "part_number": "Part Number",
    "aircraft_fh": "FH",
    "removal_reason": "Reason"
}
df = df.rename(columns=column_map)

# Data Type Conversions
df["Date"] = pd.to_datetime(df["Date"])
df["FH"] = pd.to_numeric(df["FH"], errors='coerce').fillna(0)
df["ATA"] = df["ATA"].astype(str)

# 4. FILTERS
st.markdown("### 🔍 Scope of Analysis")
f1, f2 = st.columns(2)
with f1:
    min_d, max_d = df["Date"].min().date(), df["Date"].max().date()
    sel_date = st.date_input("Analysis Period", [min_d, max_d])
with f2:
    avail_ata = sorted(df["ATA"].unique())
    sel_ata = st.multiselect("Filter by ATA Chapter", avail_ata, default=avail_ata)

# Apply Date Filter
if len(sel_date) == 2:
    mask = (df["Date"].dt.date >= sel_date[0]) & (df["Date"].dt.date <= sel_date[1]) & (df["ATA"].isin(sel_ata))
    filtered_df = df[mask]
else:
    filtered_df = df

# 5. 🧠 ENGINEERING LOGIC: ESTIMATE FLEET UTILIZATION
# To calculate MTBF, we need "Total Hours Flown" during this period.
# We estimate this by taking (Max FH - Min FH) for EACH aircraft in the filtered data.
fleet_hours = 0
active_aircraft = filtered_df["Aircraft"].unique()

for ac in active_aircraft:
    ac_data = filtered_df[filtered_df["Aircraft"] == ac]
    if not ac_data.empty:
        delta = ac_data["FH"].max() - ac_data["FH"].min()
        # If delta is 0 (only 1 entry), assume a standard 5 hours/day for the duration (simple fallback)
        if delta == 0 and len(sel_date) == 2:
            days = (sel_date[1] - sel_date[0]).days
            delta = days * 5 # Assumed daily utilization if no data
        fleet_hours += delta

# 6. RELIABILITY METRICS
total_removals = len(filtered_df)
fleet_mtbf = round(fleet_hours / total_removals) if total_removals > 0 else 0
reliability_rate = round((1 - (total_removals / fleet_hours)) * 100, 2) if fleet_hours > 0 else 100

# --- KPI DISPLAY ---
st.divider()
k1, k2, k3, k4 = st.columns(4)
k1.metric("📅 Total Fleet Hours (Est.)", f"{int(fleet_hours)} FH", help="Sum of FH delta per aircraft in period")
k2.metric("🔧 Total Removals", total_removals)
k3.metric("📈 Fleet MTBF", f"{fleet_mtbf} FH", delta_color="normal", 
          help="Mean Time Between Failures (Target: >1000)")
k4.metric("🛡️ Reliability Rate", f"{reliability_rate}%")

# 7. 🚨 CAMO ALERT SYSTEM
st.subheader("🚨 Active Reliability Alerts")

# ALERT 1: ROGUE COMPONENTS (High Frequency Failures)
# Logic: Any Part Number removed > 2 times in the selected period
rogue_check = filtered_df["Part Number"].value_counts()
rogues = rogue_check[rogue_check > 2] # Threshold = 2

# ALERT 2: LOW MTBF ATA CHAPTERS
# Logic: Calculate MTBF per ATA
ata_metrics = []
for ata in filtered_df["ATA"].unique():
    subset = filtered_df[filtered_df["ATA"] == ata]
    count = len(subset)
    if count > 0:
        mtbf = int(fleet_hours / count)
        if mtbf < 500: # Threshold for "Bad" ATA
            ata_metrics.append((ata, mtbf, count))

# DISPLAY ALERTS
c_alert1, c_alert2 = st.columns(2)

with c_alert1:
    if not rogues.empty:
        st.error(f"⚠️ **Rogue Components Detected ({len(rogues)})**")
        st.caption("Components with > 2 removals in this period:")
        for pn, count in rogues.items():
            # Find component name for this PN
            name = filtered_df[filtered_df["Part Number"] == pn]["Component"].iloc[0]
            st.markdown(f"**{name}** (P/N: {pn}): **{count} Failures**")
    else:
        st.success("✅ No Rogue Components detected (Threshold: >2 removals)")

with c_alert2:
    if ata_metrics:
        st.warning(f"⚠️ **Low Reliability Systems (<500 FH MTBF)**")
        for ata, mtbf, count in ata_metrics:
             st.markdown(f"ATA **{ata}**: MTBF **{mtbf} FH** ({count} removals)")
    else:
        st.success("✅ All Systems operating above min reliability targets.")

# 8. VISUALIZATION
st.divider()
tab1, tab2 = st.tabs(["📊 Pareto Analysis", "📉 MTBF Trend"])

with tab1:
    st.markdown("**Which components are hurting reliability the most?**")
    top_comp = filtered_df["Component"].value_counts().nlargest(10).reset_index()
    top_comp.columns = ["Component", "Count"]
    fig_bar = px.bar(top_comp, x="Count", y="Component", orientation='h', text="Count", color="Count", color_continuous_scale='Reds')
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    st.markdown("**Cumulative Removals over Time**")
    filtered_df = filtered_df.sort_values("Date")
    filtered_df["Cumulative Removals"] = range(1, len(filtered_df) + 1)
    fig_line = px.line(filtered_df, x="Date", y="Cumulative Removals", markers=True, title="Failure Rate Trend")
    st.plotly_chart(fig_line, use_container_width=True)

render_footer()
