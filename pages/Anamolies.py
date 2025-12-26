import streamlit as st
import altair as alt
import pandas as pd

# Load from session
if "df" not in st.session_state:
    st.warning("Please upload or load data from the Home page.")
    st.stop()

df = st.session_state["df"]

st.title("Anomaly Explorer")

# Sidebar filters
st.sidebar.header("Filter Data")
aircraft_filter = st.sidebar.multiselect("Aircraft ID", sorted(df["aircraft_id"].dropna().unique()), default=df["aircraft_id"].dropna().unique())
component_filter = st.sidebar.multiselect("Component", sorted(df["component"].dropna().unique()), default=df["component"].dropna().unique())
technician_filter = st.sidebar.multiselect("Technician", sorted(df["technician"].dropna().unique()), default=df["technician"].dropna().unique())
pilot_filter = st.sidebar.multiselect("Pilot", sorted(df["pilot_name"].dropna().unique()), default=df["pilot_name"].dropna().unique())
ata_filter = st.sidebar.multiselect("ATA Chapter", sorted(df["ata_chapter"].dropna().unique()), default=df["ata_chapter"].dropna().unique())

# Apply filters
filtered_df = df[
    df["aircraft_id"].isin(aircraft_filter) &
    df["component"].isin(component_filter) &
    df["technician"].isin(technician_filter) &
    df["pilot_name"].isin(pilot_filter) &
    df["ata_chapter"].isin(ata_filter)
]

st.subheader("Filtered Maintenance Records")
st.dataframe(filtered_df)

# Show flagged anomalies
anomalies = filtered_df[filtered_df["anomaly"]]
st.subheader("Flagged Anomalies")
st.dataframe(anomalies)

# Altair chart
st.subheader("Anomaly Timeline")
chart = alt.Chart(filtered_df).mark_circle(size=80).encode(
    x="date:T",
    y="hours_since_last:Q",
    color=alt.condition(
        alt.datum.anomaly == True,
        alt.value("red"),
        alt.value("steelblue")
    ),
    tooltip=["aircraft_id", "component", "technician", "pilot_name", "criticality", "remarks"]
).properties(height=400)

st.altair_chart(chart, use_container_width=True)

# Download anomalies
st.download_button(
    label="Download Anomalies CSV",
    data=anomalies.to_csv(index=False),
    file_name="flagged_anomalies.csv",
    mime="text/csv"
)
