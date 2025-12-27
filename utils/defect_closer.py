# utils/defect_closer.py

import pandas as pd
from datetime import date

DEFECT_PATH = "data/defect_log.csv"

def close_defect(aircraft_reg, ata_chapter):
    """
    Finds an OPEN defect matching the Aircraft and ATA, and closes it.
    """
    try:
        df = pd.read_csv(DEFECT_PATH)
    except FileNotFoundError:
        return

    if df.empty:
        return

    # Ensure we are matching strings to strings (handle potential type mismatches)
    ata_str = str(ata_chapter)
    
    # 1. Identify the row: Must be same Aircraft, same ATA, and currently Open
    # We use a 'mask' to filter the correct row
    mask = (df["aircraft_reg"] == aircraft_reg) & \
           (df["ata_chapter"].astype(str) == ata_str) & \
           (df["status"] == "Open")

    # 2. Check if we found a match
    if not df[mask].empty:
        # Update Status and Date for the matching row(s)
        df.loc[mask, "status"] = "Closed"
        df.loc[mask, "closure_date"] = date.today()
        
        # Save changes
        df.to_csv(DEFECT_PATH, index=False)
        print(f"Success: Closed defect for {aircraft_reg} ATA {ata_str}")
    else:
        print(f"Notice: No open defect found for {aircraft_reg} ATA {ata_str}")
