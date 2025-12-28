# utils/gsheet_loader.py
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def connect_to_sheet():
    # 👇 THIS IS SAFE: It asks Streamlit for the password, it doesn't store it here.
    creds_dict = st.secrets["gcp_service_account"]
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
    client = gspread.authorize(creds)
    return client.open("MaintWatch_Data").worksheet("removal_events")
