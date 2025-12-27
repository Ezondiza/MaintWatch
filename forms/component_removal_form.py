import streamlit as st
from datetime import date
from validation.component_rules import validate_removal_event
from utils.csv_writer import append_removal_event


def component_removal_form():
    st.subheader("Component Removal Entry")

    with st.form("component_removal_form"):
        st.markdown("### Mandatory Information")

        aircraft_reg = st.text_input("Aircraft Registration")
        component_name = st.text_input("Component Name")
        part_number = st.text_input("Part Number")
        serial_number = st.text_input("Serial Number")
        ata_chapter = st.text_input("ATA Chapter")

        removal_date = st.date_input("Removal Date", max_value=date.today())

        col1, col2 = st.columns(2)
        aircraft_fh = col1.number_input("Aircraft FH at Removal", min_value=0.0)
        aircraft_fc = col2.number_input("Aircraft FC at Removal", min_value=0)

        removal_reason = st.selectbox(
            "Removal Reason",
            [
                "Unscheduled Failure",
                "Scheduled Replacement",
                "Life Limit",
                "Inspection Finding",
                "SB or Modification"
            ]
        )

        st.markdown("### Optional Information")

        station = st.text_input("Station")
        deferred_ref = st.text_input("Deferred Reference")
        work_order = st.text_input("Work Order or Task Card")
        technician_id = st.text_input("Technician ID")
        remarks = st.text_area("Remarks")

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
