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
    Connects to a specific worksheet in the 'MaintWatch_Data' Google Sheet.
    Default worksheet is 'removal_events'.
    """
    try:
        # Check for credentials in Streamlit Secrets
        if "gcp_service_account" not in st.secrets:
            st.error("Missing 'gcp_service_account' in Streamlit Secrets.")
            return None

        # Authenticate using Service Account
        creds_dict = dict(st.secrets["gcp_service_account"])
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)
        client = gspread.authorize(creds)
        
        # Open the specific Google Sheet file
        sheet_file = client.open("MaintWatch_Data")
        
        # Try to open the specific worksheet
        try:
            return sheet_file.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            st.error(f"Worksheet '{worksheet_name}' not found. Please check your Google Sheet tabs.")
            return None
            
    except Exception as e:
        st.error(f"Failed to connect to Google Sheet: {e}")
        return None

def fetch_all_data(worksheet_name="removal_events"):
    """
    Reads all data from the Google Sheet and returns a Pandas DataFrame.
    Used by the Dashboard to pull live data.
    """
    sheet = connect_to_sheet(worksheet_name)
    if not sheet:
        return pd.DataFrame()

    try:
        # Get all records (returns a list of dictionaries)
        data = sheet.get_all_records()
        
        if not data:
            return pd.DataFrame()
            
        df = pd.DataFrame(data)
        return df
        
    except Exception as e:
        st.error(f"Error reading data from Google Sheet: {e}")
        return pd.DataFrame()

def write_data_to_sheet(data_dict, target_sheet):
    """
    Generic function to append a single dictionary row to a specific sheet.
    Handles 'aircraft_fleet', 'ata_chapters', and 'removal_events'.
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
        # --- CRITICAL: MUST MATCH GOOGLE SHEET COLUMN ORDER EXACTLY ---
        row_data = [
            data_dict.get("aircraft_reg"),
            data_dict.get("component_code"),
            data_dict.get("component_name"),
            data_dict.get("part_number"),
            data_dict.get("component_type"),   # New Column
            data_dict.get("serial_number"),
            data_dict.get("ata_chapter"),
            str(data_dict.get("removal_date")), # Ensure date is string
            data_dict.get("aircraft_fh", ""),
            data_dict.get("aircraft_fc", ""),
            data_dict.get("removal_type", ""),
            data_dict.get("removal_reason")
        ]
    else:
        st.error(f"Unknown target sheet: {target_sheet}")
        return False
    
    try:
        sheet.append_row(row_data)
        return True
    except Exception as e:
        st.error(f"Error saving to {target_sheet}: {e}")
        return False

def append_removal_event_gsheet(record):
    """
    Wrapper function for backward compatibility with the New Entry form.
    """
    return write_data_to_sheet(record, "removal_events")

def write_bulk_data(df):
    """
    Appends a PANDAS DATAFRAME to 'removal_events'.
    Used by Admin Tools (Dummy Data Generator).
    """
    sheet = connect_to_sheet("removal_events")
    if not sheet:
        return False

    try:
        df_export = df.copy()
        
        # Convert date objects to strings to avoid JSON errors
        for col in df_export.columns:
            if pd.api.types.is_datetime64_any_dtype(df_export[col]):
                df_export[col] = df_export[col].astype(str)
        
        # Replace NaN values with empty strings
        df_export = df_export.fillna("")
        
        # Convert DataFrame to list of lists
        data_to_upload = df_export.values.tolist()
        
        # Append all rows at once
        sheet.append_rows(data_to_upload)
        return True
    except Exception as e:
        st.error(f"Error writing bulk data: {e}")
        return False

def clear_worksheet_data(target_sheet="removal_events"):
    """
    Clears all data in a worksheet but KEEPS the header row (Row 1).
    Used by Admin Tools (Danger Zone).
    """
    sheet = connect_to_sheet(target_sheet)
    if not sheet:
        return False
        
    try:
        # Get all values to count rows
        all_values = sheet.get_all_values()
        row_count = len(all_values)
        
        if row_count > 1:
            # Clear from Row 2 down to the last row, across columns A to M
            range_to_clear = f"A2:M{row_count}"
            sheet.batch_clear([range_to_clear])
            return True
        else:
            # Sheet is already empty (only headers exist)
            return True
            
    except Exception as e:
        st.error(f"Error clearing sheet: {e}")
        return False
