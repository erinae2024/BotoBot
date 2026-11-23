"""Checks for representative real-world questions and verified source relevance."""
import json
from pathlib import Path

import pytest
from nltk.chat.util import Chat, reflections

from nlp.classifier import train_classifier
from nlp.patterns import pairs
from nlp.query_engine import get_dynamic_tags
from nlp.response_engine import respond_to_user
from nlp.tagalog_fallback import offline_tagalog_reply
from nlp.translator import build_entity_masker

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope='module')
def assets():
    candidates = json.loads((ROOT / 'data/candidates.json').read_text(encoding='utf-8'))
    masker, mask_map = build_entity_masker(candidates)
    return candidates, masker, mask_map, train_classifier(), Chat(pairs, reflections), get_dynamic_tags(candidates)


@pytest.mark.parametrize('question', [
    'How do I vote?',
    'How can I vote i mean',
    'but how can she vote?',
    'I wanna vote',
    'i wanna vote how',
    'I want to vote',
    'How do we vote?',
    'How to vote?',
    'How can I cast my vote?',
    'Paano ako boboto?',
    'pano bumoto',
    'gusto kong bumoto',
    'Paano bumoto?',
])
def test_natural_voting_phrasing_returns_ballot_steps(question, assets):
    answer, _ = respond_to_user(question, None, assets)
    assert 'voting precinct' in answer.lower()
    assert 'ballot' in answer.lower()
    assert 'precinctfinder.comelec.gov.ph' in answer
    assert 'cannot identify that person' not in answer.lower()


def test_pronoun_context_does_not_turn_voting_steps_into_candidate_search(assets):
    _, key = respond_to_user('Who is Leni Robredo?', None, assets)
    assert key == 'leni robredo'
    answer, next_key = respond_to_user('but how can she vote?', key, assets)
    assert 'voting precinct' in answer.lower()
    assert next_key == key


@pytest.mark.parametrize('question', ['okay', 'ok', 'thanks', 'thank you', 'salamat', 'sige'])
def test_acknowledgment_is_not_a_candidate_lookup(question, assets):
    answer, _ = respond_to_user(question, None, assets)
    assert 'you can ask' in answer.lower()
    assert 'could not confidently match' not in answer.lower()


@pytest.mark.parametrize('question', ['yoko na', 'ayoko na', 'tama na', "that's all", 'bye'])
def test_conversation_end_is_handled_normally(question, assets):
    answer, _ = respond_to_user(question, None, assets)
    assert 'return whenever' in answer.lower()


@pytest.mark.parametrize('question,expected', [
    ('Where do I vote?', 'cannot access voter registration'),
    ('Who should I vote for?', 'do not recommend or endorse'),
    ('How do I vote in 2028?', '2022 Philippine presidential candidates'),
    ('What is the penalty for vote buying?', 'one to six years'),
    ('Who is Leni Robredo?', 'Maria Leonor'),
    ('How do I register to vote?', 'COMELEC'),
])
def test_similar_wording_does_not_override_critical_routes(question, expected, assets):
    answer, _ = respond_to_user(question, None, assets)
    assert expected.lower() in answer.lower()


@pytest.mark.parametrize('question', ['I wanna vote', 'how can i vote', 'Paano ako boboto?'])
def test_offline_tagalog_voting_response_works_for_natural_phrases(question, assets):
    answer, _ = respond_to_user(question, None, assets)
    tagalog = offline_tagalog_reply(question, answer, assets[0])
    assert tagalog is not None
    assert 'presinto' in tagalog.lower()
    assert 'COMELEC' in tagalog


def test_leni_citation_is_relevant_to_actual_legislative_role(assets):
    leni = assets[0]['leni robredo']
    links = leni['links']
    assert len(links) == 4
    assert all('ra_10649_2014' not in url for url in links)
    assert 'house-bill-no-5831' in links[-1]
    timta = next(p for p in leni['projects'] if 'RA 10708' in p['name'])
    assert 'House conference-committee member' in timta['name']
    assert any('house-bill-no-5831' in url for url in timta['link'])
    answer, _ = respond_to_user('Who is Leni Robredo?', None, assets)
    assert 'Senate legislative record' in answer
    assert 'ra_10649' not in answer


def test_candidate_profile_explains_that_acts_are_legislative_activities(assets):
    answer, _ = respond_to_user('Who is Leni Robredo?', None, assets)
    assert 'legislative activities recorded' in answer
    assert 'not imply endorsement or verify all claims' in answer
