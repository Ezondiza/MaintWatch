import streamlit as st
from datetime import date

from utils.component_master_loader import load_component_master
from utils.defect_loader import load_open_defects
from utils.csv_writer import append_removal_event
from utils.defect_closer import close_defect
from validation.component_rules import validate_removal_event


def component_removal_form():

    st.subheader("Component Removal Entry")

    components_df = load_component_master()

    component_map = {}
    for _, row in components_df.iterrows():
        key = f"{row['component_code']} | {row['component_name']}"
        component_map[key] = row

    with st.form("component_removal_form", clear_on_submit=True):

        col1, col2, col3 = st.columns(3)
        aircraft_reg = col1.selectbox(
            "Aircraft Registration",
            ["", "9N-AHB", "9N-AHR", "9N-AIE", "9N-AJH"]
        )

        removal_date = col2.date_input(
            "Removal Date",
            max_value=date.today()
        )

        station = col3.text_input("Station")

        component_key = st.selectbox(
            "Component",
            options=[""] + list(component_map.keys())
        )

        selected = component_map.get(component_key)

        col4, col5, col6, col7 = st.columns(4)

        component_code = col4.text_input(
            "Component Code",
            value=selected["component_code"] if selected is not None else "",
            disabled=True
        )

        ata_chapter = col5.text_input(
            "ATA Chapter",
            value=str(selected["ata_chapter"]) if selected is not None else "",
            disabled=True
        )

        category = col6.text_input(
            "Category",
            value=selected["category"] if selected is not None else "",
            disabled=True
        )

        criticality = col7.text_input(
            "Criticality",
            value=selected["criticality"] if selected is not None else "",
            disabled=True
        )

        col8, col9, col10 = st.columns(3)
        part_number = col8.text_input("Part Number")
        serial_number = col9.text_input("Serial Number")

        removal_reason = col10.selectbox(
            "Removal Reason",
            [
                "Unscheduled Failure",
                "Scheduled Replacement",
                "Life Limit",
                "Inspection Finding",
                "SB or Modification"
            ]
        )

        col11, col12 = st.columns(2)
        aircraft_fh = col11.number_input("Aircraft FH", min_value=0.0, step=0.1)
        aircraft_fc = col12.number_input("Aircraft FC", min_value=0, step=1)

        deferred_ref = ""

        if aircraft_reg:
            open_defects = load_open_defects(aircraft_reg)
            if not open_defects.empty:
                labels = [""] + open_defects["label"].tolist()
                selected_label = st.selectbox(
                    "Deferred Defect Reference (optional)",
                    labels
                )
                if selected_label:
                    deferred_ref = selected_label.split(" | ")[0]

        remarks = st.text_area("Remarks", height=80)

        submitted = st.form_submit_button("Save Removal Event")

    if not submitted:
        return

    record = {
        "aircraft_reg": aircraft_reg,
        "component_code": component_code,
        "component_name": selected["component_name"] if selected is not None else "",
        "part_number": part_number.strip(),
        "serial_number": serial_number.strip(),
        "ata_chapter": selected["ata_chapter"] if selected is not None else "",
        "category": selected["category"] if selected is not None else "",
        "criticality": selected["criticality"] if selected is not None else "",
        "removal_date": str(removal_date),
        "aircraft_fh": aircraft_fh,
        "aircraft_fc": aircraft_fc,
        "removal_reason": removal_reason,
        "station": station.strip(),
        "deferred_ref": deferred_ref,
        "remarks": remarks.strip()
    }

    errors = validate_removal_event(record)

    if errors:
        for e in errors:
            st.error(e)
        return

    append_removal_event(record)

    if deferred_ref:
        close_defect(deferred_ref, str(removal_date))

    st.success("Component removal recorded successfully")
