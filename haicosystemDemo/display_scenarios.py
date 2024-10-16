import streamlit as st
from haicosystem.protocols import HaiEnvironmentProfile
from haicosystemDemo.hai_stream import render_hai_environment_profile

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("./css/style.css")

def display_scenarios():
    st.title("HAICosystem Scenarios")
    
    # Fetch all environment profiles
    envs = HaiEnvironmentProfile.find().all()
    
    # Extract unique domains
    domains = sorted(set(env.domain for env in envs))
    
    # Create a filter by domain
    selected_domain = st.selectbox("Filter by Domain", ["All"] + domains)
    
    # Filter environments based on selected domain
    if selected_domain != "All":
        envs = [env for env in envs if env.domain == selected_domain]
    
    col1, col2 = st.columns(2, gap="medium")
    for i, env in enumerate(envs):
        with col1 if i % 2 == 0 else col2:
            render_hai_environment_profile(env)
            st.write("---")

display_scenarios()