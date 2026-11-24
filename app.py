"""BotoBot: O-COCOSDA 2026 archival Streamlit research demonstration."""
from pathlib import Path
import json

import streamlit as st
from nltk.chat.util import Chat, reflections

from nlp.patterns import pairs
from nlp.translator import build_entity_masker
from nlp.classifier import train_classifier
from nlp.query_engine import get_dynamic_tags
from nlp.response_engine import respond_to_user
from nlp.tagalog_fallback import localize_answer
from nlp.intent_guard import topic_for_reply

BASE = Path(__file__).resolve().parent
LOGO = BASE / 'BotoBot_WideLogoTransparent.png'
BOT_AVATAR = str(BASE / 'BotoBotMascot.png') if (BASE / 'BotoBotMascot.png').exists() else '🤖'
USER_AVATAR = str(BASE / 'UserMascot.png') if (BASE / 'UserMascot.png').exists() else '👤'

st.set_page_config(
    page_title='BotoBot | O-COCOSDA 2026 Research Demo',
    page_icon='🗳️',
    layout='centered',
    initial_sidebar_state='collapsed',
)

@st.cache_resource(show_spinner='Preparing the research knowledge base…')
def load_assets():
    with (BASE / 'data/candidates.json').open(encoding='utf-8') as f:
        candidates = json.load(f)
    masker, mask_map = build_entity_masker(candidates)
    return candidates, masker, mask_map, train_classifier(), Chat(pairs, reflections), get_dynamic_tags(candidates)

if LOGO.exists():
    # Keep the brand visible without pushing the first interactive controls below the fold.
    st.image(str(LOGO), width=400)
else:
    st.title('🗳️ BotoBot')
st.caption('O-COCOSDA 2026 research demo • 2022 Philippine presidential candidates & selected election laws')
st.markdown('**Technical contact / lead developer: Arron B. Baranquil** · [Email](mailto:baranquil.eyron@gmail.com) · [LinkedIn](https://www.linkedin.com/in/arnbrnql) · [GitHub](https://github.com/arnbrnql)')
st.info('**Historical research scope:** BotoBot is based on the **2022** election. It is not an official COMELEC service, a real-time guide to upcoming elections, or a candidate endorsement. Check COMELEC for current rules.', icon='ℹ️')

try:
    assets = load_assets()
except Exception:
    st.error('The research knowledge base could not load. Please contact the technical maintainer listed below.')
    st.stop()

with st.expander('What BotoBot can answer / Ano ang puwedeng itanong?', expanded=False):
    st.markdown('''- **Candidates:** Who is Leni Robredo? / Sino si Leni Robredo?
- **Topics:** Which 2022 candidates are tagged for education, environment, and health?
- **Projects:** What are Leni Robredo’s listed projects?
- **Election law:** What is RA 9006?
- **Procedure:** How to vote? / Paano bumoto?
- **Voter ID:** Is a voter-ID card the same as voter registration?

Responses are limited to the curated research database and cited material.''')

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'active_candidate_key' not in st.session_state:
    st.session_state.active_candidate_key = None
if 'response_lang' not in st.session_state:
    st.session_state.response_lang = 'en'
if 'last_topic' not in st.session_state:
    st.session_state.last_topic = None

with st.sidebar:
    st.header('About this demonstration')
    st.caption('Research method: NLTK Naive Bayes + regular-expression routing + fuzzy candidate/entity matching; optional translation of English/Tagalog inputs.')
    st.markdown('**Original study (not a re-evaluation of this demo):** SUS **79.29** (n=7); **0% observed prompt-level hallucinations** on seven evaluated prompt groups; baseline answer score **7.31/10**, versus **8.64/10** for Gemini in that same benchmark. These are bounded observations—not a guarantee of universal accuracy.')
    st.divider()
    st.markdown('**Lead developer / demo support contact**')
    st.markdown('**Arron B. Baranquil**')
    st.markdown('[Email — primary](mailto:baranquil.eyron@gmail.com) · [DLSU email](mailto:arron_baranquil@dlsu.edu.ph)')
    st.markdown('[GitHub](https://github.com/arnbrnql) · [LinkedIn](https://www.linkedin.com/in/arnbrnql) · [Facebook](https://www.facebook.com/arron.baranquil)')
    st.caption('For bugs, technical collaboration, demo questions, or independent software inquiries.')
    st.divider()
    st.markdown('**Research authors and correspondence**')
    st.caption('Maria Art Antonette D. Clariño; Arron B. Baranquil; Erin A. Evangelio; Zachary Andre A. Cruz; Alaine Carlo R. Magdaluyo.')
    st.markdown('Paper corresponding author: [Dr. Maria Art Antonette D. Clariño](mailto:maria.art.clarino@dlsu.edu.ph). Technical-demo support is a separate role.')
    if st.button('Clear conversation', width="stretch"):
        st.session_state.messages = []
        st.session_state.active_candidate_key = None
        st.session_state.last_topic = None
        st.rerun()

st.markdown('**Answer language / Wika ng sagot**')
st.caption('Your selection applies to new answers; previous messages remain unchanged.')
st.session_state.response_lang = st.radio('Response language', ['en','tl'], format_func=lambda v: 'English' if v=='en' else 'Tagalog', horizontal=True, label_visibility='collapsed', key='language_selector')
for msg in st.session_state.messages:
    avatar = USER_AVATAR if msg['role'] == 'user' else BOT_AVATAR
    with st.chat_message(msg['role'], avatar=avatar):
        if msg['role'] == 'user':
            st.write(msg['content'])
        else:
            st.markdown(msg['content'])

st.markdown('**Try a research question**' if not st.session_state.messages else '**Ask another question**')
example_labels = [
    ('2022 candidates', 'List the 2022 presidential candidates'),
    ('Multiple topics', 'Which 2022 candidates focus on education, environment, and health?'),
    ('Voter-ID clarification', "What are the requirements for a voter's ID?"),
    ('Tagalog sample', 'Paano bumoto?'),
]
example_columns = st.columns(2)
example_prompt = None
for i, (label, question) in enumerate(example_labels):
    if example_columns[i % 2].button(label, key=f'example_{i}', width="stretch"):
        example_prompt = question

chat_prompt = st.chat_input('Ask about the 2022 candidates, voting, or election laws…', max_chars=1200)
prompt = example_prompt or chat_prompt
if prompt:
    with st.chat_message('user', avatar=USER_AVATAR):
        st.write(prompt)
    st.session_state.messages.append({'role': 'user','content': prompt})
    answer, new_active = respond_to_user(
        prompt, st.session_state.active_candidate_key, assets,
        previous_topic=st.session_state.last_topic,
    )
    st.session_state.last_topic = topic_for_reply(prompt, answer, st.session_state.last_topic)
    st.session_state.active_candidate_key = new_active if st.session_state.last_topic == "candidate" else None
    answer = localize_answer(
        prompt, answer, st.session_state.response_lang,
        assets[0], assets[1], assets[2],
    )
    with st.chat_message('assistant', avatar=BOT_AVATAR):
        st.markdown(answer)
    st.session_state.messages.append({'role': 'assistant','content':answer})

st.divider()
st.caption('BotoBot — O-COCOSDA 2026 academic demonstration. All historical profiles are from a fixed 2022 dataset. For official current election information, use COMELEC. Do not send personal information; English–Tagalog translation can use a third-party translation provider. Chat history exists within your active Streamlit session and platform logs may apply.')
