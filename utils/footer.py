# /utils/footer.py
import streamlit as st

def render_footer():
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: grey; font-size: 0.8em;'>
            MaintWatch v1.1 | Developed by Ghanshyam Acharya | © 2025 Sita Air<br>
            <i>Unauthorized access is prohibited.</i>
        </div>
        """,
        unsafe_allow_html=True
    )
