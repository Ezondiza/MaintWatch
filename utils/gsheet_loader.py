# utils/gsheet_loader.py
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
