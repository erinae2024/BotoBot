# app.py

import streamlit as st
import json
import random
import re
from nltk.chat.util import Chat, reflections
from nlp.patterns import pairs
from nlp.translator import build_entity_masker, process_language
from nlp.classifier import train_classifier, get_intent
from nlp.query_engine import (
    get_dynamic_tags,
    resolve_pronouns,
    extract_and_normalize_slots,
    match_candidates_by_tag,
    get_candidate_projects,
    verify_project_association
)

USER_AVATAR = "UserMascot.png"
BOT_AVATAR = "BotoBotMascot.png"

st.set_page_config(page_title="BotoBot Chatbot", page_icon=BOT_AVATAR)
st.image("BotoBot_WideLogoTransparent.png", width="stretch")
st.caption("An NLP-powered chatbot for voter education. Developed by DLSU Computer Science Students.")

st.html("<style>[data-testid='stHeaderActionElements'] {display: none;}</style>")

@st.cache_resource
def load_assets():
    with open('data/candidates.json', 'r') as f:
        candidates_data = json.load(f)
    masker, mask_map = build_entity_masker(candidates_data)
    classifier = train_classifier()
    chatbot = Chat(pairs, reflections)
    
    dynamic_tags = get_dynamic_tags(candidates_data)
    
    return candidates_data, masker, mask_map, classifier, chatbot, dynamic_tags

candidates_data, masker, mask_map, classifier, chatbot, dynamic_tags = load_assets()

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.active_candidate_key = None
    st.session_state.response_lang = None

if not st.session_state.response_lang:
    st.markdown("### How would you like me to respond? Paano mo gusto na sumagot ako?")
    col1, col2 = st.columns(2)
    if col1.button("English"):
        st.session_state.response_lang = 'en'
        st.session_state.messages.append({"role": "assistant", "content": "Welcome to BotoBot! Ask me a question about the 2022 Philippine presidential candidates, voting processes, or election-related laws! For example:\n- Who are the 2022 presidential candidates?\n- What are the requirements for a voter's ID?\n- What is RA 9006?\n- Who is (Candidate Name)?\n- What is (Candidate Name)'s projects?"})
        st.rerun()
    if col2.button("Tagalog"):
        st.session_state.response_lang = 'tl'
        st.session_state.messages.append({"role": "assistant", "content": "Maligayang pagdating sa BotoBot! Magtanong tungkol sa mga kandidato, o proseso ng pagboto, o mga batas tungkol sa eleksyon! Halimbawa:\n- Sino ang mga 2022 kandidato para sa pagkapangulo?\n- Ano ang mga kailangan para makakuha ng voter's ID?\n- Ano ang RA 9006?\n- Sino si (Pangalan ng Kandidato)?\n- Ano ang mga proyekto ni (Pangalan ng Kandidato)?"})
        st.rerun()
    st.stop()

for message in st.session_state.messages:
    avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about candidates, voting, or elections..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    resolved_prompt = resolve_pronouns(prompt, st.session_state.active_candidate_key, candidates_data)

    translated_prompt, is_tagalog = process_language(resolved_prompt, masker, mask_map, target_lang='en')

    detected_candidate_key, project_found, normalized_prompt = extract_and_normalize_slots(
        translated_prompt, st.session_state.active_candidate_key, candidates_data
    )

    if detected_candidate_key:
        st.session_state.active_candidate_key = detected_candidate_key

    final_response = ""

    regex_response = chatbot.respond(translated_prompt)

    if regex_response:
        final_response = regex_response
    else:
        # Let Naive Bayes attempt classification first with a STRICTER threshold (0.40)
        intent = get_intent(normalized_prompt, classifier, threshold=0.40)
        
        # If Naive Bayes falls back (None), try matching by tags
        if not intent:
            tag_regex = r'(?i)\b(' + '|'.join(dynamic_tags) + r')\b'
            if bool(re.search(tag_regex, translated_prompt)) and not project_found:
                intent = '__MATCH_TAG__'
                
        # Safe downgrade for project verification
        if intent == '__VERIFY_PROJECT__' and not project_found and detected_candidate_key:
            intent = '__SHOW_PROFILE__'
        
        if intent == '__SHOW_LIST__':
            list_str = "\n".join([f"* {data.get('full_name', key.title())}" for key, data in candidates_data.items()])
            final_response = f"Here are the 2022 Presidential Candidates in my database:\n\n{list_str}"
            
        elif intent == '__MATCH_TAG__':
            final_response = match_candidates_by_tag(translated_prompt, candidates_data, detected_candidate_key)
            
        elif intent == '__SHOW_PROJECTS__':
            final_response = get_candidate_projects(st.session_state.active_candidate_key, candidates_data)
            
        elif intent == '__VERIFY_PROJECT__':
            final_response = verify_project_association(translated_prompt, project_found, st.session_state.active_candidate_key, candidates_data)
            
        elif intent == '__SHOW_PROFILE__':
            if st.session_state.active_candidate_key and st.session_state.active_candidate_key in candidates_data:
                c = candidates_data[st.session_state.active_candidate_key]

                # Defensive Extraction Logic
                full_name = c.get('full_name', st.session_state.active_candidate_key.title())
                age = c.get('age', 'N/A')
                
                positions = c.get('positions', [])
                pos_str = ', '.join(positions) if isinstance(positions, list) and positions else "None listed"
                
                education = c.get('education', [])
                edu_str = ', '.join(education) if isinstance(education, list) and education else "None listed"
                
                projects = c.get('projects', [])
                if isinstance(projects, list) and projects:
                    projects_list = [p.get('name', 'Unnamed Project') for p in projects if isinstance(p, dict)]
                    proj_str = ', '.join(projects_list) if projects_list else "None listed"
                else:
                    proj_str = "None listed"

                links = c.get('links', [])
                if isinstance(links, list) and links:
                    links_str = ', '.join(links)
                elif isinstance(links, str) and links:
                    links_str = links
                else:
                    links_str = "None listed"

                final_response = (
                    f"### {full_name}\n"
                    f"* **Age:** {age}\n"
                    f"* **Positions:** {pos_str}\n"
                    f"* **Education:** {edu_str}\n"
                    f"* **Projects:** {proj_str}\n\n"
                    f"Links: {links_str}\n"
                )
            else:
                final_response = "Who are you asking about?"
                
        elif intent == '__SHOW_AGE__':
            if st.session_state.active_candidate_key and st.session_state.active_candidate_key in candidates_data:
                c = candidates_data[st.session_state.active_candidate_key]
                full_name = c.get('full_name', st.session_state.active_candidate_key.title())
                age = c.get('age', 'N/A')
                final_response = f"**{full_name}** is {age}."
            else:
                final_response = "Which candidate's age do you want to know?"
        else:
            final_response = "I'm not sure I understand. Try asking me to 'show the 2022 presidential candidates'!"

    if random.random() < 0.40:
        hints = ["Which candidates prioritize education?", "Which candidates have government experience?", "Who focuses on labor?"]
        if st.session_state.active_candidate_key and st.session_state.active_candidate_key in candidates_data:
            name = candidates_data[st.session_state.active_candidate_key].get('full_name', 'this candidate')
            hints.extend([f"How old is {name}?", f"What are {name}'s projects?"])
        final_response += f"\n\n💡 *Tip: You can also ask me: '{random.choice(hints)}'*"

    if st.session_state.response_lang == 'tl':
        final_response, _ = process_language(final_response, masker, mask_map, target_lang='tl')

    with st.chat_message("assistant", avatar=BOT_AVATAR):
        st.markdown(final_response)
    st.session_state.messages.append({"role": "assistant", "content": final_response})