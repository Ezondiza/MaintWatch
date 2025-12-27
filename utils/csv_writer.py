# /utils/csv_writer.py

import csv
import os

CSV_PATH = "data/removal_events.csv"

FIELDNAMES = [
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
    "remarks"
]

def append_removal_event(record):
    file_exists = os.path.isfile(CSV_PATH)

    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(record)
