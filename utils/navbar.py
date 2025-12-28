# /utils/navbar.py
import streamlit as st
from streamlit_option_menu import option_menu

def create_header(current_page):
    
    # ... (CSS to hide sidebar remains the same) ...
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] {display: none;}
        [data-testid="stSidebar"] {display: none;}
        </style>
        """,
        unsafe_allow_html=True
    )

    # UPDATED MENU OPTIONS
    # "Data Upload" replaces "Data Entry"
    options = ["Home", "Dashboard", "Data Upload", "Admin Tools"]
    icons = ["house", "speedometer2", "cloud-upload", "tools"]

    try:
        default_index = options.index(current_page)
    except ValueError:
        default_index = 0

    selected = option_menu(
        menu_title=None,
        options=options,
        icons=icons,
        default_index=default_index,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#f0f2f6"},
            "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px"},
            "nav-link-selected": {"background-color": "#004080"},
        }
    )

    # UPDATED ROUTING
    if selected != current_page:
        if selected == "Home":
            st.switch_page("Home.py")
        elif selected == "Dashboard":
            st.switch_page("pages/MTBF_Dashboard.py")
        elif selected == "Data Upload":
            st.switch_page("pages/Data_Upload.py") # New Page
        elif selected == "Admin Tools":
            st.switch_page("pages/Admin_Tools.py")
            
    return selected
