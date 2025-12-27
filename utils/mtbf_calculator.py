import pandas as pd


def calculate_mtbf_by_component(removal_df: pd.DataFrame) -> pd.DataFrame:
    df = removal_df.copy()

    df["removal_date"] = pd.to_datetime(df["removal_date"])
    df = df[df["removal_reason"] == "Unscheduled Failure"]

    df = df.sort_values(
        ["component_name", "serial_number", "aircraft_reg", "removal_date"]
    )

    df["fh_delta"] = df.groupby(
        ["component_name", "serial_number", "aircraft_reg"]
    )["aircraft_fh"].diff()

    df_valid = df.dropna(subset=["fh_delta"])

    mtbf = df_valid.groupby("component_name").agg(
        mtbf_fh=("fh_delta", "mean"),
        failure_count=("component_name", "count")
    ).reset_index()

    mtbf["mtbf_fh"] = mtbf["mtbf_fh"].round(1)

    return mtbf.sort_values("mtbf_fh", ascending=False)


def calculate_mtbf_by_ata(removal_df: pd.DataFrame) -> pd.DataFrame:
    df = removal_df.copy()

    df["removal_date"] = pd.to_datetime(df["removal_date"])
    df = df[df["removal_reason"] == "Unscheduled Failure"]

    df = df.sort_values(
        ["ata_chapter", "serial_number", "aircraft_reg", "removal_date"]
    )

    df["fh_delta"] = df.groupby(
        ["ata_chapter", "serial_number", "aircraft_reg"]
    )["aircraft_fh"].diff()

    df_valid = df.dropna(subset=["fh_delta"])

    mtbf = df_valid.groupby("ata_chapter").agg(
        mtbf_fh=("fh_delta", "mean"),
        failure_count=("ata_chapter", "count")
    ).reset_index()

    mtbf["mtbf_fh"] = mtbf["mtbf_fh"].round(1)

    return mtbf.sort_values("mtbf_fh", ascending=False)
