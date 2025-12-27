# /utils/mtbf_calculator.py

import pandas as pd


def calculate_mtbf_by_component(df):
    df = df[df["removal_reason"] == "Unscheduled Failure"].copy()
    df["removal_date"] = pd.to_datetime(df["removal_date"])

    df = df.sort_values(
        ["component_name", "serial_number", "aircraft_reg", "removal_date"]
    )

    df["fh_delta"] = df.groupby(
        ["component_name", "serial_number", "aircraft_reg"]
    )["aircraft_fh"].diff()

    valid = df.dropna(subset=["fh_delta"])

    return (
        valid.groupby("component_name")
        .agg(mtbf_fh=("fh_delta", "mean"), failures=("component_name", "count"))
        .reset_index()
        .round(1)
    )

def calculate_mtbf_by_ata(df):
    import pandas as pd

    df = df[df["removal_reason"] == "Unscheduled Failure"].copy()
    df["removal_date"] = pd.to_datetime(df["removal_date"])

    df = df.sort_values(
        ["ata_chapter", "serial_number", "aircraft_reg", "removal_date"]
    )

    df["fh_delta"] = df.groupby(
        ["ata_chapter", "serial_number", "aircraft_reg"]
    )["aircraft_fh"].diff()

    valid = df.dropna(subset=["fh_delta"])

    return (
        valid.groupby("ata_chapter")
        .agg(mtbf_fh=("fh_delta", "mean"), failure_count=("ata_chapter", "count"))
        .reset_index()
        .round(1)
        .sort_values("mtbf_fh", ascending=False)
    )
