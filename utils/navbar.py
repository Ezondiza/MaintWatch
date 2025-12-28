# /utils/navbar.py
import streamlit as st
from streamlit_option_menu import option_menu

def create_header(current_page):
    """
    Renders the top navigation bar, hides the sidebar, and handles routing.
    
    Args:
        current_page (str): The active tab name: "Home", "Dashboard", "Data Entry", or "Admin Tools"
    """
    
    # --- 1. CSS to HIDE the Default Sidebar completely ---
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] {display: none;}
        [data-testid="stSidebar"] {display: none;}
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- 2. Define Menu Options ---
    # We replaced "Settings" with "Admin Tools" to keep your critical functions accessible
    options = ["Home", "Dashboard", "Data Entry", "Admin Tools"]
    icons = ["house", "speedometer2", "pencil-square", "tools"]

    # Determine default index (fallback to 0 if page name doesn't match)
    try:
        default_index = options.index(current_page)
    except ValueError:
        default_index = 0

    # --- 3. Render the Horizontal Menu ---
    selected = option_menu(
        menu_title=None,
        options=options,
        icons=icons,
        default_index=default_index,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#f0f2f6"},
            "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#004080"},
        }
    )

    # --- 4. Routing Logic ---
    # If the user clicks a tab different from the current page, switch to it.
    if selected != current_page:
        if selected == "Home":
            st.switch_page("Home.py")
        elif selected == "Dashboard":
            st.switch_page("pages/MTBF_Dashboard.py")
        elif selected == "Data Entry":
            st.switch_page("pages/Component_Removal.py")
        elif selected == "Admin Tools":
            # This is where we will move your CSV Upload/Migration logic
            st.switch_page("pages/Admin_Tools.py") 
            
    return selected
