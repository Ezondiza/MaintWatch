# /forms/component_removal_form.py

import streamlit as st
from datetime import date
from validation.component_rules import validate_removal_event
from utils.csv_writer import append_removal_event
from utils.component_master_loader import load_component_master


def component_removal_form():
    st.subheader("Component Removal Entry")

    components_df = load_component_master()

    component_map = {
        f"{row.component_code} | {row.component_name}": row
        for _, row in components_df.iterrows()
    }

    with st.form("component_removal_form"):

        col1, col2, col3 = st.columns(3)
        aircraft_reg = col1.text_input("Aircraft Reg")
        removal_date = col2.date_input("Removal Date", max_value=date.today())
        station = col3.text_input("Station")

        component_key = st.selectbox(
            "Component",
            options=list(component_map.keys())
        )

        selected = component_map[component_key]

        col4, col5, col6 = st.columns(3)
        component_code = col4.text_input(
            "Component Code",
            value=selected.component_code,
            disabled=True
        )
        ata_chapter = col5.text_input(
            "ATA Chapter",
            value=str(selected.ata_chapter),
            disabled=True
        )
        category = col6.text_input(
            "Category",
            value=selected.category,
            disabled=True
        )

        col7, col8, col9 = st.columns(3)
        part_number = col7.text_input("Part Number")
        serial_number = col8.text_input("Serial Number")
        criticality = col9.text_input(
            "Criticality",
            value=selected.criticality,
            disabled=True
        )

        col10, col11, col12 = st.columns(3)
        aircraft_fh = col10.number_input("Aircraft FH", min_value=0.0, step=0.1)
        aircraft_fc = col11.number_input("Aircraft FC", min_value=0, step=1)
        removal_reason = col12.selectbox(
            "Removal Reason",
            [
                "Unscheduled Failure",
                "Scheduled Replacement",
                "Life Limit",
                "Inspection Finding",
                "SB or Modification"
            ]
        )

        remarks = st.text_area("Remarks", height=80)

        submitted = st.form_submit_button("Save Removal Event")

    if submitted:
        record = {
            "aircraft_reg": aircraft_reg.strip(),
            "component_code": component_code,
            "component_name": selected.component_name,
            "part_number": part_number.strip(),
            "serial_number": serial_number.strip(),
            "ata_chapter": selected.ata_chapter,
            "category": selected.category,
            "criticality": selected.criticality,
            "removal_date": str(removal_date),
            "aircraft_fh": aircraft_fh,
            "aircraft_fc": aircraft_fc,
            "removal_reason": removal_reason,
            "station": station.strip(),
            "remarks": remarks.strip()
        }

        errors = validate_removal_event(record)

        if errors:
            for err in errors:
                st.error(err)
        else:
            append_removal_event(record)
            st.success("Component removal recorded successfully")
