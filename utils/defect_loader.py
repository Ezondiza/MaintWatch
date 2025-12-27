import pandas as pd

DEFECT_PATH = "data/defect_log.csv"


def load_open_defects(aircraft_reg):
    if not aircraft_reg:
        return pd.DataFrame()

    df = pd.read_csv(DEFECT_PATH)

    if df.empty:
        return df

    df = df[df["status"] == "Open"]
    df = df[df["aircraft_reg"] == aircraft_reg]

    if df.empty:
        return df

    df["label"] = (
        df["defect_id"].astype(str)
        + " | ATA "
        + df["ata_chapter"].astype(str)
        + " | "
        + df["mel_reference"].fillna("NO MEL")
    )

    return df
