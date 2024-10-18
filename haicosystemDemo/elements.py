import streamlit as st
from streamlit_extras.stylable_container import stylable_container

def stylable_button(text, color="white", icon=None, use_container_width=False, switch_page="", new_tab=False):
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
        if new_tab:
            link = switch_page.split("/")[-1].split(".")[0]
            st.markdown(
                f"""
                <a href="/{link}" target="_blank" style="
                    display: inline-block;
                    background-color: {color};
                    color: white;
                    border-radius: 10px;
                    padding: 0.5em 1em;
                    text-decoration: none;
                    width: 100%;
                    text-align: center;
                ">{text}</a>
                """, 
                unsafe_allow_html=True
            )
        else:
            if switch_page:
                if st.button(text, icon=icon, use_container_width=use_container_width):
                    st.switch_page(switch_page)
            else:
                st.button(text, icon=icon, use_container_width=use_container_width)
