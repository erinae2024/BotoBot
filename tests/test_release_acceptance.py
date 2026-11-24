"""Independent dialogue regressions for routing, scope, and localization."""
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
from nlp.translator import build_entity_masker, process_language


@pytest.fixture(scope='module')
def assets():
    candidates = json.loads((Path(__file__).resolve().parents[1] / 'data/candidates.json').read_text(encoding='utf-8'))
    masker, masks = build_entity_masker(candidates)
    return candidates, masker, masks, train_classifier(), Chat(pairs, reflections), get_dynamic_tags(candidates)


@pytest.fixture(autouse=True)
def offline(monkeypatch):
    monkeypatch.setattr('nlp.translator.GoogleTranslator', None)


def dialogue(assets, prompts, language='tl'):
    key = topic = None
    results = []
    for prompt in prompts:
        answer, next_key = respond_to_user(prompt, key, assets, previous_topic=topic)
        topic = topic_for_reply(prompt, answer, topic)
        key = next_key if topic == 'candidate' else None
        displayed = localize_answer(prompt, answer, language, *assets[:3])
        results.append((answer, displayed, key))
    return results


@pytest.mark.parametrize('prompts,expected', [
    (['paano magparehistro?', 'ano kailangan?'], 'Pagpaparehistro'),
    (['pano magparehistro', 'saan?'], 'Pagpaparehistro'),
    (['paano bumoto?', 'saan?'], 'Saan boboto?'),
    (['How do I vote?', 'okay', 'where?'], 'Saan boboto?'),
    (['Who is Leni Robredo?', 'how old is she?'], 'Edad ni'),
    (['Who is Leni Robredo?', 'how old is she?', 'what are her projects?'], 'gawaing lehislatibo'),
    (['Who is Leni Robredo?', 'how can I vote?', 'who is she?'], 'Hindi ko matukoy'),
    (['Who is Ping?', 'hello', 'ano ang buhay?'], 'Hindi ko matukoy'),
    (['What is RA 10649?', 'ano ang buhay?'], 'Hindi ko matukoy'),
    (['What is RA 9006?', 'What is RA 10649?'], 'Wala akong beripikadong'),
    (['Who is Leni Robredo?', 'sino ba dapat kong iboto?'], 'Hindi nagrerekomenda'),
    (['How do I vote?', 'sino pinakamagaling?'], 'Hindi nagrerekomenda'),
    (['List the 2022 presidential candidates', 'who would you vote for?'], 'Hindi nagrerekomenda'),
    (['Who is the president now?', 'sino presidente ngayon?'], 'susunod na eleksyon'),
    (['Who is Leni Robredo?', 'sino ang mga kandidato sa susunod na eleksyon?'], 'susunod na eleksyon'),
    (['Who is Ping?', '2024 presidential candidates'], 'susunod na eleksyon'),
    (['How do I vote?', 'pwede ba ako bumoto'], 'Kwalipikasyon'),
    (['Paano bumoto?', 'can i vote at 17?'], 'Kwalipikasyon'),
    (['What is RA 9006?', 'Who is Leni and Marcos?'], 'isang kandidato'),
    (['bili ng boto', 'sige'], 'Walang anuman'),
])
def test_independent_multiturn_scenarios(assets, prompts, expected):
    result = dialogue(assets, prompts)
    assert expected.casefold() in result[-1][1].casefold(), result[-1]
    if expected not in ('Edad ni', 'gawaing lehislatibo'):
        assert not result[-1][0].startswith('### ')


def test_tagalog_unknown_reply_is_not_a_law_explanation(assets):
    english, display, _ = dialogue(assets, ['what is the meaning of life?'])[-1]
    assert 'Hindi ko matukoy' in display
    assert not display.startswith('**Republic Act 9006')


def test_known_law_section_does_not_invent_section_contents(assets):
    answer, display, _ = dialogue(assets, ['What is Section 4 of RA 9006?'])[-1]
    assert 'cannot reliably summarize' in answer
    assert 'lawphil.net/statutes/repacts/ra2001/ra_9006_2001.html' in answer
    assert 'cannot reliably summarize' in display


def test_translation_drops_corrupted_placeholders(assets, monkeypatch):
    class BrokenTranslator:
        def __init__(self, **kwargs):
            pass
        def translate(self, text):
            return 'Translated but missing protected references'
    monkeypatch.setattr('nlp.translator.GoogleTranslator', BrokenTranslator)
    original = 'Sino si Leni Robredo? https://www.comelec.gov.ph/'
    result, _ = process_language(original, assets[1], assets[2])
    assert result == original


def test_response_translation_failure_preserves_original(assets, monkeypatch):
    def failed(*args, **kwargs):
        raise RuntimeError('provider unavailable')
    monkeypatch.setattr('nlp.tagalog_fallback.process_language', failed)
    english = 'An answer outside the offline templates.'
    result = localize_answer('question', english, 'tl', *assets[:3])
    assert english in result and 'Hindi available' in result
