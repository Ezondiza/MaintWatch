# maintwatch/forms/component_removal_form.py

import streamlit as st
import pandas as pd
from datetime import date

from utils.component_master_loader import load_component_master
# Import from the new Google Sheet loader, but keep the name 'append_removal_event'
# so you don't have to change the rest of the code.
from utils.gsheet_loader import append_removal_event_gsheet as append_removal_event
from validation.component_rules import validate_removal_event
from utils.defect_closer import close_defect


def component_removal_form():

    st.subheader("Component Removal Entry")

    components_df = load_component_master()

    # Build component selection map
    component_map = {}
    for _, row in components_df.iterrows():
        label = f"{row['component_code']} | {row['component_name']}"
        component_map[label] = row

    with st.form("component_removal_form", clear_on_submit=True):

        col1, col2 = st.columns(2)

        with col1:
            aircraft_reg = st.selectbox(
                "Aircraft Registration",
                ["9N-AHB", "9N-AHR", "9N-AIE", "9N-AJH"]
            )

            component_label = st.selectbox(
                "Component",
                sorted(component_map.keys())
            )

            serial_number = st.text_input("Serial Number")
            part_number = st.text_input("Part Number")

            removal_date = st.date_input(
                "Removal Date",
                value=date.today()
            )

        with col2:
            aircraft_fh = st.number_input(
                "Aircraft FH at Removal",
                min_value=0.0,
                step=0.1
            )

            aircraft_fc = st.number_input(
                "Aircraft FC at Removal",
                min_value=0,
                step=1
            )

            removal_type = st.selectbox(
                "Removal Type",
                ["Unscheduled", "Scheduled"]
            )

            removal_reason = st.text_input("Removal Reason")

        selected_component = component_map[component_label]

        # Locked reference fields
        st.markdown("### Component Reference (Auto-filled)")
        ref1, ref2, ref3 = st.columns(3)

        ref1.text_input(
            "Component Code",
            selected_component["component_code"],
            disabled=True
        )

        ref2.text_input(
            "ATA Chapter",
            selected_component["ata_chapter"],
            disabled=True
        )

        ref3.text_input(
            "Category",
            selected_component["category"],
            disabled=True
        )

        submitted = st.form_submit_button("Save Removal Event")

        if submitted:

            event = {
                "aircraft_reg": aircraft_reg,
                "component_code": selected_component["component_code"],
                "component_name": selected_component["component_name"],
                "part_number": part_number,
                "serial_number": serial_number,
                "ata_chapter": selected_component["ata_chapter"],
                "removal_date": removal_date,
                "aircraft_fh": aircraft_fh,
                "aircraft_fc": aircraft_fc,
                "removal_type": removal_type,
                "removal_reason": removal_reason,
            }

            errors = validate_removal_event(event)

            if errors:
                for e in errors:
                    st.error(e)
                return

            append_removal_event(event)

            if removal_type == "Unscheduled":
                close_defect(aircraft_reg, selected_component["ata_chapter"])

            st.success("Component removal recorded successfully")
