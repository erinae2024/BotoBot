"""Entity-preserving bilingual translation for the published BotoBot architecture.

External translation is best-effort. A failed network call must never crash BotoBot,
and untranslated Tagalog must never be mistaken for validated English.
"""
import re

try:
    from flashtext import KeywordProcessor
except ImportError:  # Development/QA fallback; production uses flashtext.
    KeywordProcessor = None

try:
    from deep_translator import GoogleTranslator
except ImportError:  # Production dependencies are declared in requirements.txt.
    GoogleTranslator = None

# Preserve the heuristic described in the research paper.
TAGALOG_TRIGGERS = r'(?i)\b(boto|bumoto|halalan|eleksyon|botohan|sino|ano|paano|saan|bakit|kailan|mga|niya|tungkol|ba|proyekto|kredensyal)\b'


class _LocalKeywordProcessor:
    """Fallback matcher when flashtext is unavailable in an offline test env."""
    def __init__(self):
        self.words = {}

    def add_keyword(self, word, replacement):
        self.words[word.lower()] = replacement

    def replace_keywords(self, text):
        if not self.words:
            return text
        pattern = r'(?<!\w)(?:' + '|'.join(re.escape(x) for x in sorted(self.words, key=len, reverse=True)) + r')(?!\w)'
        return re.sub(pattern, lambda match: self.words[match.group().lower()], text, flags=re.IGNORECASE)


def build_entity_masker(candidates_data):
    processor = KeywordProcessor(case_sensitive=False) if KeywordProcessor else _LocalKeywordProcessor()
    replacement_map = {}
    index = 0
    for data in candidates_data.values():
        words = [data['full_name'], *data.get('aliases', []),
                 *(project['name'] for project in data.get('projects', []))]
        for word in words:
            placeholder = f"ENT{index:04d}X"
            processor.add_keyword(word, placeholder)
            replacement_map[placeholder] = word
            index += 1
    return processor, replacement_map


def process_language(text, masker, mask_map, target_lang='en'):
    """Return (best-effort translated text, whether Tagalog markers were detected).

    This is *not* an accuracy certificate. The external translation provider can fail;
    callers should acknowledge that output may fall back to original language.
    """
    detected_tl = bool(re.search(TAGALOG_TRIGGERS, text))
    if not detected_tl and target_lang != 'tl':
        return text, False

    # Mask URLs first, then entities; preserve hyperlinks and proper nouns.
    url_map = {}
    def replace_url(match):
        placeholder = f"URL{len(url_map):04d}X"
        url_map[placeholder] = match.group()
        return placeholder
    masked = re.sub(r'https?://[^\s()<>]+', replace_url, text)
    masked = masker.replace_keywords(masked)
    translated = masked
    if GoogleTranslator:
        try:
            result = GoogleTranslator(source='auto', target=target_lang).translate(masked)
            if isinstance(result, str) and result.strip() and not any(
                phrase in result.lower() for phrase in ('error 500', 'please try again later')
            ):
                placeholders = re.findall(r'(?:ENT|URL)\d{4}X', masked)
                if all(result.count(key) == masked.count(key) for key in set(placeholders)):
                    translated = result
        except Exception:
            pass

    if translated == masked:
        return text, detected_tl

    for key, value in mask_map.items():
        translated = translated.replace(key, value)
    for key, value in url_map.items():
        translated = translated.replace(key, value)
    return translated, detected_tl
