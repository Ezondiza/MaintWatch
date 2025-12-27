# /utils/mtbf_calculator.py

import pandas as pd


def calculate_mtbf_by_component(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df = df[df["removal_reason"] == "Unscheduled Failure"]
    if df.empty:
        return pd.DataFrame()

    df["removal_date"] = pd.to_datetime(df["removal_date"])

    df = df.sort_values(
        ["component_code", "serial_number", "aircraft_reg", "removal_date"]
    )

    df["fh_delta"] = df.groupby(
        ["component_code", "serial_number", "aircraft_reg"]
    )["aircraft_fh"].diff()

    valid = df.dropna(subset=["fh_delta"])
    if valid.empty:
        return pd.DataFrame()

    mtbf = (
        valid.groupby(
            ["component_code", "component_name", "category", "criticality"]
        )
        .agg(
            mtbf_fh=("fh_delta", "mean"),
            failure_count=("fh_delta", "count")
        )
        .reset_index()
    )

    mtbf["mtbf_fh"] = mtbf["mtbf_fh"].round(1)

    return mtbf.sort_values("mtbf_fh", ascending=False)


def calculate_mtbf_by_ata(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df = df[df["removal_reason"] == "Unscheduled Failure"]
    if df.empty:
        return pd.DataFrame()

    df["removal_date"] = pd.to_datetime(df["removal_date"])

    df = df.sort_values(
        ["ata_chapter", "serial_number", "aircraft_reg", "removal_date"]
    )

    df["fh_delta"] = df.groupby(
        ["ata_chapter", "serial_number", "aircraft_reg"]
    )["aircraft_fh"].diff()

    valid = df.dropna(subset=["fh_delta"])
    if valid.empty:
        return pd.DataFrame()

    mtbf = (
        valid.groupby("ata_chapter")
        .agg(
            mtbf_fh=("fh_delta", "mean"),
            failure_count=("fh_delta", "count")
        )
        .reset_index()
    )

    mtbf["mtbf_fh"] = mtbf["mtbf_fh"].round(1)

    return mtbf.sort_values("mtbf_fh", ascending=False)
