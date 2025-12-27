# /utils/component_master_loader.py

import pandas as pd

COMPONENTS_PATH = "data/components.csv"


def load_component_master():
    df = pd.read_csv(COMPONENTS_PATH)
    return df
