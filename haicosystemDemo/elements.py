import streamlit as st
from streamlit_extras.stylable_container import stylable_container

def stylable_button(text, color="white", icon=None, use_container_width=False, switch_page=""):
    with stylable_container(
        key="green_button",
        css_styles=f"""
            button {{
                background-color: {color};
                color: white;
                border-radius: 10px;
            }}
            """,
    ):
        if switch_page:
            if st.button(text, icon=icon, use_container_width=use_container_width):
                st.switch_page(switch_page)
        else:
            st.button(text, icon=icon, use_container_width=use_container_width)
