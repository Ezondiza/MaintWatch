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
    st.info("Please go to **Data Upload** to import your CSV, or **Admin Tools** to generate test data.")
    render_footer()
    st.stop()

df = st.session_state["df"]

# 3. NORMALIZE COLUMNS (The Fix for Date Error)
# We create a map to standardize whatever columns come in (CSV vs Google Sheet)
# Your Google Sheet uses: 'removal_date', 'aircraft_reg', 'ata_chapter'
column_map = {
    "removal_date": "Date",
    "Date of Removal": "Date",
    "aircraft_reg": "Aircraft",
    "Registration": "Aircraft",
    "ata_chapter": "ATA",
    "ATA Chapter": "ATA",
    "component_name": "Component",
    "Component Name": "Component",
    "removal_reason": "Reason"
}
df = df.rename(columns=column_map)

# 4. CONVERT DATE (Robust)
try:
    df["Date"] = pd.to_datetime(df["Date"])
except Exception as e:
    st.error(f"Error: 'Date' column is not in a recognizable format. Debug info: {e}")
    st.write("First few rows of raw data:", df.head())
    st.stop()

# 5. FILTERS
st.markdown("### 🔎 Filters")
f1, f2, f3 = st.columns(3)

# Filter: Aircraft
with f1:
    if "Aircraft" in df.columns:
        avail_ac = sorted(df["Aircraft"].astype(str).unique())
        sel_ac = st.multiselect("Aircraft", avail_ac, default=avail_ac)
    else:
        sel_ac = []

# Filter: ATA
with f2:
    if "ATA" in df.columns:
        avail_ata = sorted(df["ATA"].astype(str).unique())
        sel_ata = st.multiselect("ATA Chapter", avail_ata, default=avail_ata)
    else:
        sel_ata = []

# Filter: Date
with f3:
    if not df.empty and "Date" in df.columns:
        min_d = df["Date"].min().date()
        max_d = df["Date"].max().date()
        sel_date = st.date_input("Date Range", [min_d, max_d])
    else:
        sel_date = [pd.Timestamp.today(), pd.Timestamp.today()]

# 6. APPLY FILTERS
if "Aircraft" in df.columns and "ATA" in df.columns:
    mask = (df["Aircraft"].isin(sel_ac)) & (df["ATA"].isin(sel_ata))
    
    # Handle Date Filter safely
    if len(sel_date) == 2:
        mask = mask & (df["Date"].dt.date >= sel_date[0]) & (df["Date"].dt.date <= sel_date[1])
        
    filtered_df = df[mask]
else:
    filtered_df = df

# 7. CHARTS
if not filtered_df.empty:
    st.divider()
    
    k1, k2, k3 = st.columns(3)
    k1.metric("Total Removals", len(filtered_df))
    if "Component" in filtered_df.columns:
        k2.metric("Unique Components", filtered_df["Component"].nunique())
    if "ATA" in filtered_df.columns:
        k3.metric("Most Frequent ATA", filtered_df["ATA"].mode()[0] if not filtered_df["ATA"].empty else "N/A")

    st.subheader("📅 Component Removal Timeline")
    
    if "Aircraft" in filtered_df.columns:
        fig = px.scatter(
            filtered_df,
            x="Date",
            y="Aircraft",
            color="ATA" if "ATA" in filtered_df.columns else None,
            hover_data=["Component", "Reason"] if "Component" in filtered_df.columns else None,
            title="Removal Events by Date",
            size_max=15
        )
        fig.update_traces(marker=dict(size=14, line=dict(width=1, color='DarkSlateGrey')))
        st.plotly_chart(fig, use_container_width=True)

    # Bar Chart
    if "Component" in filtered_df.columns:
        st.subheader("🏆 Top Offending Components")
        top_comp = filtered_df["Component"].value_counts().nlargest(10).reset_index()
        top_comp.columns = ["Component", "Count"]
        
        fig_bar = px.bar(top_comp, x="Count", y="Component", orientation='h', text="Count")
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)

else:
    st.info("No records match the selected filters.")

render_footer()
