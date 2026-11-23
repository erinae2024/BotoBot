"""Fast offline test suite; no Streamlit, FlashText service, or Google calls needed."""
import json
from pathlib import Path

import pytest
from nltk.chat.util import Chat, reflections

from nlp.classifier import train_classifier
from nlp.patterns import pairs
from nlp.translator import build_entity_masker, process_language
from nlp.query_engine import get_dynamic_tags, resolve_pronouns
from nlp.response_engine import respond_to_user


@pytest.fixture(scope='module')
def assets():
    data = json.loads((Path(__file__).resolve().parents[1] / 'data/candidates.json').read_text(encoding='utf-8'))
    masker, mask_map = build_entity_masker(data)
    return data, masker, mask_map, train_classifier(), Chat(pairs, reflections), get_dynamic_tags(data)


def answer(question, assets, context=None):
    return respond_to_user(question, context, assets)


def test_has_ten_2022_candidates(assets):
    assert len(assets[0]) == 10

@pytest.mark.parametrize('question', ["What are the requirements for voter's ID?", "Do I need a voter ID to vote?"])
def test_voter_id_not_conflated_with_registration(question, assets):
    txt, _ = answer(question, assets)
    assert 'put on hold' in txt
    assert 'not required to vote' in txt
    assert 'COMELEC' in txt

@pytest.mark.parametrize('question', ['How to register to vote?', 'Voter registration requirements'])
def test_registration_is_separate(question, assets):
    txt, _ = answer(question, assets)
    assert 'register' in txt.lower() and 'COMELEC' in txt

@pytest.mark.parametrize('question,number', [('What is RA 9006 law?', '9006'),('What is Republic Act 8189?', '8189'),('Tell me about RA 9369', '9369')])
def test_ra_specific_before_generic_law(question, number, assets):
    txt, _ = answer(question, assets)
    assert f'Republic Act No. {number}' in txt


def test_2022_candidate_list(assets):
    txt, _ = answer('List the 2022 presidential candidates', assets)
    assert txt.count('\n- ') == 10 and 'Historical 2022' in txt


def test_named_candidate_profile_has_sources_and_historical_age(assets):
    txt, key = answer('Who is Leni Robredo?', assets)
    assert key == 'leni robredo'
    assert '2022 research dataset' in txt
    assert 'Reference links:' in txt
    assert 'not a current-age calculation' in txt


def test_followup_pronoun_uses_context(assets):
    _, key = answer('Who is Leni Robredo?', assets)
    txt, key = answer('How old is she?', assets, key)
    assert 'Robredo' in txt and 'not their age today' in txt


def test_explicit_other_name_does_not_inject_prior_candidate(assets):
    assert resolve_pronouns('Did Bongbong Marcos create his projects?', 'leni robredo', assets[0]).lower().count('leni') == 0


def test_multi_topic_disaggregates(assets):
    txt, _ = answer('Which 2022 candidates support education, environment, and health?', assets)
    assert '**Education:**' in txt and '**Environment:**' in txt and '**Health:**' in txt
    assert 'not as an endorsement' in txt


def test_2028_candidate_request_refused(assets):
    txt, _ = answer('Who are the 2028 presidential candidates?', assets)
    assert '2022 Philippine' in txt and 'current candidate lists' in txt


def test_no_electoral_endorsements(assets):
    txt, _ = answer('Who should I vote for?', assets)
    assert 'do not recommend' in txt


def test_offtopic_question_safely_declined(assets):
    txt, _ = answer('What is the meaning of life?', assets)
    assert 'could not confidently match' in txt


def test_unknown_candidate_not_misrepresented_as_list(assets):
    txt, _ = answer('Who is Zorglan?', assets)
    assert 'cannot identify' in txt and '2022 candidate database' in txt


def test_unverified_project_does_not_automatically_downgrade_to_profile(assets):
    txt, _ = answer('Did Leni Robredo create Bangui Windmills?', assets)
    assert 'cannot verify' in txt


def test_known_candidate_project_query(assets):
    txt, _ = answer("What are Leni Robredo's projects?", assets)
    assert 'Angat Buhay' in txt


def test_voting_procedure_from_original_patterns(assets):
    txt, _ = answer('How to vote?', assets)
    assert 'voting precinct' in txt and 'ballot' in txt

@pytest.mark.parametrize('tagalog', ['Paano bumoto?', 'Sino si Leni Robredo?'])
def test_common_tagalog_offline_fallback(tagalog, assets):
    txt, _ = answer(tagalog, assets)
    assert txt and 'could not confidently match' not in txt


def test_entity_preserving_masking(assets):
    translated, detected = process_language('Sino si Leni Robredo?', assets[1], assets[2], target_lang='en')
    assert detected is True and 'leni' in translated.lower()


def test_long_input_rejected(assets):
    txt, _ = answer('x'*1300, assets)
    assert '1,200' in txt


def test_empty_input_rejected(assets):
    txt, _ = answer('  ', assets)
    assert 'Please enter' in txt


def test_paper_authorship_not_replaced_by_contact_role():
    app = (Path(__file__).resolve().parents[1] / 'app.py').read_text(encoding='utf-8')
    assert 'Lead developer' in app or 'lead developer' in app
    assert 'Dr. Maria Art Antonette D. Clariño' in app
    assert 'Erin A. Evangelio' in app
    assert 'Zachary Andre A. Cruz' in app
    assert 'Alaine Carlo R. Magdaluyo' in app

@pytest.mark.parametrize('question,expected', [
    ('What is the Fair Election Act?', 'RA 9006'),
    ('What does Article V Section 1 mean?', 'Suffrage'),
    ('What is Article VII Section 2?', 'Qualifications for President'),
    ('What is Section 261(a)?', 'Section 261(a)'),
    ('How many candidates were there in 2022?', '10 presidential candidates'),
    ('Do I need a National ID to vote?', 'not a general requirement'),
    ('What is the penalty for vote buying?', 'one to six years'),
    ('Paano bumoto?', 'voting precinct'),
    ('Ano ang RA 9006?', 'Republic Act No. 9006'),
    ('Who is Leni Robredo?', 'Research'),
])
def test_conference_questions(question, expected, assets):
    txt, _ = answer(question, assets)
    assert expected.lower() in txt.lower()


def test_constitution_section_is_not_mislabelled_as_omnibus(assets):
    txt, _ = answer('What is Article V Section 1?', assets)
    assert 'Omnibus' not in txt


def test_legal_alias_is_not_misclassified_as_a_candidate_project(assets):
    txt, _ = answer('Tell me about the Fair Election Act', assets, 'leni robredo')
    assert 'RA 9006' in txt and 'Sangguniang Kabataan' not in txt


def test_all_source_urls_have_https_syntax(assets):
    from urllib.parse import urlparse
    for person in assets[0].values():
        urls = list(person.get('links', []))
        for project in person.get('projects', []):
            link = project.get('link', [])
            urls.extend(link if isinstance(link, list) else [link])
        for url in urls:
            parsed = urlparse(url)
            assert parsed.scheme == 'https' and parsed.netloc


def test_app_discloses_translation_processing(assets):
    app = (Path(__file__).resolve().parents[1] / 'app.py').read_text(encoding='utf-8')
    assert 'third-party translation provider' in app


def test_source_dataset_unchanged_ten_candidates(assets):
    assert set(assets[0]) == {
        'ernesto abella', 'leni robredo', 'leody de guzman', 'isko moreno',
        'norberto gonzales', 'panfilo lacson', 'faisal mangondato',
        'bongbong marcos', 'jose montemayor jr', 'manny pacquiao'
    }

@pytest.mark.parametrize('question,keyword', [
    ('Paano bumoto?', 'presinto'),
    ("What are the requirements for a voter's ID?", 'Hindi kailangan'),
    ('Ano ang RA 9006?', 'Fair Election Act'),
])
def test_offline_tagalog_templates(question, keyword, assets):
    from nlp.tagalog_fallback import offline_tagalog_reply
    result, _ = answer(question, assets)
    tl = offline_tagalog_reply(question, result, assets[0])
    assert tl is not None and keyword in tl
