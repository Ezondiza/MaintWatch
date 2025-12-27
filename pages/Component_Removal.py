# /pages/Component_Removal.py

import streamlit as st
from forms.component_removal_form import component_removal_form

st.set_page_config(page_title="Component Removal", layout="wide")

st.title("Component Removal")

component_removal_form()
