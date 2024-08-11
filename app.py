import os
import streamlit as st
os.environ["REDIS_OM_URL"] = st.secrets["REDIS_OM_URL"]
print(os.environ['REDIS_OM_URL'])
from sotopia.database import EpisodeLog

from haicosystem.utils.render import render_for_humans # type: ignore
from haicosystemDemo.hai_stream import streamlit_rendering

@st.cache_data
def episode_list(tag: str) -> tuple[list[EpisodeLog], int]:
    episode_list = EpisodeLog.find(EpisodeLog.tag == tag).all()
    episode_list_len = len(episode_list)-1
    return episode_list, episode_list_len

st.title("HAICosystem Episode Rendering")
# Text input for episode number
tag_option = st.selectbox(
    "Which tag do you want to see?",
    ("haicosystem_debug", "haicosystem_trial_experiment_0"),
    placeholder="Select contact method...",
)

st.write("You selected:", tag_option)
episode_list, episode_list_len = episode_list(tag_option)

# Select an episode
episode_number = st.text_input(f"Enter episode number (0-{episode_list_len}):", value="2")
episode = episode_list[int(episode_number)]  # type: ignore
st.write(f"Episode retrieved: {episode.pk}")

assert isinstance(episode, EpisodeLog)
messages = render_for_humans(episode)
streamlit_rendering(messages)