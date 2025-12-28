# /Home.py

import streamlit as st
from utils.navbar import create_header # Import the function

# Page config must be the very first command
st.set_page_config(page_title="MaintWatch", layout="wide", initial_sidebar_state="collapsed")

# Render the Navbar (Tell it we are currently on 'Home')
create_header(current_page="Home")

# ... The rest of your Home code (Welcome text, etc.) ...
st.title("🛠️ Maintenance Watch")
# ...
