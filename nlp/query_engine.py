# nlp/query_engine.py

import re
from nltk.tokenize import word_tokenize
from rapidfuzz import fuzz, process

def get_dynamic_tags(candidates_data):
    """Dynamically extracts all valid tags from the candidate database."""
    tags = set(["government experience"])
    for data in candidates_data.values():
        tags.update(data.get('tags', []))
        for proj in data.get('projects', []):
            tags.update(proj.get('tags', []))
    return list(tags)

def normalize_contractions(text):
    """Normalizes common user contractions for clean tokenization."""
    text = re.sub(r"\b(who's|whos)\b", "who is", text, flags=re.IGNORECASE)
    text = re.sub(r"\b(what's|whats)\b", "what is", text, flags=re.IGNORECASE)
    text = re.sub(r"\b(how's|hows)\b", "how is", text, flags=re.IGNORECASE)
    text = re.sub(r"(?<=\w)('s|')(?:(?=\s)|$)", "", text)
    return text

def resolve_pronouns(text, active_candidate_key, candidates_data):
    if not active_candidate_key:
        return text
    
    specific_pronouns = candidates_data[active_candidate_key].get('pronouns', [])
    generic_pronouns = ['he', 'she', 'they', 'her', 'his', 'him', 'niya', 'kanya']
    all_pronouns = list(set(specific_pronouns + generic_pronouns))
    
    pattern = r'\b(' + '|'.join(all_pronouns) + r'|this candidate)\b'
    name = candidates_data[active_candidate_key]['full_name']
    return re.sub(pattern, name, text, flags=re.IGNORECASE)

def extract_and_normalize_slots(text, active_candidate_key, candidates_data):
    normalized_text = normalize_contractions(text)
    words = word_tokenize(normalized_text)
    
    alias_map = {}
    for key, data in candidates_data.items():
        alias_map[data['full_name'].lower()] = (key, data['full_name'])
        for alias in data.get('aliases', []):
            alias_map[alias.lower()] = (key, alias)

    all_projects = {}
    stop_words = {"public", "housing", "field", "hospital", "program", "e-konsulta", "covid-19", "covid", "project"}
    for key, data in candidates_data.items():
        for proj in data.get('projects', []):
            proj_name = proj['name']
            all_projects[proj_name.lower()] = proj_name
            
            proj_tokens = re.findall(r'\b[a-zA-Z0-9\-]{4,}\b', proj_name.lower())
            for token in proj_tokens:
                if token not in stop_words and token not in all_projects:
                    all_projects[token] = proj_name

    detected_candidate_key = None
    matched_candidate_str = None
    project_found = None
    raw_cand_ngram = ""
    raw_proj_ngram = ""

    ngrams = []
    n_words = len(words)
    for size in range(1, min(6, n_words + 1)):
        for i in range(n_words - size + 1):
            ngram_str = " ".join(words[i:i+size])
            ngrams.append(ngram_str)

    best_cand_score = 0
    for ngram in ngrams:
        if len(ngram) < 3:
            continue
        match = process.extractOne(ngram.lower(), list(alias_map.keys()), scorer=fuzz.ratio)
        if match and match[1] >= 68:
            if match[1] > best_cand_score or (match[1] == best_cand_score and len(ngram) > len(raw_cand_ngram)):
                best_cand_score = match[1]
                matched_alias = match[0]
                detected_candidate_key, matched_candidate_str = alias_map[matched_alias]
                raw_cand_ngram = ngram

    best_proj_score = 0
    for ngram in ngrams:
        if len(ngram.strip()) < 3:
            continue
        match = process.extractOne(ngram.lower(), list(all_projects.keys()), scorer=fuzz.ratio)
        if match and match[1] >= 75:
            if match[1] > best_proj_score or (match[1] == best_proj_score and len(ngram) > len(raw_proj_ngram)):
                best_proj_score = match[1]
                project_found = all_projects[match[0]]
                raw_proj_ngram = ngram

    if detected_candidate_key and raw_cand_ngram:
        pattern = re.compile(re.escape(raw_cand_ngram), re.IGNORECASE)
        normalized_text = pattern.sub('_CANDIDATE_', normalized_text)

    if project_found and raw_proj_ngram:
        pattern = re.compile(re.escape(raw_proj_ngram), re.IGNORECASE)
        normalized_text = pattern.sub('_PROJECT_', normalized_text)

    return detected_candidate_key, project_found, normalized_text

def match_candidates_by_tag(query_text, candidates_data, detected_candidate_key=None):
    dynamic_tags = get_dynamic_tags(candidates_data)
    tag_regex = r'(?i)\b(' + '|'.join(dynamic_tags) + r')\b'
    match = re.search(tag_regex, query_text)
    
    if not match:
        extracted = re.sub(r'(?i)\b(which|who|what|candidates|candidate|prioritize|focus|focuses|on|supports|support|advocates|for|care|cares|about|associated|with|in|are|is|the|any|does|anyone)\b', '', query_text)
        extracted = re.sub(r'[^\w\s]', '', extracted).strip()
        if extracted and len(extracted) > 2:
            return f"I couldn't find any candidates directly associated with '{extracted}'."
        return "I'm not sure which specific advocacy or field you are asking about."
    
    query_tag = match.group(1).lower()
    matches = []
    
    for key, data in candidates_data.items():
        if query_tag == "government experience" and data.get("has_gov_experience"):
            matches.append(data['full_name'])
            continue
            
        all_tags = set(data.get('tags', []))
        for proj in data.get('projects', []):
            all_tags.update(proj.get('tags', []))
            
        if query_tag in all_tags:
            matches.append(data['full_name'])
            
    unique_matches = sorted(list(set(matches)))

    if detected_candidate_key and detected_candidate_key in candidates_data:
        cand_name = candidates_data[detected_candidate_key]['full_name']
        if cand_name in unique_matches:
            prefix = f"Yes, **{cand_name}** is associated with **{query_tag}**.\n\n"
        else:
            prefix = f"No, **{cand_name}** is not directly listed for **{query_tag}** in my database.\n\n"
        
        if not unique_matches:
            return prefix + f"I couldn't find any candidates directly associated with '{query_tag}'."
        return prefix + f"All candidates associated with **{query_tag}** include: " + ", ".join(unique_matches)

    if not unique_matches:
        return f"I couldn't find any candidates directly associated with '{query_tag}'."
    return f"Candidates associated with **{query_tag}** include: " + ", ".join(unique_matches)

def get_candidate_projects(active_candidate_key, candidates_data):
    if not active_candidate_key:
        return "Which candidate's projects would you like to see?"
        
    c_data = candidates_data[active_candidate_key]
    projects = c_data.get('projects', [])
    
    if not projects:
        return f"No specific projects are currently listed for {c_data['full_name']}."
        
    response = f"Here are the major projects/programs of **{c_data['full_name']}**:\n"
    for p in projects:
        link_data = p.get('link', '')
        link_str = " and ".join(link_data) if isinstance(link_data, list) else link_data
        response += f"\n* **{p['name']}**\n  More details: {link_str}"
    return response

def verify_project_association(query_text, project_found, active_candidate_key, candidates_data):
    search_target = project_found.lower() if project_found else query_text.lower()
    if not project_found:
        search_target = re.sub(r'(?i)\b(tell me about|what is|did|create|is|by|about|the|a|an|details|info)\b', '', search_target).strip()

    if active_candidate_key:
        c_data = candidates_data[active_candidate_key]
        candidate_projects = [p['name'].lower() for p in c_data.get('projects', [])]
        best_match = process.extractOne(search_target, candidate_projects, scorer=fuzz.token_set_ratio)
        if best_match and best_match[1] > 60:
            matched_proj_name = best_match[0]
            proj_data = next(p for p in c_data['projects'] if p['name'].lower() == matched_proj_name)
            
            link_data = proj_data.get('link', '')
            link_str = " and ".join(link_data) if isinstance(link_data, list) else link_data
            
            return f"Yes, '{proj_data['name']}' is a project by **{c_data['full_name']}**.\nDetails: {link_str}"

    all_projects = []
    for key, data in candidates_data.items():
        for proj in data.get('projects', []):
            all_projects.append((proj['name'].lower(), key, proj))

    best_global_match = process.extractOne(search_target, [p[0] for p in all_projects], scorer=fuzz.token_set_ratio)
    
    if best_global_match and best_global_match[1] > 60:
        matched_proj_name = best_global_match[0]
        _, owning_candidate_key, proj_data = next(p for p in all_projects if p[0] == matched_proj_name)
        owner_name = candidates_data[owning_candidate_key]['full_name']
        
        link_data = proj_data.get('link', '')
        link_str = " and ".join(link_data) if isinstance(link_data, list) else link_data
        
        if active_candidate_key and active_candidate_key != owning_candidate_key:
            active_name = candidates_data[active_candidate_key]['full_name']
            return f"There is no information associating {active_name} with that project. However, '{proj_data['name']}' is actually a project by **{owner_name}**.\nDetails: {link_str}"
        else:
            return f"'{proj_data['name']}' is a project by **{owner_name}**.\nDetails: {link_str}"

    if active_candidate_key:
        return f"There is no information associating {candidates_data[active_candidate_key]['full_name']} with that project in my database."
    return "I couldn't find any information about that specific project in my database."