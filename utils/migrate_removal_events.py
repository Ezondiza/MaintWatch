# /utils/migrate_removal_events.py

import pandas as pd

REMOVALS_PATH = "data/removal_events.csv"
COMPONENTS_PATH = "data/components.csv"


def migrate_removal_events():
    removals = pd.read_csv(REMOVALS_PATH)
    components = pd.read_csv(COMPONENTS_PATH)

    # Normalize for matching
    removals["component_name_norm"] = removals["component_name"].str.strip().str.lower()
    components["component_name_norm"] = components["component_name"].str.strip().str.lower()

    merged = removals.merge(
        components[
            [
                "component_code",
                "component_name_norm",
                "category",
                "criticality",
                "ata_chapter"
            ]
        ],
        left_on=["component_name_norm", "ata_chapter"],
        right_on=["component_name_norm", "ata_chapter"],
        how="left"
    )

    missing = merged["component_code"].isna().sum()
    if missing > 0:
        print(f"WARNING: {missing} rows could not be mapped to component master")

    # Drop helper column
    merged.drop(columns=["component_name_norm"], inplace=True)

    # Reorder columns
    ordered_cols = [
        "aircraft_reg",
        "component_code",
        "component_name",
        "part_number",
        "serial_number",
        "ata_chapter",
        "category",
        "criticality",
        "removal_date",
        "aircraft_fh",
        "aircraft_fc",
        "removal_reason",
        "station",
        "deferred_ref",
        "work_order",
        "technician_id",
        "remarks",
    ]

    final_cols = [c for c in ordered_cols if c in merged.columns]
    merged = merged[final_cols]

    merged.to_csv(REMOVALS_PATH, index=False)
    print("Migration complete. removal_events.csv updated.")
