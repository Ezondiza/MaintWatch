import pandas as pd

def load_data():
    components = pd.read_csv("data/components.csv")
    technicians = pd.read_csv("data/ames.csv")  # Updated filename
    pilots = pd.read_csv("data/pilots.csv")
    return components, technicians, pilots

def load_maintenance(uploaded_file=None):
    if uploaded_file:
        return pd.read_csv(uploaded_file)
    return pd.read_csv("data/sample_maintenance.csv")

def merge_data(df, components, technicians, pilots):
    df = df.merge(components, left_on="component", right_on="component_name", how="left")
    df = df.merge(technicians, left_on="technician", right_on="technician_name", how="left")
    df = df.merge(pilots, left_on="pilot_name", right_on="pilot_name", how="left")
    return df

def detect_anomalies(df):
    df["z_score"] = (df["hours_since_last"] - df["hours_since_last"].mean()) / df["hours_since_last"].std()
    df["anomaly"] = df["z_score"].abs() > 2
    return df
