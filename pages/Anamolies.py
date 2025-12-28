# pages/Anamolies.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.gsheet_loader import connect_to_sheet

st.set_page_config(page_title="Anomaly Detection", layout="wide")
st.title("🚨 Component Anomaly Detection")
st.markdown("Automatic detection of components failing significantly earlier than their fleet average.")

def load_data():
    """Fetches live data from Google Sheets."""
    try:
        sheet = connect_to_sheet()
        if not sheet:
            return pd.DataFrame()
            
        data = sheet.get_all_records()
        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)
        
        # Convert 'aircraft_fh' to numeric, handling any text errors
        df['aircraft_fh'] = pd.to_numeric(df['aircraft_fh'], errors='coerce')
        
        # Ensure we only look at Unscheduled removals for anomaly detection
        # (Scheduled removals are planned, so they aren't failures)
        if 'removal_type' in df.columns:
            df = df[df['removal_type'] == 'Unscheduled']
            
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# 1. Load Data
df = load_data()

if df.empty:
    st.info("👋 No unscheduled removal data found in Google Sheets yet.")
    st.stop()

# 2. Sidebar Filters (Updated for new columns)
st.sidebar.header("Filter Data")
selected_aircraft = st.sidebar.multiselect(
    "Aircraft Registration", 
    options=df["aircraft_reg"].unique(),
    default=df["aircraft_reg"].unique()
)
selected_ata = st.sidebar.multiselect(
    "ATA Chapter",
    options=df["ata_chapter"].unique(),
    default=df["ata_chapter"].unique()
)

# Apply Filters
filtered_df = df[
    (df["aircraft_reg"].isin(selected_aircraft)) &
    (df["ata_chapter"].isin(selected_ata))
]

# 3. The Logic: Find Premature Failures
# We group by 'component_name' to find the average life of each type of part.
if not filtered_df.empty:
    stats = filtered_df.groupby("component_name")['aircraft_fh'].agg(['mean', 'std', 'count']).reset_index()

    # We need at least 2 data points to calculate a standard deviation
    valid_components = stats[stats['count'] >= 2] 

    if valid_components.empty:
        st.warning("ℹ️ Not enough data to detect anomalies yet. You need at least 2 removals of the same component.")
        st.subheader("Current Data Log")
        st.dataframe(filtered_df)
    else:
        # Merge stats back to the main list
        df_analysis = pd.merge(filtered_df, stats, on="component_name")

        # Define "Anomaly": Failing earlier than (Mean - 1.5 Standard Deviations)
        # The .replace(0, 1) prevents division by zero if all parts last exactly the same amount
        df_analysis['z_score'] = (df_analysis['aircraft_fh'] - df_analysis['mean']) / df_analysis['std'].replace(0, 1)
        
        # We look for z_score < -1.5 (Bottom 7% of performers)
        anomalies = df_analysis[df_analysis['z_score'] < -1.5]

        # 4. Display Results
        st.divider()
        if not anomalies.empty:
            st.error(f"🚨 Found {len(anomalies)} Premature Failures")
            
            for index, row in anomalies.iterrows():
                with st.expander(f"⚠️ {row['component_name']} on {row['aircraft_reg']} (ATA {row['ata_chapter']})", expanded=True):
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Failed At", f"{row['aircraft_fh']} FH")
                    c2.metric("Fleet Average", f"{row['mean']:.1f} FH")
                    c3.metric("Deficit", f"{row['aircraft_fh'] - row['mean']:.1f} FH", delta_color="inverse")
                    st.caption(f"Reason: {row['removal_reason']}")
        else:
            st.success("✅ No anomalies detected. All components are performing within normal limits.")

        # 5. Visualizing the Fleet
        st.subheader("Fleet Reliability Overview")
        fig = px.scatter(
            filtered_df, 
            x="aircraft_fh", 
            y="component_name", 
            color="aircraft_reg",
            size="aircraft_fh",
            hover_data=["removal_reason", "removal_date"],
            title="Component Life Distribution (Flight Hours)"
        )
        st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data matches your filters.")
