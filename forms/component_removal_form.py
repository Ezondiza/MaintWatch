# /forms/component_removal_form.py

import streamlit as st
from datetime import date
from validation.component_rules import validate_removal_event
from utils.csv_writer import append_removal_event


def component_removal_form():
    st.subheader("Component Removal Entry")

    with st.form("component_removal_form"):

        st.markdown("Mandatory Information")

        col1, col2, col3 = st.columns(3)
        aircraft_reg = col1.text_input("Aircraft Reg")
        ata_chapter = col2.text_input("ATA")
        removal_date = col3.date_input(
            "Removal Date",
            max_value=date.today()
        )

        col4, col5, col6 = st.columns(3)
        component_name = col4.text_input("Component")
        part_number = col5.text_input("Part Number")
        serial_number = col6.text_input("Serial Number")

        col7, col8, col9 = st.columns(3)
        aircraft_fh = col7.number_input("Aircraft FH", min_value=0.0, step=0.1)
        aircraft_fc = col8.number_input("Aircraft FC", min_value=0, step=1)
        removal_reason = col9.selectbox(
            "Removal Reason",
            [
                "Unscheduled Failure",
                "Scheduled Replacement",
                "Life Limit",
                "Inspection Finding",
                "SB or Modification"
            ]
        )

        with st.expander("Optional Information"):
            col10, col11, col12 = st.columns(3)
            station = col10.text_input("Station")
            deferred_ref = col11.text_input("Deferred Ref")
            technician_id = col12.text_input("Technician ID")

            work_order = st.text_input("Work Order or Task Card")
            remarks = st.text_area("Remarks", height=80)

        submitted = st.form_submit_button("Save Removal Event")

    if submitted:
        record = {
            "aircraft_reg": aircraft_reg.strip(),
            "component_name": component_name.strip(),
            "part_number": part_number.strip(),
            "serial_number": serial_number.strip(),
            "ata_chapter": ata_chapter.strip(),
            "removal_date": str(removal_date),
            "aircraft_fh": aircraft_fh,
            "aircraft_fc": aircraft_fc,
            "removal_reason": removal_reason,
            "station": station.strip(),
            "deferred_ref": deferred_ref.strip(),
            "work_order": work_order.strip(),
            "technician_id": technician_id.strip(),
            "remarks": remarks.strip()
        }

        errors = validate_removal_event(record)

        if errors:
            for err in errors:
                st.error(err)
        else:
            append_removal_event(record)
            st.success("Component removal recorded successfully")
