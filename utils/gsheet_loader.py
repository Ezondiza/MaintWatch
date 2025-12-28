import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def connect_to_sheet():
    """
    Connects to the 'MaintWatch_Data' Google Sheet.
    """
    try:
        # Check if secrets exist
        if "gcp_service_account" not in st.secrets:
            st.error("Missing 'gcp_service_account' in Streamlit Secrets.")
            return None

        creds_dict = dict(st.secrets["gcp_service_account"])
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)
        client = gspread.authorize(creds)
        
        # Open the specific file
        sheet_file = client.open("MaintWatch_Data")
        
        # Try to open the specific worksheet, fallback to the first one if missing
        try:
            return sheet_file.worksheet("removal_events")
        except gspread.WorksheetNotFound:
            # If 'removal_events' tab doesn't exist, use the first tab (default)
            return sheet_file.sheet1
            
    except Exception as e:
        st.error(f"Failed to connect to Google Sheet: {e}")
        return None

def append_removal_event_gsheet(record):
    """
    Appends a SINGLE dictionary record (used by New Entry form).
    """
    sheet = connect_to_sheet()
    if not sheet:
        return False

    # Ensure this order matches your Google Sheet columns exactly!
    row_data = [
        record.get("aircraft_reg"),
        record.get("component_code"),
        record.get("component_name"),
        record.get("part_number"),
        record.get("serial_number"),
        record.get("ata_chapter"),
        str(record.get("removal_date")),  # Dates must be strings
        record.get("aircraft_fh", ""),
        record.get("aircraft_fc", ""),
        record.get("removal_type", ""),
        record.get("removal_reason")
    ]
    
    try:
        sheet.append_row(row_data)
        return True
    except Exception as e:
        st.error(f"Error saving to Google Sheet: {e}")
        return False

def write_bulk_data(df):
    """
    Appends a PANDAS DATAFRAME (used by Admin Tools / Dummy Generator).
    """
    sheet = connect_to_sheet()
    if not sheet:
        return False

    try:
        # Prepare DataFrame: Convert dates to strings and fill NaNs
        df_export = df.copy()
        
        # Convert date columns to string if they exist
        for col in df_export.columns:
            if pd.api.types.is_datetime64_any_dtype(df_export[col]):
                df_export[col] = df_export[col].astype(str)
        
        df_export = df_export.fillna("")
        
        # Convert to list of lists for gspread
        data_to_upload = df_export.values.tolist()
        
        # Append all rows at once
        sheet.append_rows(data_to_upload)
        return True
    except Exception as e:
        st.error(f"Error writing bulk data: {e}")
        return False
