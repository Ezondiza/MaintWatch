import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def connect_to_sheet(worksheet_name="removal_events"):
    """
    Connects to a specific worksheet in 'MaintWatch_Data'.
    """
    try:
        if "gcp_service_account" not in st.secrets:
            st.error("Missing 'gcp_service_account' in Streamlit Secrets.")
            return None

        creds_dict = dict(st.secrets["gcp_service_account"])
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)
        client = gspread.authorize(creds)
        
        sheet_file = client.open("MaintWatch_Data")
        
        try:
            return sheet_file.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            st.error(f"Worksheet '{worksheet_name}' not found in Google Sheet.")
            return None
            
    except Exception as e:
        st.error(f"Failed to connect to Google Sheet: {e}")
        return None

def write_data_to_sheet(data_dict, target_sheet):
    """
    Generic function to append a dictionary row to any sheet.
    """
    sheet = connect_to_sheet(target_sheet)
    if not sheet:
        return False

    # Define column order based on the target sheet
    if target_sheet == "aircraft_fleet":
        row_data = [
            data_dict.get("Registration"),
            data_dict.get("MSN"),
            data_dict.get("FH"),
            data_dict.get("FC")
        ]
    elif target_sheet == "ata_chapters":
        row_data = [
            data_dict.get("Chapter"),
            data_dict.get("Description")
        ]
    elif target_sheet == "removal_events":
        # Matches the new schema with Component Type
        row_data = [
            data_dict.get("aircraft_reg"),
            data_dict.get("component_code"),
            data_dict.get("component_name"),
            data_dict.get("part_number"),
            data_dict.get("component_type"), # New Column
            data_dict.get("serial_number"),
            data_dict.get("ata_chapter"),
            str(data_dict.get("removal_date")),
            data_dict.get("aircraft_fh", ""),
            data_dict.get("aircraft_fc", ""),
            data_dict.get("removal_type", ""),
            data_dict.get("removal_reason")
        ]
    else:
        st.error("Unknown target sheet.")
        return False
    
    try:
        sheet.append_row(row_data)
        return True
    except Exception as e:
        st.error(f"Error saving to {target_sheet}: {e}")
        return False

def append_removal_event_gsheet(record):
    """Wrapper for backward compatibility with older pages."""
    return write_data_to_sheet(record, "removal_events")

def write_bulk_data(df):
    """
    Appends a PANDAS DATAFRAME (for Dummy Data).
    """
    sheet = connect_to_sheet("removal_events")
    if not sheet:
        return False

    try:
        df_export = df.copy()
        # Convert dates to strings
        for col in df_export.columns:
            if pd.api.types.is_datetime64_any_dtype(df_export[col]):
                df_export[col] = df_export[col].astype(str)
        
        df_export = df_export.fillna("")
        data_to_upload = df_export.values.tolist()
        sheet.append_rows(data_to_upload)
        return True
    except Exception as e:
        st.error(f"Error writing bulk data: {e}")
        return False

def clear_worksheet_data(target_sheet="removal_events"):
    """
    Clears all data in a worksheet but KEEPS the header row (Row 1).
    """
    sheet = connect_to_sheet(target_sheet)
    if not sheet:
        return False
        
    try:
        all_values = sheet.get_all_values()
        row_count = len(all_values)
        
        if row_count > 1:
            range_to_clear = f"A2:M{row_count}"
            sheet.batch_clear([range_to_clear])
            return True
        else:
            return True
            
    except Exception as e:
        st.error(f"Error clearing sheet: {e}")
        return False
