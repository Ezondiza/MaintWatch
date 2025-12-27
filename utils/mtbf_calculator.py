import pandas as pd

def calculate_mtbf_by_component(removal_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates MTBF (Mean Time Between Failures) per component_name.
    Assumes removal_df has multiple removals per component across aircraft.
    """
    # Sort by component and removal date
    removal_df["removal_date"] = pd.to_datetime(removal_df["removal_date"])
    df_sorted = removal_df.sort_values(["component_name", "aircraft_reg", "removal_date"])

    # Group by component and aircraft to compute deltas
    df_sorted["fh_delta"] = df_sorted.groupby(["component_name", "aircraft_reg"])["aircraft_fh_at_removal"].diff()
    df_sorted["fc_delta"] = df_sorted.groupby(["component_name", "aircraft_reg"])["aircraft_fc_at_removal"].diff()

    # Drop first occurrences (no prior removal to compare)
    df_valid = df_sorted.dropna(subset=["fh_delta", "fc_delta"])

    # Aggregate MTBF per component
    mtbf = df_valid.groupby("component_name").agg(
        mtbf_fh=("fh_delta", "mean"),
        mtbf_fc=("fc_delta", "mean"),
        removal_count=("component_name", "count")
    ).reset_index()

    mtbf["mtbf_fh"] = mtbf["mtbf_fh"].round(1)
    mtbf["mtbf_fc"] = mtbf["mtbf_fc"].round(1)

    return mtbf.sort_values("mtbf_fh", ascending=False)


def calculate_mtbf_by_ata(removal_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates MTBF per ATA chapter.
    """
    removal_df["removal_date"] = pd.to_datetime(removal_df["removal_date"])
    df_sorted = removal_df.sort_values(["ata_chapter", "aircraft_reg", "removal_date"])

    df_sorted["fh_delta"] = df_sorted.groupby(["ata_chapter", "aircraft_reg"])["aircraft_fh_at_removal"].diff()
    df_sorted["fc_delta"] = df_sorted.groupby(["ata_chapter", "aircraft_reg"])["aircraft_fc_at_removal"].diff()

    df_valid = df_sorted.dropna(subset=["fh_delta", "fc_delta"])

    mtbf = df_valid.groupby("ata_chapter").agg(
        mtbf_fh=("fh_delta", "mean"),
        mtbf_fc=("fc_delta", "mean"),
        removal_count=("ata_chapter", "count")
    ).reset_index()

    mtbf["mtbf_fh"] = mtbf["mtbf_fh"].round(1)
    mtbf["mtbf_fc"] = mtbf["mtbf_fc"].round(1)

    return mtbf.sort_values("mtbf_fh", ascending=False)
