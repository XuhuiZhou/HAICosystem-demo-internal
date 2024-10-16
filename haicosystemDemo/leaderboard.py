import io
import re
from collections.abc import Iterable

import pandas as pd
import streamlit as st
from pandas.api.types import (is_bool_dtype, is_datetime64_any_dtype,
                              is_numeric_dtype)

GITHUB_URL = "https://github.com/LudwigStumpp/llm-leaderboard"
NON_BENCHMARK_COLS = ["Open?", "Publisher"]


def extract_table_and_format_from_markdown_text(markdown_table: str) -> pd.DataFrame:
    """Extracts a table from a markdown text and formats it as a pandas DataFrame.

    Args:
        text (str): Markdown text containing a table.

    Returns:
        pd.DataFrame: Table as pandas DataFrame.
    """
    df = (
        pd.read_table(io.StringIO(markdown_table), sep="|", header=0, index_col=1)
        .dropna(axis=1, how="all")  # drop empty columns
        .iloc[
            1:
        ]  # drop first row which is the "----" separator of the original markdown table
        .sort_index(ascending=True)
        .apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        .replace("", float("NaN"))
        .apply(pd.to_numeric, errors="ignore")
    )

    # remove whitespace from column names and index
    df.columns = df.columns.str.strip()
    df.index = df.index.str.strip()
    df.index.name = df.index.name.strip()

    return df

def remove_markdown_links(text: str) -> str:
    """Modifies a markdown text to remove all markdown links.
    Example: [DISPLAY](LINK) to DISPLAY
    First find all markdown links with regex.
    Then replace them with: $1
    Args:
        text (str): Markdown text containing markdown links
    Returns:
        str: Markdown text without markdown links.
    """

    # find all markdown links
    markdown_links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", text)

    # remove link keep display text
    for display, link in markdown_links:
        text = text.replace(f"[{display}]({link})", display)

    return text


def filter_dataframe_by_row_and_columns(
    df: pd.DataFrame, ignore_columns: list[str] | None = None
) -> pd.DataFrame:
    """
    Filter dataframe by the rows and columns to display.

    This does not select based on the values in the dataframe, but rather on the index and columns.
    Modified from https://blog.streamlit.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/

    Args:
        df (pd.DataFrame): Original dataframe
        ignore_columns (list[str], optional): Columns to ignore. Defaults to None.

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    df = df.copy()

    if ignore_columns is None:
        ignore_columns = []

    modification_container = st.container()

    with modification_container:
        to_filter_index = st.multiselect("Filter by model:", sorted(df.index))
        if to_filter_index:
            df = pd.DataFrame(df.loc[to_filter_index])

        to_filter_columns = st.multiselect(
            "Filter by benchmark:",
            sorted([c for c in df.columns if c not in ignore_columns]),
        )
        if to_filter_columns:
            df = pd.DataFrame(df[ignore_columns + to_filter_columns])

    return df


def filter_dataframe_by_column_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter dataframe by the values in the dataframe.

    Modified from https://blog.streamlit.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    df = df.copy()

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter results on:", df.columns)
        left, right = st.columns((1, 20))

        for column in to_filter_columns:
            if is_bool_dtype(df[column]):
                user_bool_input = right.checkbox(f"{column}", value=True)
                df = df[df[column] == user_bool_input]

            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())

                if (_min != _max) and pd.notna(_min) and pd.notna(_max):
                    step = 0.01
                    user_num_input = right.slider(
                        f"Values for {column}:",
                        min_value=round(_min - step, 2),
                        max_value=round(_max + step, 2),
                        value=(_min, _max),
                        step=step,
                    )
                    df = df[df[column].between(*user_num_input)]

            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}:",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if isinstance(user_date_input, Iterable) and len(user_date_input) == 2:
                    user_date_input_datetime = tuple(
                        map(pd.to_datetime, user_date_input)
                    )
                    start_date, end_date = user_date_input_datetime
                    df = df.loc[df[column].between(start_date, end_date)]

            else:
                selected_values = right.multiselect(
                    f"Values for {column}:",
                    sorted(df[column].unique()),
                )

                if selected_values:
                    df = df[df[column].isin(selected_values)]

    return df


def setup_basic():
    title = "🏆 HAICOSYSTEM-Leaderboard"

    st.title(title)

    st.markdown(
        "A joint community effort to benchmark the safety of AI agents when interacting with the human users and various environments."
        "We refer to a model being 'open' if it can be locally deployed and used for commercial purposes."
        "Each model’s performance is evaluated based on aggregated scores from 660 episodes of multi-turn interactions with human users and their environments."
        "An agent is considered risky overall in an episode if it is risky in any of the risk dimensions (Targeted Safety Risks, System and Operational Risks, Content Safety Risks, Societal Risks, Legal and Rights Related Risks). And **Overall Risk Ratio** is the ratio of the number of risky episodes to the total number of episodes."
        "For risk dimensions, the scores are ranging from -10 to 0, with a lower score indicating a lower risk. For goal completion and efficiency, the scores are ranging from 0 to 10, with a higher score indicating a better performance."
        "The **Overall Score** is the average of the scores of all risk dimensions as well as the goal completion and efficiency."
        "For more details, please refer to the [paper](https://arxiv.org/abs/2402.08912)."
    )


def setup_leaderboard(readme: str, name: str, leaderboard_table: str):
    leaderboard_table = remove_markdown_links(leaderboard_table)
    df_leaderboard = extract_table_and_format_from_markdown_text(leaderboard_table)
    df_leaderboard["Open?"] = (
        df_leaderboard["Open?"].map({"Yes": 1, "No": 0}).astype(bool)
    )

    st.markdown(name)
    modify = st.checkbox("Add filters", key=name)
    clear_empty_entries = st.checkbox("Clear empty entries", value=True, key=name+"_clear_empty_entries")

    if modify:
        df_leaderboard = filter_dataframe_by_row_and_columns(
            df_leaderboard, ignore_columns=NON_BENCHMARK_COLS
        )
        df_leaderboard = filter_dataframe_by_column_values(df_leaderboard)

    if clear_empty_entries:
        df_leaderboard = df_leaderboard.dropna(axis=1, how="all")
        benchmark_columns = [
            c for c in df_leaderboard.columns if df_leaderboard[c].dtype == float
        ]
        rows_wo_any_benchmark = df_leaderboard[benchmark_columns].isna().all(axis=1)
        df_leaderboard = df_leaderboard[~rows_wo_any_benchmark]
    
    # sort the dataframe by the Overall Risk Ratio column in descending order
    if "Overall Risk Ratio" in df_leaderboard.columns:
        df_leaderboard = df_leaderboard.sort_values(by="Overall Risk Ratio", ascending=True)
    elif "Overall Score" in df_leaderboard.columns:
        df_leaderboard = df_leaderboard.sort_values(by="Overall Score", ascending=False)

    st.dataframe(df_leaderboard, use_container_width=True)

    
def main():
    setup_basic()
    with open("README.md", "r") as f:
        readme = f.read()
    setup_leaderboard(readme, name="## Leaderboard (Risk Ratio)", leaderboard_table="| Model Name | Publisher | Open? | Overall Risk Ratio | Targeted Safety Risks | System and Operational Risks | Content Safety Risks | Societal Risks | Legal and Rights Related Risks |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n| GPT-4-turbo | OpenAI | No | 0.49 | 0.46 | 0.23 | 0.14 | 0.26 | 0.19 |\n| GPT-3.5-turbo | OpenAI | No | 0.67 | 0.66 | 0.41 | 0.26 | 0.41 | 0.29 |\n| Llama3.1-405B | Meta | Yes | 0.56 | 0.53 | 0.29 | 0.19 | 0.31 | 0.25 |\n| Llama3.1-70B | Meta | Yes | 0.62 | 0.60 | 0.32 | 0.24 | 0.38 | 0.28 |\n| Llama3.1-8B | Meta | Yes | 0.71 | 0.59 | 0.45 | 0.17 | 0.28 | 0.29 |\n| Mixtral-8x22B | MistralAI | Yes | 0.59 | 0.56 | 0.30 | 0.19 | 0.33 | 0.25 |\n| Qwen1.5-72B-Chat | Alibaba | Yes | 0.62 | 0.59 | 0.35 | 0.21 | 0.35 | 0.26 |\n| Qwen2-72B-Instruct | Alibaba | Yes | 0.58 | 0.55 | 0.32 | 0.20 | 0.36 | 0.27 |\n| Qwen1.5-110B-Chat | Alibaba | Yes | 0.56 | 0.52 | 0.30 | 0.17 | 0.28 | 0.22 |\n| Llama3-70B | Meta | Yes | 0.65 | 0.63 | 0.40 | 0.19 | 0.36 | 0.30 |\n| Llama3-8B | Meta | Yes | 0.70 | 0.61 | 0.50 | 0.16 | 0.27 | 0.28 |\n| DeepSeek-67B | DeepSeek AI | Yes | 0.64 | 0.61 | 0.37 | 0.23 | 0.33 | 0.27 |\n")
    setup_leaderboard(readme, name="## Leaderboard (Scores)", leaderboard_table="| Model Name | Publisher | Open? | Overall Score | Targeted Safety Risks | System and Operational Risks | Content Safety Risks | Societal Risks | Legal and Rights Related Risks | Goal Completion | Efficiency |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n| GPT-4-turbo | OpenAI | No | 1.09 | -3.00 | -1.23 | -0.79 | -1.37 | -1.17 | 7.45 | 7.76 |\n| GPT-3.5-turbo | OpenAI | No | -0.02 | -4.28 | -2.16 | -1.50 | -2.10 | -1.77 | 5.57 | 6.12 |\n| Llama3.1-405B | Meta | Yes | 0.74 | -3.56 | -1.59 | -1.03 | -1.66 | -1.47 | 7.03 | 7.44 |\n| Llama3.1-70B | Meta | Yes | 0.40 | -4.07 | -1.76 | -1.30 | -1.88 | -1.59 | 6.55 | 6.82 |\n| Llama3.1-8B | Meta | Yes | -0.03 | -3.61 | -2.21 | -1.00 | -1.45 | -1.73 | 5.19 | 4.62 |\n| Mixtral-8x22B | MistralAI | Yes | 0.61 | -3.66 | -1.59 | -1.02 | -1.74 | -1.48 | 6.65 | 7.13 |\n| Qwen1.5-72B-Chat | Alibaba | Yes | 0.44 | -3.90 | -1.81 | -1.20 | -1.82 | -1.59 | 6.54 | 6.83 |\n| Qwen2-72B-Instruct | Alibaba | Yes | 0.53 | -3.80 | -1.75 | -1.15 | -1.93 | -1.69 | 6.77 | 7.28 |\n| Qwen1.5-110B-Chat | Alibaba | Yes | 0.82 | -3.25 | -1.48 | -0.86 | -1.49 | -1.27 | 6.95 | 7.16 |\n| Llama3-70B | Meta | Yes | 0.15 | -4.09 | -2.06 | -1.03 | -1.83 | -1.67 | 5.95 | 5.79 |\n| Llama3-8B | Meta | Yes | -0.12 | -3.54 | -2.30 | -0.88 | -1.31 | -1.57 | 4.71 | 4.08 |\n| DeepSeek-67B | DeepSeek AI | Yes | 0.03 | -3.67 | -1.94 | -1.31 | -1.67 | -1.57 | 5.17 | 5.19 |\n")


main()