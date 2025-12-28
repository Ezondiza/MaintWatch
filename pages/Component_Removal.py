# /pages/Component_Removal.py
import streamlit as st
from utils.navbar import create_header

st.set_page_config(page_title="New Removal", layout="wide", initial_sidebar_state="collapsed")

# Note: Since this page isn't in the top menu, we can default the highlight to "Home"
# or just leave it unselected.
create_header(current_page="Home") 

st.title("➕ New Component Removal Event")
st.markdown("Record a single unscheduled removal event.")

# ... Place your original form code here ...
# with st.form("removal_form"):
#    ...
