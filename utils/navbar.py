import streamlit as st
from streamlit_option_menu import option_menu

def create_header(current_page):
    
    # 1. CSS to HIDE the Default Sidebar completely
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] {display: none;}
        [data-testid="stSidebar"] {display: none;}
        </style>
        """,
        unsafe_allow_html=True
    )

    # 2. Define Menu Options
    # Added "New Entry" so you can access it easily without the Home page buttons
    options = ["Home", "New Entry", "Dashboard", "Data Upload", "Admin Tools"]
    icons = ["house", "plus-circle", "speedometer2", "cloud-upload", "tools"]

    try:
        default_index = options.index(current_page)
    except ValueError:
        default_index = 0

    # 3. Render the Horizontal Menu
    selected = option_menu(
        menu_title=None,
        options=options,
        icons=icons,
        default_index=default_index,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#f0f2f6"},
            "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px"},
            "nav-link-selected": {"background-color": "#004080"},
        }
    )

    # 4. Routing Logic
    if selected != current_page:
        if selected == "Home":
            st.switch_page("Home.py")
        elif selected == "New Entry":
            st.switch_page("pages/Component_Removal.py")
        elif selected == "Dashboard":
            st.switch_page("pages/MTBF_Dashboard.py")
        elif selected == "Data Upload":
            st.switch_page("pages/Data_Upload.py")
        elif selected == "Admin Tools":
            st.switch_page("pages/Admin_Tools.py")
            
    return selected
