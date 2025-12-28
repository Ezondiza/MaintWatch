# pages/Connection_Test.py
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

st.title("🔌 Google Sheet Connection Test")

# 1. Check Secrets
if "gcp_service_account" in st.secrets:
    st.success("✅ Secrets found!")
    email = st.secrets["gcp_service_account"]["client_email"]
    st.info(f"🤖 Bot Email: {email}")
    st.warning(f"⚠️ PLEASE CHECK: Is '{email}' added as an Editor to your Google Sheet?")
else:
    st.error("❌ No 'gcp_service_account' section found in Secrets.")
    st.stop()

# 2. Try Connecting
try:
    SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], 
        scopes=SCOPE
    )
    client = gspread.authorize(creds)
    
    # 3. Try Writing
    sheet = client.open("MaintWatch_Data").worksheet("removal_events")
    st.success("✅ Successfully found the Sheet!")
    
    sheet.append_row(["TEST_CONNECTION", "If you see this", "It works!"])
    st.balloons()
    st.success("✅ Wrote a test row to the sheet. Check it now!")

except Exception as e:
    st.error(f"❌ Connection Failed: {e}")
