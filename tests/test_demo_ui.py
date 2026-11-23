"""Regression checks for the public BotoBot presentation experience."""
import ast
import json
from pathlib import Path
import tomllib

import pytest
from nltk.chat.util import Chat, reflections

from nlp.classifier import train_classifier
from nlp.patterns import pairs
from nlp.query_engine import get_dynamic_tags
from nlp.response_engine import respond_to_user
from nlp.tagalog_fallback import offline_tagalog_reply
from nlp.translator import build_entity_masker

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def assets():
    candidates = json.loads((ROOT / "data/candidates.json").read_text(encoding="utf-8"))
    masker, mask_map = build_entity_masker(candidates)
    return candidates, masker, mask_map, train_classifier(), Chat(pairs, reflections), get_dynamic_tags(candidates)


def test_chat_replay_never_uses_streamlit_magic_conditional_expression():
    """Ternary st.write/markdown calls were displayed as DeltaGenerator help in the demo."""
    tree = ast.parse((ROOT / "app.py").read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.IfExp):
            assert "st." not in ast.unparse(node), "Streamlit writes must use statement-level if/else"


def test_chat_replay_renders_user_and_assistant_in_separate_branches():
    tree = ast.parse((ROOT / "app.py").read_text(encoding="utf-8"))
    branches = [node for node in ast.walk(tree)
                if isinstance(node, ast.If) and "msg['role']" in ast.unparse(node.test)]
    assert any("st.write(msg['content'])" in ast.unparse(branch.body)
               and "st.markdown(msg['content'])" in ast.unparse(branch.orelse)
               for branch in branches)


def test_magic_rendering_is_disabled_in_project_config():
    config = tomllib.loads((ROOT / ".streamlit/config.toml").read_text(encoding="utf-8"))
    assert config["runner"]["magicEnabled"] is False


def test_deprecated_container_width_has_been_removed():
    assert "use_container_width" not in (ROOT / "app.py").read_text(encoding="utf-8")


@pytest.mark.parametrize("question", [
    "saan boboto?", "Saan ako boboto?", "Where do I vote?", "Where is my polling precinct?",
])
def test_precinct_questions_route_to_official_source_without_collecting_records(question, assets):
    answer, _ = respond_to_user(question, None, assets)
    assert "precinctfinder.comelec.gov.ph" in answer
    assert "cannot access voter registration" in answer
    assert "Do not send your personal details" in answer


def test_tagalog_precinct_fallback_is_useful_without_translation(assets):
    english_answer, _ = respond_to_user("saan boboto?", None, assets)
    tagalog_answer = offline_tagalog_reply("saan boboto?", english_answer, assets[0])
    assert tagalog_answer and "presinto" in tagalog_answer
    assert "COMELEC" in tagalog_answer


def test_future_election_precinct_query_still_respects_archival_scope(assets):
    answer, _ = respond_to_user("Where do I vote in the 2028 election?", None, assets)
    assert "2022 Philippine" in answer
    assert "precinctfinder.comelec.gov.ph" not in answer


def test_streamlit_chat_history_smoke_renders_text_not_internal_objects(monkeypatch):
    """Execute the app with a tiny UI stand-in to check message display branches."""
    import runpy
    import sys
    from types import ModuleType

    rendered = []
    current_role = [None]

    class State(dict):
        def __getattr__(self, name):
            return self[name]

        def __setattr__(self, name, value):
            self[name] = value

    class Scope:
        def __init__(self, role=None):
            self.role = role

        def __enter__(self):
            current_role[0] = self.role
            return self

        def __exit__(self, *_):
            current_role[0] = None

    mock = ModuleType("streamlit")
    mock.session_state = State(messages=[
        {"role": "user", "content": "Who is Leni Robredo?"},
        {"role": "assistant", "content": "**A 2022 research profile.**"},
    ], active_candidate_key=None, response_lang="en")
    mock.sidebar = Scope()
    mock.set_page_config = lambda **kwargs: None
    mock.cache_resource = lambda **kwargs: (lambda f: f)
    mock.expander = lambda *args, **kwargs: Scope()
    mock.chat_message = lambda role, **kwargs: Scope(role)
    mock.columns = lambda n: [mock for _ in range(n)]
    mock.radio = lambda *args, **kwargs: "en"
    mock.chat_input = lambda *args, **kwargs: None
    mock.button = lambda *args, **kwargs: False

    def write(value, *args, **kwargs):
        rendered.append((current_role[0], "write", value))

    def markdown(value, *args, **kwargs):
        rendered.append((current_role[0], "markdown", value))
        return object()  # Streamlit returns a DeltaGenerator-like value.

    mock.write = write
    mock.markdown = markdown
    for name in ("title", "caption", "info", "header", "divider", "image", "error"):
        setattr(mock, name, lambda *args, **kwargs: None)
    mock.stop = lambda: pytest.fail("The research knowledge base unexpectedly failed to load")
    monkeypatch.setitem(sys.modules, "streamlit", mock)

    runpy.run_path(str(ROOT / "app.py"), run_name="__main__")
    assert ("user", "write", "Who is Leni Robredo?") in rendered
    assert ("assistant", "markdown", "**A 2022 research profile.**") in rendered
    assert all(isinstance(value, str) for role, _, value in rendered if role is not None)


def test_voting_procedure_has_clickable_comelec_precinct_reference(assets):
    response, _ = respond_to_user("How to vote?", None, assets)
    assert "[COMELEC Precinct Finder](https://precinctfinder.comelec.gov.ph/)" in response
    assert "availability may vary" in response
