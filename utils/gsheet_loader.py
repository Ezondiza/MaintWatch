import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def connect_to_sheet():
    try:
        creds_dict = st.secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)
        client = gspread.authorize(creds)
        sheet = client.open("MaintWatch_Data").worksheet("removal_events")
        return sheet
    except Exception as e:
        st.error(f"Failed to connect to Google Sheet: {e}")
        return None

def append_removal_event_gsheet(record):
    """
    Appends a dictionary to Google Sheets.
    """
    sheet = connect_to_sheet()
    if not sheet:
        return False

    # Convert the dictionary (record) into a list of values
    # The order MUST match the columns in your Google Sheet
    row_data = [
        record.get("aircraft_reg"),
        record.get("component_code"),
        record.get("component_name"),
        record.get("part_number"),
        record.get("serial_number"),
        record.get("ata_chapter"),
        str(record.get("removal_date")),  # Dates must be strings
        record.get("aircraft_fh"),
        record.get("aircraft_fc"),
        record.get("removal_type"),
        record.get("removal_reason")
    ]
    
    try:
        sheet.append_row(row_data)
        return True
    except Exception as e:
        st.error(f"Error saving to Google Sheet: {e}")
        return False
