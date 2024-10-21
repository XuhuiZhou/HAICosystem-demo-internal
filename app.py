import streamlit as st

st.set_page_config(page_title="HAICOSYSTEM: An Ecosystem for Sandboxing Safety Risks in Human-AI Interactions", page_icon="./figs/haicosys.svg", layout="wide", initial_sidebar_state="expanded", menu_items={"About": "Xuhui Zhou from CMU LTI: https://xuhuiz.com/"})

display_intro = st.Page("./haicosystemDemo/intro.py", title="Introduction", icon=":material/home:")
display_scenario = st.Page("./haicosystemDemo/display_scenarios.py", title="Scenarios", icon=":material/photo_library:")
display_episode = st.Page("./haicosystemDemo/display_episode.py", title="Episode", icon=":material/live_tv:")
display_leaderboard = st.Page("./haicosystemDemo/leaderboard.py", title="Leaderboard", icon=":material/leaderboard:")
display_paper = st.Page("./haicosystemDemo/paper.py", title="Paper", icon=":material/description:")
display_chat_now = st.Page("./haicosystemDemo/chat_now.py", title="Chat Now (Coming Soon)", icon=":material/chat:")
display_create_your_own = st.Page("./haicosystemDemo/create_your_own.py", title="Create Your Own (Coming Soon)", icon=":material/add:")
st.logo("./figs/haicosys.svg", icon_image="./figs/haicosys.svg", size="large", link="https://haicosystem.org")

pg = st.navigation([display_intro, display_scenario, display_episode, display_leaderboard, display_paper, display_chat_now, display_create_your_own])
pg.run()
