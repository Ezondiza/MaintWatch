import pandas as pd

DEFECT_PATH = "data/defect_log.csv"


def close_defect(defect_id, closure_date):
    try:
        df = pd.read_csv(DEFECT_PATH)
    except FileNotFoundError:
        return

    if df.empty:
        return

    if "defect_id" not in df.columns:
        return

    df.loc[df["defect_id"] == defect_id, "status"] = "Closed"
    df.loc[df["defect_id"] == defect_id, "closure_date"] = closure_date

    df.to_csv(DEFECT_PATH, index=False)
