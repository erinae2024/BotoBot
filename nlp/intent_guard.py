"""Conservative, bilingual intent guards for the existing BotoBot research pipeline.

Deterministic routing precedes the published regex/Naive-Bayes/fuzzy tiers for
high-impact voter-information topics. This is not a new generative model.
"""
import re


_VOTING_WORD = r'(?:vot(?:e|ing)|ballot|boto|bumoto|boboto|pagboto|iboboto|pag[- ]?boto)'
_VOTE_BUYING = re.compile(
    r'\b(?:vote[- ]?(?:buying|selling)|buy(?:ing)?\s+votes?|sell(?:ing)?\s+votes?|'
    r'(?:bumili|bili)\s+ng\s+boto|bilihan\s+ng\s+boto|bayad\s+(?:para\s+sa\s+)?boto|'
    r'suhol\s+(?:sa\s+)?(?:boto|botante))\b', re.I)
_REGISTRATION = re.compile(
    r'\b(?:register|registration|registr(?:ation)?\s+to\s+vote|rehistro|magparehistro|'
    r'pagpaparehistro|mag[- ]?register)\b', re.I)


def is_vote_buying_question(text):
    return bool(_VOTE_BUYING.search(text))


def is_registration_question(text):
    if re.search(r'\b(?:magparehistro|pagpaparehistro|rehistro|mag[- ]?register)\b', text, re.I):
        return True
    return bool(_REGISTRATION.search(text) and re.search(
        r'\b(?:vot\w*|elect\w*|boto|botante|halalan|eleksyon|voter|pagboto)\b', text, re.I))


def is_precinct_question(text):
    return bool(re.search(
        r'\b(?:saan\s+(?:(?:ba|po|ako|ba\s+ako)\s+)?(?:boboto|bumoboto)|'
        r'(?:where|which\s+precinct)\s+(?:(?:do|can|should|will)\s+)?'
        r'(?:(?:i|we)\s+)?vote|polling\s+(?:place|precinct)|voting\s+precinct|'
        r'presinto\s+ko|aking\s+presinto)\b', text, re.I))


def is_voting_procedure_question(text):
    """Detect voting *steps*, not a recommendation, law, or unrelated profile.

    This intentionally handles colloquial Tagalog (even misspelled 'nan tama')
    without sending such text through fuzzy candidate matching.
    """
    if is_vote_buying_question(text) or is_registration_question(text) or is_precinct_question(text):
        return False
    t = re.sub(r'\s+', ' ', text.casefold()).strip()
    if re.search(r'\bhow\s+(?:do|can|could|should|would)\s+(?:(?:i|we|you|she|he|they)\s+)?'
                 r'(?:(?:actually|properly|correctly)\s+)?(?:vote|cast\s+(?:(?:my|a|the)\s+)?(?:vote|ballot))\b', t):
        return True
    if re.search(r'\bhow\s+to\s+(?:(?:properly|correctly)\s+)?vote\b', t):
        return True
    if re.search(r'\bi\s+(?:wanna|want\s+to|would\s+like\s+to|need\s+to|am\s+ready\s+to)\s+vote\b', t):
        return True
    if re.search(r'\b(?:gusto|nais)\s+(?:kong|ko|naming|namin|niyang|niya|nating|natin)\s+'
                 r'(?:bumoto|boboto|mag[- ]?boto)\b', t):
        return True
    if re.search(r'\b(?:voting|pagboto|boto)\s+(?:process|proseso|procedure|steps?|hakbang|paraan)\b', t):
        return True
    if re.search(r'\bhow\s+(?:(?:does|do)\s+)?(?:voting|the\s+vote)\s+work\b', t):
        return True
    # Colloquial constructions: "paano kaya bumoto nan tama", "pano ba ako boboto".
    if re.search(r'\b(?:paano|pano)\b(?:\s+\w+){0,6}\s+'
                 r'(?:bumoto|boboto|pagboto|mag[- ]?boto|mag[- ]?vote|iboboto)\b', t):
        return True
    # "ano ang proseso nung boto?", "paano process ng voting".
    if re.search(r'\b(?:proseso|process|procedure|steps?|hakbang|paraan)\b'
                 r'(?:\s+\w+){0,5}\s+' + _VOTING_WORD + r'\b', t):
        return True
    if re.search(r'\b(?:paano|pano|ano)\b(?:\s+\w+){0,5}\s+'
                 r'(?:proseso|process|procedure|steps?|hakbang|paraan)\b'
                 r'(?:\s+\w+){0,5}\s+' + _VOTING_WORD + r'\b', t):
        return True
    if re.search(r'\b(?:bumoto|boboto|pagboto)\b(?:\s+\w+){0,4}\s+'
                 r'(?:tama|maayos|properly|correctly)\b', t):
        return True
    return False


def is_ambiguous_process_followup(text):
    """No fabricated context: require prior voting topic to answer this."""
    return bool(re.fullmatch(
        r'(?i)\s*(?:(?:okay|ok|sige|edi|eh|then|so|ano|what|paano|pano|ang|yung|nung|the|is|it|po|ba|naman)\s+)*'
        r'(?:process|proseso|procedure|steps?|hakbang|paraan)\s*[?.! ]*', text))


def topic_for_reply(question, answer, previous_topic=None):
    """Track only demonstrated topic context; acknowledgments retain it."""
    if re.fullmatch(r'(?i)\s*(?:ok|okay|sige|salamat|thanks?|thank\s+you|ty)[!. ]*', question):
        return previous_topic
    if answer.startswith('To vote in Philippine elections:'):
        return 'voting_procedure'
    if answer.startswith('**To register as a voter:**'):
        return 'registration'
    if answer.startswith('**Voter eligibility'):
        return 'eligibility'
    if answer.startswith('**Where do I vote?'):
        return 'precinct'
    if answer.startswith('**Vote-buying'):
        return 'vote_buying'
    if answer.startswith(('### ', '**Age recorded in the 2022 dataset for ', 'Selected projects, programs, and legislative activities listed for **')):
        return 'candidate'
    return None
