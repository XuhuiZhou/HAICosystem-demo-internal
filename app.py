import os
import streamlit as st
os.environ["REDIS_OM_URL"] = st.secrets["REDIS_OM_URL"]
print(os.environ['REDIS_OM_URL'])
from sotopia.database import EpisodeLog

from haicosystem.utils.render import render_for_humans # type: ignore
from haicosystem.protocols import HaiEnvironmentProfile # type: ignore
from haicosystemDemo.hai_stream import streamlit_rendering

def init_params():
    if "pk" not in st.query_params:
        st.query_params.pk = ""
        st.session_state.coming_from_link = False
    else:
        st.session_state.coming_from_link = True

def update_params(pk: str = ""):
    st.query_params.pk = pk


def episode_list() -> None:
    # Text input for episode number
    tag_option = st.selectbox(
        "Which tag do you want to see?",
        ("haicosystem_debug", "benchmark_gpt-4-turbo_gpt-4o_gpt-4o_haicosystem_trial0"),
        index=1,
        placeholder="Select contact method...",
    )
    st.write("You selected:", tag_option)
    print("You selected:", tag_option)
    episode_list: list[EpisodeLog] = EpisodeLog.find(EpisodeLog.tag == tag_option).all()
    episode_list_len = max(len(episode_list)-1, 0)
    st.session_state.episode_list_len = episode_list_len
    st.session_state.episode_list = episode_list
    try:
        st.session_state.episode_code_name = []  # type: ignore
        st.session_state.domain = []  # type: ignore
        for i, episode in enumerate(episode_list):
            environment = HaiEnvironmentProfile.get(pk=episode.environment)
            st.session_state.episode_code_name.append(environment.codename)
            st.session_state.domain.append(environment.domain)
    except Exception as e:
        st.session_state.episode_code_name = []

@st.fragment()
def display_episode() -> None:
    if st.session_state.episode_list_len == 0:
        st.write("No episode found.")
    else:
        # Select an episode
        episode_index = 0
        if st.session_state.episode_code_name:
            if st.session_state.coming_from_link:
                st.write(f"Query param: {st.query_params.pk}")
                episode_index = [i for i in range(st.session_state.episode_list_len) if st.session_state.episode_list[i].pk == st.query_params.pk][0]
                st.session_state.coming_from_link = False
            episode_choice = st.selectbox(
                "Which episode would you like to see?",
                [f"{str(i)}-[{st.session_state.domain[i]}]-{st.session_state.episode_code_name[i]}" for i in range(st.session_state.episode_list_len)],
                index=episode_index,
            )
            episode_number = episode_choice.split("-")[0]
        else:
            episode_number = st.text_input(f"Enter episode number (0-{st.session_state.episode_list_len}):", value="0")
        episode = st.session_state.episode_list[int(episode_number)]  # type: ignore
        st.write(f"Episode retrieved with pk: {episode.pk}")
        update_params(episode.pk)
        assert isinstance(episode, EpisodeLog)
        messages = render_for_humans(episode)
        streamlit_rendering(messages)

st.title("HAICosystem Episode Rendering")
st.session_state.episode_list_len = 0
st.session_state.episode_list = []

init_params()
episode_list()
display_episode()

