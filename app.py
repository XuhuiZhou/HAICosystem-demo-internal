import os
import streamlit as st
os.environ["REDIS_OM_URL"] = st.secrets["REDIS_OM_URL"]
print(os.environ['REDIS_OM_URL'])
from sotopia.database import EpisodeLog

from haicosystem.utils.render import render_for_humans # type: ignore
from haicosystemDemo.hai_stream import streamlit_rendering

def episode_list() -> None:
    # Text input for episode number
    tag_option = st.selectbox(
        "Which tag do you want to see?",
        ("haicosystem_debug", "haicosystem_trial_experiment_0"),
        placeholder="Select contact method...",
    )
    st.write("You selected:", tag_option)
    print("You selected:", tag_option)
    episode_list = EpisodeLog.find(EpisodeLog.tag == tag_option).all()
    episode_list_len = max(len(episode_list)-1, 0)
    st.session_state.episode_list_len = episode_list_len
    st.session_state.episode_list = episode_list

@st.fragment()
def display_episode() -> None:
    if st.session_state.episode_list_len == 0:
        st.write("No episode found.")
    else:
        # Select an episode
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

