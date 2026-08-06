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
        st.session_state.messages.append({"role": "assistant", "content": "Welcome to BotoBot! Ask me a question about the 2022 Philippine presidential candidates or voting processes!"})
        st.rerun()
    if col2.button("Tagalog"):
        st.session_state.response_lang = 'tl'
        st.session_state.messages.append({"role": "assistant", "content": "Maligayang pagdating sa BotoBot! Magtanong tungkol sa mga kandidato o proseso ng pagboto!"})
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
        tag_regex = r'(?i)\b(' + '|'.join(dynamic_tags) + r')\b'
        has_tag_word = bool(re.search(tag_regex, translated_prompt))
        
        if has_tag_word and not project_found:
            intent = '__MATCH_TAG__'
        else:
            intent = get_intent(normalized_prompt, classifier, threshold=0.25)
            if intent == '__VERIFY_PROJECT__' and not project_found and detected_candidate_key:
                intent = '__SHOW_PROFILE__'
        
        if intent == '__SHOW_LIST__':
            list_str = "\n".join([f"* {data['full_name']}" for key, data in candidates_data.items()])
            final_response = f"Here are the 2022 Presidential Candidates in my database:\n\n{list_str}"
            
        elif intent == '__MATCH_TAG__':
            final_response = match_candidates_by_tag(translated_prompt, candidates_data, detected_candidate_key)
            
        elif intent == '__SHOW_PROJECTS__':
            final_response = get_candidate_projects(st.session_state.active_candidate_key, candidates_data)
            
        elif intent == '__VERIFY_PROJECT__':
            final_response = verify_project_association(translated_prompt, project_found, st.session_state.active_candidate_key, candidates_data)
            
        elif intent == '__SHOW_PROFILE__':
            if st.session_state.active_candidate_key:
                c = candidates_data[st.session_state.active_candidate_key]

                projectsList = [project["name"] for project in c["projects"]]

                final_response = (
                    f"### {c['full_name']}\n"
                    f"* **Age:** {c['age']}\n"
                    f"* **Positions:** {', '.join(c['positions'])}\n"
                    f"* **Education:** {', '.join(c['education'])}\n"
                    f"* **Projects:** {', '.join(projectsList)}\n\n"
                    f"Links: {', '.join(c['links'])}\n"
                )
            else:
                final_response = "Who are you asking about?"
                
        elif intent == '__SHOW_AGE__':
            if st.session_state.active_candidate_key:
                final_response = f"**{candidates_data[st.session_state.active_candidate_key]['full_name']}** is {candidates_data[st.session_state.active_candidate_key]['age']}."
            else:
                final_response = "Which candidate's age do you want to know?"
        else:
            final_response = "I'm not sure I understand. Try asking me to 'show the 2022 presidential candidates'!"

    if random.random() < 0.40:
        hints = ["Which candidates prioritize education?", "Which candidates have government experience?", "Who focuses on labor?"]
        if st.session_state.active_candidate_key:
            name = candidates_data[st.session_state.active_candidate_key]['full_name']
            hints.extend([f"How old is {name}?", f"What are {name}'s projects?"])
        final_response += f"\n\n💡 *Tip: You can also ask me: '{random.choice(hints)}'*"

    if st.session_state.response_lang == 'tl':
        final_response, _ = process_language(final_response, masker, mask_map, target_lang='tl')

    with st.chat_message("assistant", avatar=BOT_AVATAR):
        st.markdown(final_response)
    st.session_state.messages.append({"role": "assistant", "content": final_response})