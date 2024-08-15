import json
import streamlit as st
from haicosystem.protocols import messageForRendering # type: ignore

def role_mapping(role: str) -> str:
    role_mapping = {
        "Background Info": "background",
        "System": "info",
        "Environment": "env",
        "Observation": "obs",
        "General": "info",
        "Agent 1": "info",
        "Agent 2": "info",
        "User": "human",
        "Echo AI": "ai",
    }
    if 'AI' in role:
        return "ai"
    elif len(role.split()) > 1 and role.split()[1]!="Info":
        return "human"
    else:
        return role_mapping.get(role, "info")

avatar_mapping = {
    "env": "🌍",
    "obs": "🌍"
}

def streamlit_rendering(messages: list[messageForRendering]) -> None:
    for index, message in enumerate(messages):
        role = role_mapping(message["role"])
        content = message["content"]
        
        if role == "obs" or message.get("type") == "action":
            try:
                content = json.loads(content)
            except json.JSONDecodeError:
                pass

        with st.chat_message(role, avatar=avatar_mapping.get(role, None)):
            if isinstance(content, dict):
                st.json(content)
            elif role == "info":
                st.markdown(
                    f"""
                    <div style="background-color: lightblue; padding: 10px; border-radius: 5px;">
                        {content}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            elif index < 2:  # Apply foldable for the first two messages
                st.markdown(
                    f"""
                    <details>
                        <summary>Message {index + 1}</summary>
                        {content}
                    </details>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(content.replace("\n", "<br />"), unsafe_allow_html=True)


