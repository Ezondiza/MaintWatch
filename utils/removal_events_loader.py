# /utils/removal_events_loader.py

import pandas as pd
import os

CSV_PATH = "data/removal_events.csv"


def load_removal_events():
    if not os.path.isfile(CSV_PATH):
        return pd.DataFrame()

    df = pd.read_csv(CSV_PATH)

    if "removal_date" in df.columns:
        df["removal_date"] = pd.to_datetime(df["removal_date"], errors="coerce")

    return df
