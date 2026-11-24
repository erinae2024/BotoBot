"""Black-box multilingual conversations copied from or modeled on real demo failures.

No internet connection, Streamlit server, or external translation service is required.
The intention is abstention and correct routing, not broad generative coverage.
"""
import ast
import json
from pathlib import Path

import pytest
from nltk.chat.util import Chat, reflections

from nlp.classifier import train_classifier
from nlp.intent_guard import topic_for_reply
from nlp.patterns import pairs
from nlp.query_engine import get_dynamic_tags
from nlp.response_engine import respond_to_user
from nlp.tagalog_fallback import localize_answer
from nlp.translator import build_entity_masker

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope='module')
def assets():
    candidates = json.loads((ROOT / 'data/candidates.json').read_text(encoding='utf-8'))
    masker, mask_map = build_entity_masker(candidates)
    return (candidates, masker, mask_map, train_classifier(),
            Chat(pairs, reflections), get_dynamic_tags(candidates))


# These are everyday phrasings, not the exact scripted prompts from the paper.
@pytest.mark.parametrize('question', [
    'paano bumoto?',
    'okay paano bumoto?',
    'paano kaya bumoto nan tama',
    'paano kaya bumoto nang tama',
    'paano process ng voting',
    'ano ang proseso nung boto?',
    'ano ang proseso ng pagboto?',
    'ano po ang tamang proseso ng pagboto?',
    'paano po ang pagboto?',
    'pano ba ako boboto',
    'paano mag vote',
    'gusto kong bumoto',
    'gusto ko bumoto',
    'how can I cast my ballot?',
    'how can we vote?',
    'how does voting work?',
    'what is the voting process?',
    'what are the steps in voting?',
    'what is the process of voting?',
    'what is the procedure to vote?',
    'i wanna vote how',
    'but how can she vote?',
])
def test_unrehearsed_phrases_route_to_voting_steps_not_candidate(question, assets):
    answer, candidate = respond_to_user(question, None, assets)
    assert answer.startswith('To vote in Philippine elections:')
    assert 'precinctfinder.comelec.gov.ph' in answer
    assert not answer.startswith('### ')
    assert candidate is None


@pytest.mark.parametrize('question', [
    'paano kaya bumoto nan tama',
    'paano process ng voting',
    'ano ang proseso nung boto?',
    'saan ba ako boboto?',
    'what is the voting process?',
    'how to vote correctly?',
    'mga hakbang sa pagboto',
    'gusto kong bumoto',
    'what is the process?',
    'how do you vote in the Philippines?',
    'bili ng boto',
    'sige',
    'okay',
    'what is the meaning of life?',
])
def test_non_name_queries_never_become_candidate_biographies(question, assets):
    answer, _ = respond_to_user(question, None, assets)
    assert not answer.startswith('### '), f'Unrelated candidate profile for {question!r}'
    assert '### Emmanuel' not in answer


@pytest.mark.parametrize('question,expected', [
    ('bili ng boto', 'Section 261(a)'),
    ('vote buying', 'Section 261(a)'),
    ('buying votes', 'Section 261(a)'),
    ('vote-selling', 'Section 261(a)'),
    ('how to register to vote?', 'register as a voter'),
    ('saan ba ako boboto?', 'cannot access voter registration'),
    ('where can I vote?', 'cannot access voter registration'),
    ('how do I vote in 2028?', '2022 Philippine presidential candidates'),
    ('Who should I vote for?', 'do not recommend or endorse'),
    ('Sino ang dapat kong iboto?', 'do not recommend or endorse'),
    ('Paano bumoto sa 2028?', '2022 Philippine presidential candidates'),
    ('ano ang mga kandidato sa 2028 eleksyon?', '2022 Philippine presidential candidates'),
    ('Paano bumili ng boto?', 'Section 261(a)'),
    ('What is the penalty for vote buying?', 'one to six years'),
    ('Who is Leni Robredo?', 'Maria Leonor'),
    ('Who is Robreddo?', 'Maria Leonor'),
    ('What is RA 9006?', 'Republic Act No. 9006'),
    ('Is a voter-ID card the same as voter registration?', 'different from voter registration'),
])
def test_competing_routing_priorities(question, expected, assets):
    answer, _ = respond_to_user(question, None, assets)
    assert expected.casefold() in answer.casefold()


def simulate_dialogue(prompts, assets, language='en'):
    candidate = None
    topic = None
    transcript = []
    for prompt in prompts:
        english, candidate = respond_to_user(prompt, candidate, assets, previous_topic=topic)
        topic = topic_for_reply(prompt, english, topic)
        displayed = localize_answer(prompt, english, language, assets[0], assets[1], assets[2])
        transcript.append((prompt, english, displayed, candidate, topic))
    return transcript


@pytest.mark.parametrize('language', ['en', 'tl'])
def test_exact_problem_transcript_preserves_context_and_language(language, assets, monkeypatch):
    # Simulate external translation outage; the demonstrated topics remain useful.
    monkeypatch.setattr('nlp.tagalog_fallback.process_language', lambda text, *_a, **_k: (text, False))
    chat = simulate_dialogue([
        'paano bumoto?',
        'okay edi ano ang process',
        'ano ang proseso nung boto?',
        'bili ng boto',
        'sige',
        'paano kaya bumoto nan tama',
    ], assets, language)
    for index in (0, 1, 2, 5):
        assert chat[index][1].startswith('To vote in Philippine elections:')
        assert chat[index][3] is None
        if language == 'tl':
            assert 'Paano bumoto' in chat[index][2]
            assert 'pagsasalin' not in chat[index][2]
    assert 'Section 261(a)' in chat[3][1]
    assert 'welcome' in chat[4][1].lower()
    if language == 'tl':
        assert 'Pagbili' in chat[3][2]
        assert 'Walang anuman' in chat[4][2]
        assert 'pagsasalin' not in chat[3][2]
        assert 'pagsasalin' not in chat[4][2]


def test_ambiguous_process_question_requires_actual_context(assets):
    text, _ = respond_to_user('okay edi ano ang process', None, assets)
    assert text.startswith('Do you mean **how to cast a ballot**?')
    # After an unrelated candidate profile, do not assume this means casting a vote.
    text, _ = respond_to_user('ano ang process', 'leni robredo', assets, previous_topic='candidate')
    assert text.startswith('Do you mean **how to cast a ballot**?')


def test_acknowledgment_retains_topic_but_new_subject_resets_it(assets):
    chat = simulate_dialogue(['How do I vote?', 'sige', 'okay edi ano ang process'], assets)
    assert chat[-1][1].startswith('To vote in Philippine elections:')
    chat = simulate_dialogue(['How do I vote?', 'Who is Leni Robredo?', 'okay edi ano ang process'], assets)
    assert chat[-1][1].startswith('Do you mean **how to cast a ballot**?')


@pytest.mark.parametrize('question,expected', [
    ('Paano bumoto?', 'presinto'),
    ('ano ang proseso nung boto?', 'presinto'),
    ('bili ng boto', 'Pagbili'),
    ('sige', 'Walang anuman'),
    ('Who is Leni Robredo?', 'Edad sa datos'),
    ('How old is Leni Robredo?', 'Edad ni'),
    ('What are Leni Robredo\'s projects?', 'gawaing lehislatibo'),
    ('What are the requirements for a voter\'s ID?', 'Magkaiba'),
    ('Who should I vote for?', 'Hindi nagrerekomenda'),
    ('Who are the 2028 presidential candidates?', '2022'),
    ('How do I register to vote?', 'Pagpaparehistro'),
    ('What is the penalty for vote buying?', 'pagkakakulong'),
])
def test_offline_tagalog_covers_core_topics_without_translation_service(question, expected, assets, monkeypatch):
    calls = []
    def unavailable(*_args, **_kwargs):
        calls.append(True)
        raise RuntimeError('Translation provider unavailable')
    monkeypatch.setattr('nlp.tagalog_fallback.process_language', unavailable)
    english, _ = respond_to_user(question, None, assets)
    displayed = localize_answer(question, english, 'tl', assets[0], assets[1], assets[2])
    assert expected.casefold() in displayed.casefold()
    assert not calls, 'Should not depend on translation for a core research topic'
    assert 'Hindi available ang awtomatikong pagsasalin' not in displayed


def test_tagalog_out_of_scope_cannot_turn_2028_question_into_2022_instructions(assets):
    english, _ = respond_to_user('How do I vote in 2028?', None, assets)
    tagalog = localize_answer('How do I vote in 2028?', english, 'tl', assets[0], assets[1], assets[2])
    assert 'susunod na eleksyon' in tagalog
    assert 'Paano bumoto (pangkalahatang proseso' not in tagalog


def test_candidate_info_requires_named_subject_not_a_fuzzy_generic_word(assets):
    answer, candidate = respond_to_user('paano kaya bumoto nan tama', None, assets)
    assert candidate is None
    assert not answer.startswith('###')
    answer, candidate = respond_to_user('Who is Robreddo?', None, assets)
    assert candidate == 'leni robredo'
    assert answer.startswith('### Maria Leonor')


def test_chat_app_wires_previous_topic_and_localization_instead_of_direct_translator():
    source = (ROOT / 'app.py').read_text(encoding='utf-8')
    ast.parse(source)
    assert 'previous_topic=st.session_state.last_topic' in source
    assert 'st.session_state.last_topic = topic_for_reply(' in source
    assert 'answer = localize_answer(' in source
    assert 'st.session_state.last_topic = None' in source
    assert 'st.markdown(answer)' in source
