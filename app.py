import os
import streamlit as st
os.environ["REDIS_OM_URL"] = st.secrets["REDIS_OM_URL"]
print(os.environ['REDIS_OM_URL'])
from sotopia.database import EpisodeLog

from haicosystem.utils.render import render_for_humans # type: ignore
from haicosystem.protocols import HaiEnvironmentProfile
from haicosystemDemo.hai_stream import streamlit_rendering

def episode_list() -> None:
    # Text input for episode number
    tag_option = st.selectbox(
        "Which tag do you want to see?",
        ("haicosystem_debug", "benchmark_gpt-4-turbo_gpt-4o_gpt-4o_haicosystem_trial0"),
        placeholder="Select contact method...",
    )
    st.write("You selected:", tag_option)
    print("You selected:", tag_option)
    episode_list: list[EpisodeLog] = EpisodeLog.find(EpisodeLog.tag == tag_option).all()
    episode_list_len = max(len(episode_list)-1, 0)
    st.session_state.episode_list_len = episode_list_len
    st.session_state.episode_list = episode_list
    try:
        st.session_state.episode_code_name = [HaiEnvironmentProfile.get(episode.environment).codename for episode in episode_list]  # type: ignore
    except Exception as e:
        st.session_state.episode_code_name = []

@st.fragment()
def display_episode() -> None:
    if st.session_state.episode_list_len == 0:
        st.write("No episode found.")
    else:
        # Select an episode
        if st.session_state.episode_code_name:
            episode_choice = st.selectbox(
                "Which episode would you like to see?",
                [f"{str(i)}-{st.session_state.episode_code_name[i]}" for i in range(st.session_state.episode_list_len)],
            )
            episode_number = episode_choice.split("-")[0]
        else:
            episode_number = st.text_input(f"Enter episode number (0-{st.session_state.episode_list_len}):", value="0")
        episode = st.session_state.episode_list[int(episode_number)]  # type: ignore
        st.write(f"Episode retrieved: {episode.pk}")
        assert isinstance(episode, EpisodeLog)
        messages = render_for_humans(episode)
        streamlit_rendering(messages)

st.title("HAICosystem Episode Rendering")
st.session_state.episode_list_len = 0
st.session_state.episode_list = []
episode_list()
display_episode()

