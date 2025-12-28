import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from utils.navbar import create_header
from utils.footer import render_footer

# 1. Page Config
st.set_page_config(page_title="Dashboard", layout="wide", initial_sidebar_state="collapsed")
create_header(current_page="Dashboard")

st.title("📊 Reliability & MTBF Dashboard")

# --- HELPER: GENERATE DEMO DATA (For testing when no CSV is loaded) ---
def load_demo_data():
    dates = pd.date_range(start="2024-01-01", periods=20)
    data = {
        "Date": dates,
        "Aircraft": np.random.choice(["9N-AHA", "9N-AHB", "9N-AIC"], 20),
        "ATA": np.random.choice(["32", "24", "21", "73"], 20),
        "Component": np.random.choice(["Main Wheel", "Starter Gen", "Brake Unit"], 20),
        "Reason": ["Wear", "Leaking", "Vibration", "Electrical Fault"] * 5
    }
    return pd.DataFrame(data)

# 2. CHECK FOR DATA
if "df" not in st.session_state or st.session_state["df"].empty:
    st.warning("⚠️ No data loaded.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("Option 1: Go to 'Data Upload' to import your CSV file.")
    with col2:
        # ADDED: Button to load fake data so you can see the plots working!
        if st.button("🔄 Load Demo Data (Test Mode)"):
            st.session_state["df"] = load_demo_data()
            st.rerun()
    st.stop()

# 3. PREPARE DATA
df = st.session_state["df"]

# Ensure columns exist (Auto-fix names)
column_map = {"Aircraft Registration": "Aircraft", "ATA Chapter": "ATA", "Date of Removal": "Date"}
df = df.rename(columns=column_map)

# Convert Date
try:
    df["Date"] = pd.to_datetime(df["Date"])
except:
    st.error("Error: 'Date' column is not in a recognizable format.")
    st.stop()

# 4. FILTERS
st.markdown("### 🔎 Filters")
f1, f2, f3 = st.columns(3)
with f1:
    avail_ac = sorted(df["Aircraft"].astype(str).unique())
    sel_ac = st.multiselect("Aircraft", avail_ac, default=avail_ac)
with f2:
    avail_ata = sorted(df["ATA"].astype(str).unique())
    sel_ata = st.multiselect("ATA Chapter", avail_ata, default=avail_ata)
with f3:
    if not df.empty:
        min_d, max_d = df["Date"].min().date(), df["Date"].max().date()
        sel_date = st.date_input("Date Range", [min_d, max_d])
    else:
        sel_date = [pd.Timestamp.today(), pd.Timestamp.today()]

# Apply Filters
mask = (df["Aircraft"].isin(sel_ac)) & (df["ATA"].isin(sel_ata))
# Handle date filtering safely
if len(sel_date) == 2:
    mask = mask & (df["Date"].dt.date >= sel_date[0]) & (df["Date"].dt.date <= sel_date[1])

filtered_df = df[mask]

# 5. CHARTS (The Scatter Plot is back!)
if not filtered_df.empty:
    st.divider()
    
    # KPI Row
    k1, k2, k3 = st.columns(3)
    k1.metric("Total Removals", len(filtered_df))
    k2.metric("Unique Components", filtered_df["Component"].nunique())
    k3.metric("Most Frequent ATA", filtered_df["ATA"].mode()[0] if not filtered_df["ATA"].empty else "N/A")

    st.subheader("📅 Component Removal Timeline")
    
    # SCATTER PLOT
    fig = px.scatter(
        filtered_df,
        x="Date",
        y="Aircraft",
        color="ATA",
        hover_data=["Component", "Reason"],
        title="Removal Events by Date",
        size_max=15
    )
    fig.update_traces(marker=dict(size=15, line=dict(width=1, color='DarkSlateGrey')))
    st.plotly_chart(fig, use_container_width=True)

    # BAR CHART
    st.subheader("🏆 Top Offending Components")
    top_comp = filtered_df["Component"].value_counts().nlargest(10).reset_index()
    top_comp.columns = ["Component", "Count"]
    
    fig_bar = px.bar(top_comp, x="Count", y="Component", orientation='h', text="Count")
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_bar, use_container_width=True)

else:
    st.info("No records match the selected filters.")
    render_footer()
