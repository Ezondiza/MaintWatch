# /utils/forecasting.py

import pandas as pd


def forecast_expected_failures(mtbf_df: pd.DataFrame, fleet_hours: float) -> pd.DataFrame:
    if mtbf_df.empty or fleet_hours <= 0:
        return pd.DataFrame()

    df = mtbf_df.copy()
    df = df[df["mtbf_fh"] > 0].copy()

    df["expected_failures"] = fleet_hours / df["mtbf_fh"]
    df["expected_failures"] = df["expected_failures"].round(2)

    return df.sort_values("expected_failures", ascending=False)
