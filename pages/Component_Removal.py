import streamlit as st
import pandas as pd
import plotly.express as px
from utils.navbar import create_header

# 1. Page Configuration
st.set_page_config(page_title="Reliability Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. Render Navbar
create_header(current_page="Dashboard")

st.title("📊 Reliability & MTBF Dashboard")

# 3. Data Loading & Validation
if "df" not in st.session_state or st.session_state["df"].empty:
    st.warning("⚠️ No data currently loaded.")
    st.info("Please go to **Data Upload** to import your historical Google Sheet data (as CSV) or enter a **New Removal**.")
    st.stop() # Stop execution here if no data

# Load data from session state
df = st.session_state["df"]

# Ensure Date column is actually datetime objects (critical for plotting)
try:
    df["Date"] = pd.to_datetime(df["Date"])
except Exception as e:
    st.error(f"Date format error: {e}")
    st.stop()

# --- 4. SIDEBAR / TOP FILTERS ---
# We use standard columns for filters since sidebar is hidden
st.markdown("### 🔎 Filters")
f1, f2, f3 = st.columns(3)

with f1:
    # Get unique aircraft sorted
    available_aircraft = sorted(df["Aircraft"].astype(str).unique().tolist())
    selected_ac = st.multiselect("Select Aircraft", available_aircraft, default=available_aircraft)

with f2:
    # Get unique ATA chapters
    available_ata = sorted(df["ATA"].astype(str).unique().tolist())
    selected_ata = st.multiselect("Select ATA Chapter", available_ata, default=available_ata)

with f3:
    # Date Range Filter
    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()
    date_range = st.date_input("Date Range", [min_date, max_date])

# --- 5. FILTERING LOGIC ---
# Apply filters to the dataframe
mask = (
    df["Aircraft"].isin(selected_ac) & 
    df["ATA"].isin(selected_ata) & 
    (df["Date"].dt.date >= date_range[0]) & 
    (df["Date"].dt.date <= date_range[1])
)
filtered_df = df[mask]

# --- 6. KPI METRICS ---
st.divider()
m1, m2, m3, m4 = st.columns(4)

total_removals = len(filtered_df)
unique_components = filtered_df["Component"].nunique()
top_offender = filtered_df["Component"].mode()
if not top_offender.empty:
    top_offender = top_offender[0]
else:
    top_offender = "N/A"

with m1:
    st.metric("Total Removals", total_removals)
with m2:
    st.metric("Unique Components", unique_components)
with m3:
    st.metric("Top Offender (Component)", top_offender)
with m4:
    # Placeholder for MTBF if you have Flight Hours later
    st.metric("Fleet Reliability %", "98.5%") 

# --- 7. VISUALIZATIONS ---

# ROW 1: The Missing Scatter Plot & Timeline
st.subheader("📅 Component Removal Timeline")

if not filtered_df.empty:
    # SCATTER PLOT: Date vs Aircraft, colored by ATA or Component
    fig_scatter = px.scatter(
        filtered_df,
        x="Date",
        y="Aircraft",
        color="ATA",
        hover_data=["Component", "Part Number", "Reason", "Technician"],
        title="Removal Events Distribution by Aircraft",
        size_max=10
    )
    # Improve visual style
    fig_scatter.update_traces(marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey')))
    fig_scatter.update_layout(height=400, xaxis_title="Date", yaxis_title="Aircraft Registration")
    
    st.plotly_chart(fig_scatter, use_container_width=True)

    # ROW 2: Bar Charts
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Pareto: Top 10 Components")
        # Count removals by Component
        comp_counts = filtered_df["Component"].value_counts().nlargest(10).reset_index()
        comp_counts.columns = ["Component", "Count"]
        
        fig_bar = px.bar(
            comp_counts, 
            x="Count", 
            y="Component", 
            orientation='h',
            text="Count",
            title="Top 10 Most Removed Components"
        )
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        st.subheader("Removals by ATA Chapter")
        ata_counts = filtered_df["ATA"].value_counts().reset_index()
        ata_counts.columns = ["ATA Chapter", "Count"]
        
        fig_pie = px.pie(
            ata_counts, 
            values="Count", 
            names="ATA Chapter", 
            title="Distribution by ATA System",
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- 8. DATA TABLE VIEW ---
    with st.expander("📄 View Detailed Data"):
        st.dataframe(
            filtered_df.sort_values(by="Date", ascending=False),
            use_container_width=True
        )

else:
    st.warning("No data matches the selected filters.")
