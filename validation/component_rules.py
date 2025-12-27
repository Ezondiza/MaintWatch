# /validation/component_rules.py

def validate_removal_event(record):
    errors = []

    required_fields = [
        "aircraft_reg",
        "component_name",
        "part_number",
        "serial_number",
        "ata_chapter",
        "removal_date",
        "aircraft_fh",
        "aircraft_fc",
        "removal_reason"
    ]

    for field in required_fields:
        if not record.get(field):
            errors.append(f"{field} is required")

    if record.get("aircraft_fh", 0) <= 0:
        errors.append("Aircraft FH must be greater than zero")

    if record.get("aircraft_fc", -1) < 0:
        errors.append("Aircraft FC must be zero or greater")

    ata = str(record.get("ata_chapter", ""))
    if not ata.replace("-", "").isdigit():
        errors.append("ATA chapter format is invalid")

    return errors
