"""Pure, testable response generation for the BotoBot O-COCOSDA research demo.

Scope stays 2022 presidential candidates, static cited election-law information,
and registration/voting procedures. NOT a real-time election advice service.
"""
import re
from urllib.parse import urlparse

from nltk.chat.util import Chat, reflections
from rapidfuzz import fuzz

from nlp.patterns import pairs
from nlp.translator import process_language
from nlp.intent_guard import (
    is_voting_procedure_question, is_ambiguous_process_followup,
    is_vote_buying_question, is_precinct_question, is_registration_question,
)
from nlp.classifier import get_intent
from nlp.query_engine import (
    resolve_pronouns, extract_and_normalize_slots, get_dynamic_tags,
    match_candidates_by_tag, get_candidate_projects, verify_project_association,
)

COMELEC_VOTER_ID = 'https://www.comelec.gov.ph/index.html?r=VoterRegistration%2FWhatisVoterRegistration%2FVoterIDIssuance'
COMELEC_REGISTRATION = 'https://www.comelec.gov.ph/index.html?r=VoterRegistration%2FWhatisVoterRegistration%2FRegistrationRequirements'
CONSTITUTION = 'https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/3/353'
LEGAL = {
    '9006': ('Fair Election Act', 'https://lawphil.net/statutes/repacts/ra2001/ra_9006_2001.html'),
    '9369': ('Automated Election System amendments', 'https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/2/7412'),
    '8189': ('Voter Registration Act', 'https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/2/4068'),
    '7166': ('Synchronized National and Local Elections', 'https://www.officialgazette.gov.ph/1991/11/26/republic-act-no-7166/'),
}
OUT_OF_SCOPE = ('BotoBot is a research demonstration focused on the **2022 Philippine presidential candidates** '
                'and selected election rules. I cannot provide current candidate lists, election predictions, '
                'endorsements, or live election updates. For current information, use [COMELEC](https://www.comelec.gov.ph/).')


def _urls(values):
    result = []
    for value in values or []:
        if not isinstance(value, str):
            continue
        p = urlparse(value)
        if p.scheme == 'https' and p.netloc:
            result.append(value)
    return result


def _source_name(url):
    """Use informative publisher labels instead of uninformative Source 1/2 links."""
    host = (urlparse(url).hostname or '').removeprefix('www.')
    names = {
        'gmanetwork.com': 'GMA News',
        'abs-cbn.com': 'ABS-CBN',
        'hks.harvard.edu': 'Harvard Kennedy School',
        'issuances-library.senate.gov.ph': 'Senate legislative record',
        'ldr.senate.gov.ph': 'Senate legislative record',
        'newsinfo.inquirer.net': 'Inquirer',
        'rappler.com': 'Rappler',
        'southpointschool.edu.ph': 'Southpoint School',
        'lawphil.net': 'Lawphil',
    }
    return names.get(host, host)


def _profile(key, candidates):
    if not key or key not in candidates:
        return 'Which **2022 presidential candidate** do you mean?'
    c = candidates[key]
    lines = [f"### {c['full_name']}",
             f"**Age recorded in the 2022 research dataset:** {c.get('age', 'Not listed')} (not a current-age calculation)",
             '**Positions listed in the research dataset:** ' + '; '.join(c.get('positions', []) or ['Not listed']),
             '**Education listed:** ' + '; '.join(c.get('education', []) or ['Not listed']),
             '**Projects, programs and legislative activities recorded:** ' + '; '.join(p.get('name', 'Unspecified') for p in c.get('projects', []))]
    urls = _urls(c.get('links', []))
    if urls:
        lines.append('**Reference links:** ' + ' · '.join(f'[{_source_name(url)}]({url})' for url in urls))
    lines.append('*Historical 2022 candidate profile; listing does not imply endorsement or verify all claims.*')
    return '\n\n'.join(lines)


def _requested_tags(query, candidates):
    return [tag for tag in get_dynamic_tags(candidates) if re.search(r'(?<!\w)' + re.escape(tag) + r'(?!\w)', query, re.I)]


def _multi_topic(query, candidates, key):
    tags = _requested_tags(query, candidates)
    if not tags:
        return None
    wants_topic = bool(re.search(r'\b(which|who|what|candidates?|prioritiz\w*|support\w*|focus\w*|advocat\w*|issue|topic|tag|policy|environment|education|health)\b', query, re.I))
    if not wants_topic:
        return None
    if len(tags) == 1:
        return match_candidates_by_tag(query, candidates, key)
    blocks = ['**2022 research-dataset topic matches** (shown by topic, not as an endorsement):']
    for tag in tags:
        matched = []
        for c in candidates.values():
            tags_for_candidate = set(c.get('tags', []))
            for proj in c.get('projects', []):
                tags_for_candidate.update(proj.get('tags', []))
            if tag in tags_for_candidate or (tag == 'government experience' and c.get('has_gov_experience')):
                matched.append(c['full_name'])
        blocks.append(f"- **{tag.title()}:** " + (', '.join(matched) if matched else 'No tagged entries'))
    blocks.append('*These are database tags, not a comprehensive review of platforms or evidence of current positions.*')
    return '\n'.join(blocks)


def _voter_id_response():
    return ("**Voter's ID card is different from voter registration.** COMELEC states that the creation and "
            "distribution of new voter's ID cards have been put on hold; an ID card is **not required to vote**. "
            "To **register as a voter**, follow the registration procedure and identification requirements "
            "published by COMELEC. The research paper identified confusion between these two questions.\n\n"
            f"Sources: [COMELEC on voter-ID cards]({COMELEC_VOTER_ID}) · "
            f"[Registration requirements]({COMELEC_REGISTRATION})")


def _registration_response():
    return ("**To register as a voter:** Confirm your legal eligibility, check COMELEC's currently applicable "
            "registration procedure and schedule, bring accepted identification, and submit the required "
            "application through the proper COMELEC registration channel. Do not confuse voter registration "
            "with getting a voter's ID card. Requirements and schedules may change.\n\n"
            f"Official source: [COMELEC registration requirements]({COMELEC_REGISTRATION})")



def _precinct_response():
    return ("**Where do I vote? / Saan boboto?** BotoBot cannot access voter registration "
            "records or determine your assigned polling place. For election-specific precinct "
            "information, use the [COMELEC Precinct Finder](https://precinctfinder.comelec.gov.ph/) "
            "when available, or contact your local COMELEC election office. The service may "
            "not be available outside election periods. Do not send your personal details "
            "to this chatbot. [COMELEC official website](https://www.comelec.gov.ph/).")


def _strong_candidate_reference(text, key, candidates):
    """Reject fuzzy candidate matches from ordinary non-name words.

    Exact candidate names/aliases are always accepted. Approximate spellings
    require an explicit candidate-information request and a close match to a
    distinctive alias, not arbitrary 3-grams within a voting question.
    """
    if not key or key not in candidates:
        return False
    data = candidates[key]
    aliases = [data['full_name'], *data.get('aliases', [])]
    if any(re.search(r'(?<!\w)' + re.escape(alias) + r'(?!\w)', text, re.I)
           for alias in aliases if len(alias) >= 3):
        return True
    if not re.search(r'\b(?:who\s+is|who\s+was|sino\s+si|sino\s+ang|tell\s+me\s+about|'
                     r'profile|biography|info(?:rmation)?\s+about|how\s+old\s+is|'
                     r'projects?\s+of|about\s+the\s+candidate)\b', text, re.I):
        return False
    tokens = re.findall(r'[a-z]{5,}', text.casefold())
    distinctive = [part.casefold() for alias in aliases for part in alias.split()
                   if len(part) >= 5]
    # A meaningful single-word near match such as "Robreddo" remains supported.
    return any(fuzz.ratio(token, alias) >= 87 for token in tokens for alias in distinctive)


def _explicit_project_reference(text, project):
    if not project:
        return False
    if project.casefold() in text.casefold():
        return True
    # Broad project triggers are not evidence; require a distinctive sequence.
    project_tokens = [token for token in re.findall(r'[a-z]{5,}', project.casefold())
                      if token not in {'project', 'program', 'voting', 'election',
                                       'senate', 'republic', 'national', 'government',
                                       'voters', 'registration', 'philippines'}]
    return any(re.search(r'(?<!\w)' + re.escape(token) + r'(?!\w)', text, re.I)
               for token in project_tokens)


def _voting_procedure_response():
    return ('To vote in Philippine elections:\n\n'
            '1. Go to your assigned voting precinct on election day.\n'
            '2. Get your official ballot from the Electoral Board.\n'
            '3. Fully shade the oval beside your chosen candidate on the ballot.\n'
            '4. Follow the Electoral Board instructions for the Vote Counting Machine and voter receipt.\n\n'
            'Check your assigned precinct using the '
            '[COMELEC Precinct Finder](https://precinctfinder.comelec.gov.ph/) '
            '(availability may vary by election period). For current voting procedures, '
            'always follow [COMELEC](https://www.comelec.gov.ph/).')


def _short_conversation_reply(text):
    """Avoid treating acknowledgments as failed 2022 candidate lookups."""
    if re.fullmatch(r'\s*(?:ok|okay|okey|sige|thanks?|thank you|ty|salamat|salamat po)[.!? ]*', text, re.I):
        return 'You’re welcome! You can ask about a 2022 candidate, an election law, or how voting works.'
    if re.fullmatch(r'\s*(?:ayoko na|yoko na|tama na|no thanks|that\'s all|stop|bye|goodbye|paalam)[.!? ]*', text, re.I):
        return 'Okay. Feel free to return whenever you want to explore the 2022 research information.'
    return None


def _candidate_list(candidates):
    return ('**2022 Philippine presidential candidates in the research database:**\n\n'
            + '\n'.join(f"- {x['full_name']}" for x in candidates.values())
            + '\n\n*Historical 2022 list, not a current election candidate list.*')


def respond_to_user(text, active_candidate_key, assets, previous_topic=None):
    """Return (markdown answer, next active candidate key). No Streamlit imports."""
    candidates, masker, mask_map, classifier, chatbot, _ = assets
    text = text.strip()
    if not text:
        return 'Please enter a question about the 2022 Philippine presidential election.', active_candidate_key
    if len(text) > 1200:
        return 'Please shorten your question to 1,200 characters or fewer.', active_candidate_key

    conversation_reply = _short_conversation_reply(text)
    if conversation_reply is not None:
        return conversation_reply, active_candidate_key

    # Guard both the published temporal boundary and the political neutrality boundary.
    if (re.search(r'\b(who should i vote|who do you endorse|recommend (a |which )?candidate|best candidate|vote for me)\b', text, re.I)
            or re.search(r'\b(?:sino(?:ng)?|sino ang|sino ba ang)\s+(?:ang\s+)?(?:dapat\s+)?'
                         r'(?:(?:ko|kong|namin|naming)\s+)?(?:iboto|botohin)\b', text, re.I)
            or re.search(r'\b(?:sinong\s+dapat\s+(?:ko|kong)\s+iboto|'
                         r'kaninong\s+kandidato\s+ang\s+dapat\s+kong\s+iboto)\b', text, re.I)):
        return ('I do not recommend or endorse candidates. I can present source-linked historical '
                'profiles from the 2022 dataset so you can make your own assessment.'), active_candidate_key
    if re.search(r'\b(2025|2026|2027|2028|2029|2030|current|upcoming|latest|today|this year|next election)\b', text, re.I) and re.search(r'\b(candidate|presiden|election|vote|voting|poll|registration|kandidato|eleksyon|eleksiyon|halalan|boto|bumoto|boboto|pagboto|presinto|rehistro)\w*', text, re.I):
        return OUT_OF_SCOPE, active_candidate_key

    # A precinct is a personal, election-specific record: route to COMELEC, never guess.
    if is_precinct_question(text):
        return _precinct_response(), active_candidate_key

    # Specific electoral offenses/registration win over the generic word "boto".
    if (is_vote_buying_question(text)
            and re.search(r'\b(?:penalt(?:y|ies)|punishment|prison|imprisonment|jail|'
                          r'parusa|pagkakakulong|kulong)\b', text, re.I)):
        return ('**Vote-buying and vote-selling:** Section 261(a) of BP 881 defines the '
                'offenses, and Section 264 provides the general penalty of '
                '**one to six years of imprisonment** for covered election offenses, '
                'subject to the applicable statute and case circumstances. '
                '[COMELEC — Omnibus Election Code]('
                'https://www.comelec.gov.ph/?r=References/RelatedLaws/OmnibusElectionCode/OECArt22). '
                'This is general legal information, not a case-specific ruling.'), active_candidate_key
    if is_vote_buying_question(text):
        return ('**Vote-buying and vote-selling** are election offenses under Section 261(a) '
                'of BP 881 (Omnibus Election Code). Offering or accepting money or valuable '
                'consideration to influence voting may constitute an offense. '
                'For the legal text and current complaint channels, refer to '
                '[COMELEC](https://www.comelec.gov.ph/). '
                'This is general historical/legal information, not case-specific advice.'), active_candidate_key
    # The ID-card distinction must take precedence over registration keywords.
    # Example: "Is voter-ID the same as voter registration?"
    if re.search(r"\bvoter[’']?s?\s*(?:id|identification card)\b|\bvoters?[- ]?id\b",
                 text, re.I):
        return _voter_id_response(), active_candidate_key
    if is_registration_question(text):
        return _registration_response(), active_candidate_key

    # Recognize voting steps before fuzzy candidate/project matching or Naive Bayes.
    if is_voting_procedure_question(text):
        return _voting_procedure_response(), active_candidate_key
    if is_ambiguous_process_followup(text):
        if previous_topic == 'voting_procedure':
            return _voting_procedure_response(), active_candidate_key
        return ('Do you mean **how to cast a ballot**? If so, I can explain '
                'the general voting process. I do not have access to personal '
                'voter records.'), active_candidate_key

    resolved = resolve_pronouns(text, active_candidate_key, candidates)
    translated, _ = process_language(resolved, masker, mask_map, target_lang='en')
    # Small offline mappings for common Tagalog prompts. Does not create new factual content.
    normalized = translated.lower().strip()
    if re.search(r'\b(paano|ano|sino|mga|bumoto|eleksyon)\b', normalized):
        normalized = re.sub(r'\bpaano\s+bumoto\b', 'how to vote', normalized)
        normalized = re.sub(r'\bsino\s+(?:si|ang)\b', 'who is', normalized)
        normalized = re.sub(r'\bmga\s+kandidato\b', 'candidates', normalized)
        normalized = re.sub(r'\bproyekto\b', 'projects', normalized)
    else:
        normalized = translated

    # Critical fixes must precede broad regex matching and statistical classification.
    if re.search(r'\b(penalt(?:y|ies)|punishment|prison|imprisonment|jail)\b', normalized, re.I) and re.search(r'\b(vote[- ]?buying|vote[- ]?selling|buying votes|selling votes)\b', normalized, re.I):
        return ('**Vote-buying and vote-selling:** Section 261(a) of BP 881 defines the offenses, '
                'and Section 264 provides the general penalty of **one to six years of imprisonment** '
                'for covered election offenses, subject to the applicable statute and case circumstances. '
                '[COMELEC — Omnibus Election Code](https://www.comelec.gov.ph/?r=References/RelatedLaws/OmnibusElectionCode/OECArt22). '
                'This is general legal information, not a case-specific ruling.'), active_candidate_key
    # Source-specific constitutional and electoral exceptions take priority.
    if re.search(r'\b(?:fair election act)\b', normalized, re.I):
        name, url = LEGAL['9006']
        return (f'**RA 9006 — {name}.** The Act addresses fair election practices, campaign '
                f'propaganda, and related media rules. [Read the statute]({url}).'), active_candidate_key
    if re.search(r'\b(?:article|art\.?)\s*(?:v|5)\s*(?:section|sec\.?)\s*1\b', normalized, re.I):
        return ('**Article V, Section 1 — Suffrage.** The 1987 Constitution describes voter '
                'eligibility for Filipino citizens, including the minimum voting age and residency '
                f'requirements, subject to legal disqualifications. [Constitution]({CONSTITUTION}).'), active_candidate_key
    if re.search(r'\b(?:article|art\.?)\s*(?:vii|7)\s*(?:section|sec\.?)\s*2\b', normalized, re.I):
        return ('**Article VII, Section 2 — Qualifications for President.** A candidate must be '
                'a natural-born Filipino citizen, a registered voter, able to read and write, at least '
                '40 years old on election day, and resident in the Philippines for at least ten '
                f'years immediately before the election. [Constitution]({CONSTITUTION}).'), active_candidate_key
    if re.search(r'\b(?:section|sec\.?)\s*261\s*\(?a\)?\b', normalized, re.I):
        return ('**Section 261(a), BP 881** addresses vote-buying and vote-selling offenses. '
                'For legal definitions and applicable penalties, consult the statutory text and '
                '[COMELEC](https://www.comelec.gov.ph/).'), active_candidate_key
    if re.search(r'\b(?:national|philsys)\s*(?:id|identification)\b', normalized, re.I) and re.search(r'\b(vote|voting|ballot|poll)\b', normalized, re.I):
        return ('**A National ID is not a general requirement to cast a vote.** '
                'Voters must satisfy registration and identification procedures set by COMELEC; '
                'check current guidance for exceptional identity checks. '
                f'[COMELEC voter-ID guidance]({COMELEC_VOTER_ID}).'), active_candidate_key
    if re.search(r'\b(how many|number of|count)\b', normalized, re.I) and re.search(r'\b(candidate|kandidato)\w*', normalized, re.I):
        return f'The fixed 2022 research database contains **{len(candidates)} presidential candidates**. This is not a current candidate list.', active_candidate_key
    if re.search(r'\b(?:section|sec\.?)\s*\d+\b', normalized, re.I) and not re.search(r'\b(?:bp\s*881|omnibus election code)\b', normalized, re.I):
        return ('Which Philippine statute or constitutional article do you mean? '
                'A section number alone does not identify the law.'), active_candidate_key
    if re.search(r"\bvoter[’']?s?\s*(?:id|identification card)\b|\bvoters?[- ]?id\b", normalized, re.I):
        return _voter_id_response(), active_candidate_key
    if re.search(r'\b(register|registration|how to register|rehistro)\b', normalized, re.I) and re.search(r'\b(vot|elec|bumoto)\w*', normalized, re.I):
        return _registration_response(), active_candidate_key
    ra = re.search(r'\b(?:r\.?a\.?|republic act)\s*[-:# ]*\s*(\d{4})\b', normalized, re.I)
    if ra and ra.group(1) in LEGAL:
        title, url = LEGAL[ra.group(1)]
        return f'**Republic Act No. {ra.group(1)} — {title}.**\n\nRead the [full official/legal text]({url}) for specific provisions.', active_candidate_key

    key, project, classification_text = extract_and_normalize_slots(normalized, active_candidate_key, candidates)
    if key and not _strong_candidate_reference(resolved, key, candidates):
        # The fuzzy engine sometimes matches colloquial words such as "paano"
        # to candidate aliases. Reject the match and restore original text.
        key = None
        classification_text = normalized
    if project and not _explicit_project_reference(resolved, project):
        project = None
        classification_text = normalized
    effective_key = key or active_candidate_key
    # Do not silently downgrade an unverified creation claim into a profile.
    if re.search(r'\b(did|created?|founded?|owns?|built|responsible for)\b', normalized, re.I) and key and not project:
        if key == 'bongbong marcos' and re.search(r'\b(bangui|windmill)\w*', normalized, re.I):
            factcheck = chatbot.respond(normalized)
            if factcheck:
                return factcheck, effective_key
        return ('I cannot verify that claimed project association in the curated 2022 database. '
                'Please provide an exact project name or consult a reliable primary source.'), effective_key
    tags_answer = _multi_topic(normalized, candidates, key)
    if tags_answer:
        return tags_answer, effective_key

    # Keep regex tier before Naive Bayes tier, per published methodology.
    regex_answer = chatbot.respond(normalized)
    if regex_answer:
        return regex_answer, effective_key

    intent = get_intent(classification_text, classifier, threshold=0.40)
    # Avoid inventing facts on off-topic questions because of overconfident classification.
    if not key and not project and not _requested_tags(normalized, candidates):
        if intent not in ('__SHOW_LIST__',):
            return ('I could not confidently match that question to the 2022 research database. '
                    'Try “Who is Leni Robredo?”, “What is RA 9006?”, or “How do I vote?”'), active_candidate_key

    if intent == '__SHOW_LIST__':
        if re.search(r'\b(list|candidates|kandidato|who (can|could|should) i vote for)\b', normalized, re.I):
            return _candidate_list(candidates), effective_key
        return ('I cannot identify that person in the 2022 candidate database. '
                'Try asking for the 2022 presidential candidate list.'), effective_key
    if intent == '__MATCH_TAG__':
        return (match_candidates_by_tag(normalized, candidates, key), effective_key) if _requested_tags(normalized, candidates) else ('Which topic are you asking about?', effective_key)
    if intent == '__SHOW_PROJECTS__':
        return get_candidate_projects(effective_key, candidates), effective_key
    if intent == '__VERIFY_PROJECT__':
        if not project:
            return (_profile(effective_key, candidates) if key else 'Which project in the 2022 database do you mean?', effective_key)
        return verify_project_association(normalized, project, effective_key, candidates), effective_key
    if intent == '__SHOW_AGE__':
        if effective_key in candidates:
            c = candidates[effective_key]
            return f"**Age recorded in the 2022 dataset for {c['full_name']}:** {c.get('age', 'Not listed')}. This is not their age today.", effective_key
        return 'Which 2022 candidate do you mean?', active_candidate_key
    if intent == '__SHOW_PROFILE__':
        if not key and not re.search(r'\b(?:he|she|her|his|him|niya|kanya|this candidate)\b', text, re.I):
            return ('Which 2022 presidential candidate do you mean? '
                    'Please provide a candidate name.'), active_candidate_key
        return _profile(effective_key, candidates), effective_key
    if project:
        return verify_project_association(normalized, project, effective_key, candidates), effective_key
    return ('I could not find a verified answer within the 2022 dataset. Please rephrase with '
            'a candidate name, electoral topic, or cited law.'), effective_key
