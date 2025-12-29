import streamlit as st
import pandas as pd
import plotly.express as px
from utils.navbar import create_header
from utils.footer import render_footer

# 1. Page Config
st.set_page_config(page_title="Reliability Dashboard", layout="wide", initial_sidebar_state="collapsed")
create_header(current_page="Dashboard")

st.title("📉 Reliability Control Board")
st.markdown("Monitor fleet health, track repetitive defects, and analyze MTBF trends.")

# 2. LOAD DATA
if "df" not in st.session_state or st.session_state["df"].empty:
    st.warning("⚠️ No data loaded.")
    st.info("Please go to **Admin Tools** -> **Testing Data** and click 'Generate 50 Smart Records' to see this dashboard in action.")
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
    "removal_reason": "Reason",
    "component_type": "Type"
}
df = df.rename(columns=column_map)

# Data Type Enforcement
df["Date"] = pd.to_datetime(df["Date"])
df["FH"] = pd.to_numeric(df["FH"], errors='coerce').fillna(0)
df["ATA"] = df["ATA"].astype(str)
if "Aircraft" in df.columns:
    df["Aircraft"] = df["Aircraft"].astype(str)

# 4. FILTERS (Restored Aircraft Filter)
st.markdown("### 🔍 Scope of Analysis")
f1, f2, f3 = st.columns(3)

with f1:
    # Aircraft Filter
    avail_ac = sorted(df["Aircraft"].unique())
    sel_ac = st.multiselect("Filter by Aircraft", avail_ac, default=avail_ac)

with f2:
    # ATA Filter
    avail_ata = sorted(df["ATA"].unique())
    sel_ata = st.multiselect("Filter by ATA Chapter", avail_ata, default=avail_ata)

with f3:
    # Date Filter
    min_d, max_d = df["Date"].min().date(), df["Date"].max().date()
    sel_date = st.date_input("Analysis Period", [min_d, max_d])

# Apply Filters
mask = (df["Aircraft"].isin(sel_ac)) & (df["ATA"].isin(sel_ata))
if len(sel_date) == 2:
    mask = mask & (df["Date"].dt.date >= sel_date[0]) & (df["Date"].dt.date <= sel_date[1])
filtered_df = df[mask]

# 5. ENGINEERING LOGIC & KPI CALCULATION
# Estimate Fleet Hours based on (Max FH - Min FH) per aircraft in selection
fleet_hours = 0
for ac in sel_ac:
    ac_data = filtered_df[filtered_df["Aircraft"] == ac]
    if not ac_data.empty:
        delta = ac_data["FH"].max() - ac_data["FH"].min()
        if delta == 0: delta = 10 # Minimal fallback to avoid div/0
        fleet_hours += delta

total_removals = len(filtered_df)
fleet_mtbf = int(fleet_hours / total_removals) if total_removals > 0 else 0
reliability = round((1 - (total_removals / fleet_hours)) * 100, 2) if fleet_hours > 0 else 100

# 6. KPI ROW ("The Golden Numbers")
st.divider()
k1, k2, k3, k4 = st.columns(4)
k1.metric("✈️ Fleet Hours (Period)", f"{int(fleet_hours)} FH")
k2.metric("🔧 Total Removals", total_removals)
k3.metric("📈 Fleet MTBF", f"{fleet_mtbf} FH", help="Target: >500 FH", 
          delta=f"{fleet_mtbf - 500} vs Target")
k4.metric("🛡️ Technical Dispatch", f"{reliability}%")

# 7. 🚨 ALERT SECTION
# Identify "Repetitive Defects" (Same Part removed > 2 times in period)
rogues = filtered_df["Part Number"].value_counts()
rogues = rogues[rogues > 2]

if not rogues.empty:
    st.error(f"⚠️ **ALERT: Repetitive Defects Detected**")
    st.markdown("The following parts are failing repeatedly (Potential Rogue Units):")
    # Create a clean little table for the rogues
    rogue_list = []
    for pn, count in rogues.items():
        # Get Component Name
        name = filtered_df[filtered_df["Part Number"] == pn]["Component"].iloc[0]
        rogue_list.append({"Component": name, "P/N": pn, "Failures": count})
    st.table(pd.DataFrame(rogue_list))
else:
    st.success("✅ No repetitive defects detected (Threshold: >2 removals in period).")

# 8. ANALYTICAL CHARTS
st.subheader("📊 Defect Analysis")

tab_scatter, tab_pareto = st.tabs(["📍 Repetitive Defect Visualizer", "🏆 Top Offenders"])

# CHART 1: SCATTER PLOT (The "Deep Think" Tool)
# Visualizes CLUSTERS of failures.
with tab_scatter:
    st.markdown("**How to read this chart:** Look for **clusters of dots** horizontally. "
                "Multiple dots close together on the same line indicate a **Repetitive Defect** on that aircraft.")
    
    if not filtered_df.empty:
        fig_scatter = px.scatter(
            filtered_df,
            x="Date",
            y="Aircraft",
            color="ATA",
            size="FH", # Bigger dot = Later in life (Higher FH)
            hover_data=["Component", "Reason", "Part Number"],
            title="Timeline of Removal Events (Spot the Clusters)",
            height=400
        )
        # Add visual guides
        fig_scatter.update_traces(marker=dict(size=15, line=dict(width=2, color='DarkSlateGrey')))
        fig_scatter.update_layout(xaxis_title="Timeline", yaxis_title="Aircraft Registration")
        st.plotly_chart(fig_scatter, use_container_width=True)

# CHART 2: PARETO (Contextualized)
with tab_pareto:
    st.markdown("**Which systems are consuming the most maintenance resources?**")
    
    if not filtered_df.empty:
        # Group by Component AND ATA to give engineering context
        top_offenders = filtered_df.groupby(["Component", "ATA"]).size().reset_index(name="Count")
        top_offenders = top_offenders.sort_values("Count", ascending=False).head(10)
        
        fig_bar = px.bar(
            top_offenders, 
            x="Count", 
            y="Component", 
            color="ATA", # Color by ATA so you see if it's a "Hydraulic" vs "Electrical" issue
            orientation='h', 
            text="Count",
            title="Top 10 Unscheduled Removals"
        )
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)

render_footer()
