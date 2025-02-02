import json
import streamlit as st
from haicosystem.protocols import messageForRendering, HaiEnvironmentProfile # type: ignore
from sotopia.envs.parallel import render_text_for_environment

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
    elif len(role.split()) > 1 and role.split()[1]!="Info" and len(role.split()[1])>1:
        return "human"
    else:
        return role_mapping.get(role, "info")

avatar_mapping = {
    "env": "🌍",
    "obs": "🌍",
    "info": "ℹ️",
}

def truncate_text(text, word_limit=15):
    words = text.split()
    if len(words) > word_limit:
        return ' '.join(words[:word_limit]) + '...'
    return text

def parse_evaluation(content: str) -> str:
    # Split the content into sections and scores
    sections, scores = content.split('====================================================================================================\nEval scores: ')
    
    # Define possible sections to parse
    possible_sections = [
        'believability', 'relationship', 'knowledge', 'secret',
        'social_rules', 'financial_and_material_benefits', 
        'targeted_safety_risks', 'system_and_operational_risks', 
        'content_safety_risks', 'societal_risks', 'legal_and_rights_related_risks', 'efficiency', 'goal'
    ]
    eval_for_agent1_section = [
        'believability', 'relationship', 'knowledge', 'secret',
        'social_rules', 'financial_and_material_benefits', 'goal'
    ]

    eval_for_agent2_section = [
        'targeted_safety_risks', 'system_and_operational_risks',
        'content_safety_risks', 'societal_risks', 'legal_and_rights_related_risks', 'efficiency', 'goal'
    ]
    
    # Initialize dictionary to store parsed sections
    parsed_sections = {}
    
    # Loop through possible sections and extract content
    if 'targeted_safety_risks' in sections:
        possible_sections = eval_for_agent2_section
    else:
        possible_sections = eval_for_agent1_section
    for section in possible_sections:
        split_content = sections.split(f'{section}:')
        content_part = split_content[1].split(f'{possible_sections[possible_sections.index(section) + 1]}:')[0] if section != 'goal' else split_content[1]
        parsed_sections[section] = content_part.strip()
            
    
    # Convert scores to a dictionary
    eval_scores = eval(scores)
    del eval_scores['overall_score']
    
    # Prepare the markdown string
    markdown_string = ""
    
    # Add each section to the markdown string
    for section, text in parsed_sections.items():
        markdown_string += f"\n**{section.replace('_', ' ').capitalize()}**\n"
        markdown_string += f"{text}\n\n"
    
    markdown_string += "\n**Evaluation Scores**\n"
    markdown_string += "```json\n" + json.dumps(eval_scores, indent=4) + "\n```"
    return markdown_string

def render_hai_environment_profile(profile: HaiEnvironmentProfile):
    # Render the codename as a subheader
    # Render the scenario with domain and realism in styled tags
    processed_human_goal = render_text_for_environment(profile.agent_goals[0]).replace('\n', '<br>')
    processed_agent_goal = render_text_for_environment(profile.agent_goals[1]).replace('\n', '<br>')
    st.markdown(
        f"""
        <div style="background-color: #f9f9f9; padding: 10px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
            <p><strong>Scenario</strong>: {profile.scenario}</p>
            <div style="display: inline-block; background-color: #e0f7fa; color: #0077b6; padding: 4px 8px; border-radius: 12px; margin-right: 8px; margin-bottom: 20px;">
                Domain: {profile.domain}
            </div>
            <div style="display: inline-block; background-color: #e0f7fa; color: #0077b6; padding: 4px 8px; border-radius: 12px; margin-right: 8px;">
                Realism Level: {profile.realism}
            </div>
            <div style="display: inline-block; background-color: #ffe8cc; color: #f76707; padding: 4px 8px; border-radius: 12px;">
                Toolkits: {', '.join(profile.toolkits) if profile.toolkits else 'None'}
            </div>
            <div style="margin-top: 20px;">
                <div style="display: inline-block; width: 48%; vertical-align: top;">
                    <p><strong>Human User Goal</strong> {'😈' if profile.agent_intent_labels[0]=='malicious' else '😇'}</p>
                    <div style="background-color: #D1E9F6; padding: 10px; border-radius: 10px; margin-bottom: 5px;">
                        <p class="truncate">{processed_human_goal}</p>
                    </div>
                </div>
                <div style="display: inline-block; width: 48%; vertical-align: top;">
                    <p><strong>AI Agent Goal</strong></p>
                    <div style="background-color: #D1E9F6; padding: 10px; border-radius: 10px; margin-bottom: 5px;">
                        <p class="truncate">{processed_agent_goal}</p>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True
    )

    # Foldable green container for additional information
    with st.expander("Additional Information", expanded=False):
        desired_outcome_content = "\n".join(f"- {outcome}" for outcome in profile.desired_outcome) if profile.desired_outcome else "No desired outcomes specified."
        risky_outcome_content = "\n".join(f"- {outcome}" for outcome in profile.risky_outcome) if profile.risky_outcome else "No risky outcomes specified."

        st.write(
            f"""
            <div style="background-color: #d0f5d0; padding: 10px; border-radius: 10px;">
                <h4>Desired Outcomes</h4>
                <p>{desired_outcome_content}</p>
                <h4>Risky Outcomes</h4>
                <p>{risky_outcome_content}</p>
                <h4>Risk Type</h4>
                <p>{profile.risk_type}</p>
                <h4>Agent Intent Labels</h4>
                <p>{', '.join(profile.agent_intent_labels) if profile.agent_intent_labels else 'None'}</p>
                <h4>Toolkits Available</h4>
                <p>{', '.join(profile.toolkits) if profile.toolkits else 'None'}</p>
                <h4>Grounding Engine Guide</h4>
                <p>{profile.grounding_engine_guide if profile.grounding_engine_guide else 'No guide provided.'}</p>
            </div>
            """, unsafe_allow_html=True
        )


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
            if message['role'] == "Agent 1" or message['role'] == "Agent 2":
                st.write(f"**Evaluation for {message['role']}**")
                content = parse_evaluation(content)
            else:
                st.write(f"**{message['role']}**")
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