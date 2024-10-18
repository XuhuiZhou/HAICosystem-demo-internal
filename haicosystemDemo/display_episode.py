import os
import streamlit as st
os.environ["REDIS_OM_URL"] = st.secrets["REDIS_OM_URL"]
print(os.environ['REDIS_OM_URL'])
from sotopia.database import EpisodeLog

from haicosystem.utils.render import render_for_humans # type: ignore
from haicosystem.protocols import HaiEnvironmentProfile # type: ignore
from haicosystemDemo.hai_stream import render_hai_environment_profile, streamlit_rendering

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("./css/style.css")

TAGS = (
    "haicosystem_debug", 
    "benchmark_gpt-4-turbo_gpt-4o_gpt-4o_haicosystem_trial0",
    "benchmark_gpt-4-turbo_gpt-4o_gpt-4o_haicosystem_trial2",
    "benchmark_gpt-3.5-turbo_gpt-4o_gpt-4o_haicosystem_trial2",
    "benchmark_gpt-4-turbo_gpt-4o-2024-08-06_gpt-4o-2024-08-06_haicosystem_trial2",
    "benchmark_gpt-3.5-turbo_gpt-4o-2024-08-06_gpt-4o-2024-08-06_haicosystem_trial2",
    "benchmark_together_ai/meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo_gpt-4o-2024-08-06_gpt-4o-2024-08-06_haicosystem_trial2",
    "benchmark_together_ai/meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo_gpt-4o-2024-08-06_gpt-4o-2024-08-06_haicosystem_trial2",
    "benchmark_together_ai/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo_gpt-4o-2024-08-06_gpt-4o-2024-08-06_haicosystem_trial2",
    "benchmark_gpt-4-turbo_gpt-4o-2024-08-06_gpt-4o-2024-08-06_haicosystem_wo_interaction_2",
    "benchmark_claude-3-opus-20240229_gpt-4o-2024-08-06_gpt-4o-2024-08-06_haicosystem_trial3",
)

TAGS_MAPPING = {
    "gpt-4-turbo": [
        "benchmark_gpt-4-turbo_gpt-4o-2024-08-06_gpt-4o-2024-08-06_haicosystem_trial2",
    ],
    "gpt-3.5-turbo": [
        "benchmark_gpt-3.5-turbo_gpt-4o-2024-08-06_gpt-4o-2024-08-06_haicosystem_trial2"
    ],
    "Llama-3.1-405B": [
        "benchmark_together_ai/meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo_gpt-4o-2024-08-06_gpt-4o-2024-08-06_haicosystem_trial2",
    ],
    "Llama-3.1-70B": [
        "benchmark_together_ai/meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo_gpt-4o-2024-08-06_gpt-4o-2024-08-06_haicosystem_trial2",
    ],
    "Llama-3.1-8B": [
        "benchmark_together_ai/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo_gpt-4o-2024-08-06_gpt-4o-2024-08-06_haicosystem_trial2",
    ]
}

def init_params():
    if "pk" not in st.query_params:
        st.query_params.pk = ""
        st.session_state.coming_from_link = False
    elif "coming_from_link" not in st.session_state:
        st.session_state.coming_from_link = True
    print("Coming from link:", st.session_state.coming_from_link)
    print("Query params:", st.query_params)

def update_params(pk: str = ""):
    st.query_params.pk = pk

@st.cache_data(max_entries=1)
def episode_list(tag_option: str) -> tuple[list[EpisodeLog], int, list[str], list[str]]:
    # st.write("You selected:", tag_option)
    # print("You selected:", tag_option)
    episode_list: list[EpisodeLog] = EpisodeLog.find(EpisodeLog.tag == tag_option).all()
    episode_list_len = max(len(episode_list), 0)
    print("Episode list length:", episode_list_len)
    try:
        episode_code_name = []  # type: ignore
        domain = []  # type: ignore
        for i, episode in enumerate(episode_list):
            environment = HaiEnvironmentProfile.get(pk=episode.environment)
            episode_code_name.append(environment.codename)
            domain.append(environment.domain)
    except Exception as e:
        episode_code_name = []
    return episode_list, episode_list_len, episode_code_name, domain

def display_episode(pk: str = "") -> None:
    # Text input for episode number
    if pk:
        episode = EpisodeLog.get(pk=pk)
    else:
        if st.session_state.coming_from_link:
            episode = EpisodeLog.get(pk=st.query_params.pk)
            tag = episode.tag
            print("Tag:", tag)
            tag_index = TAGS.index(tag)
            print("Tag index:", tag_index)
        else:
            tag_index = 4 # default tag index

        # tag_option = st.selectbox(
        #     "Which tag do you want to see?",
        #     TAGS,
        #     index=tag_index,
        #     placeholder="Select contact method...",
        # )
        model_option = st.selectbox(
            "Which model do you want to see?",
            TAGS_MAPPING.keys(),
            index=0,
            placeholder="Select contact method...",
        )
        tag_option = TAGS_MAPPING[model_option][0]
        st.session_state.episode_list, st.session_state.episode_list_len, st.session_state.episode_code_name, st.session_state.domain = episode_list(tag_option)
        if st.session_state.episode_list_len == 0:
            st.write("No episode found.")
        else:
            # Select an episode
            if st.session_state.episode_code_name:
                if st.session_state.coming_from_link:
                    for i in range(st.session_state.episode_list_len):
                        if st.session_state.episode_list[i].pk == st.query_params.pk:
                            episode_index = i
                            break
                    st.session_state.coming_from_link = False
                try:
                    episode_choice = st.selectbox(
                        "Which episode would you like to see?",
                        [f"{str(i)}-[{st.session_state.domain[i]}]-{st.session_state.episode_code_name[i]}" for i in range(st.session_state.episode_list_len)],
                        index=episode_index,
                    )
                except NameError:
                    episode_choice = st.selectbox(
                        "Which episode would you like to see?",
                        [f"{str(i)}-[{st.session_state.domain[i]}]-{st.session_state.episode_code_name[i]}" for i in range(st.session_state.episode_list_len)],
                    )
                episode_number = episode_choice.split("-")[0]
            else:
                episode_number = st.text_input(f"Enter episode number (0-{st.session_state.episode_list_len}):", value="0")
            episode = st.session_state.episode_list[int(episode_number)]  # type: ignore
            if st.session_state.episode_code_name:
                episode_env = HaiEnvironmentProfile.get(pk=episode.environment)
                render_hai_environment_profile(episode_env)
            st.write(f"Episode retrieved with pk: {episode.pk}")
            update_params(episode.pk)
            assert isinstance(episode, EpisodeLog)
    messages = render_for_humans(episode)
    streamlit_rendering(messages)




DISPLAY_EPISODE_MODE = "Display Episodes"
# CHAT_MODE = "Chat with Model"
DISPLAY_SCENARIOS_MODE = "Display Scenarios"

st.title("HAICOSYSTEM Episode Rendering")
st.session_state.episode_list_len = 0
st.session_state.episode_list = []
init_params()
display_episode()