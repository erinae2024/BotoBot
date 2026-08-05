# nlp/query_engine.py

import re
from rapidfuzz import fuzz, process

VALID_TAGS = ["education", "health", "women", "poverty", "labor", "workers", "economy", "housing", "infrastructure", "government experience"]

def resolve_pronouns(text, active_candidate_key, candidates_data):
    if not active_candidate_key:
        return text
    
    pronouns = candidates_data[active_candidate_key].get('pronouns', ['he', 'she', 'they', 'her', 'his', 'him', 'niya'])
    pattern = r'\b(' + '|'.join(pronouns) + r'|this candidate)\b'
    
    name = candidates_data[active_candidate_key]['full_name']
    return re.sub(pattern, name, text, flags=re.IGNORECASE)

def extract_and_normalize_slots(text, active_candidate_key, candidates_data):
    detected_candidate_key = None
    project_found = None
    normalized_text = text

    alias_map = {}
    for key, data in candidates_data.items():
        alias_map[data['full_name'].lower()] = (key, data['full_name'])
        for alias in data.get('aliases', []):
            alias_map[alias.lower()] = (key, alias)
            
    best_candidate_match = process.extractOne(text.lower(), list(alias_map.keys()), scorer=fuzz.partial_ratio)
    
    if best_candidate_match and best_candidate_match[1] > 80:
        matched_alias = best_candidate_match[0]
        detected_candidate_key, matched_str = alias_map[matched_alias]
        pattern = re.compile(re.escape(matched_str), re.IGNORECASE)
        normalized_text = pattern.sub('_CANDIDATE_', normalized_text)

    all_projects = []
    for data in candidates_data.values():
        for proj in data.get('projects', []):
            all_projects.append(proj['name'])

    best_proj_match = process.extractOne(text.lower(), all_projects, scorer=fuzz.token_set_ratio)
    if best_proj_match and best_proj_match[1] > 75:
        project_found = best_proj_match[0]
        pattern = re.compile(re.escape(project_found), re.IGNORECASE)
        normalized_text = pattern.sub('_PROJECT_', normalized_text)

    return detected_candidate_key, project_found, normalized_text

def match_candidates_by_tag(query_text, candidates_data):
    tag_regex = r'(?i)\b(' + '|'.join(VALID_TAGS) + r')\b'
    match = re.search(tag_regex, query_text)
    
    if not match:
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
            
    if not matches:
        return f"I couldn't find any candidates directly associated with '{query_tag}'."
    return f"Candidates associated with **{query_tag}** include: " + ", ".join(set(matches))

def get_candidate_projects(active_candidate_key, candidates_data):
    if not active_candidate_key:
        return "Which candidate's projects would you like to see?"
        
    c_data = candidates_data[active_candidate_key]
    projects = c_data.get('projects', [])
    
    if not projects:
        return f"No specific projects are currently listed for {c_data['full_name']}."
        
    response = f"Here are the major projects/programs of **{c_data['full_name']}**:\n"
    for p in projects:
        response += f"\n* **{p['name']}**\n  More details: {p['link']}"
    return response

def verify_project_association(query_text, project_found, active_candidate_key, candidates_data):
    if not active_candidate_key:
        return "Please specify which candidate you are asking about."
        
    c_data = candidates_data[active_candidate_key]
    candidate_projects = [p['name'].lower() for p in c_data.get('projects', [])]
    
    search_target = project_found.lower() if project_found else query_text.lower()
    best_match = process.extractOne(search_target, candidate_projects, scorer=fuzz.token_set_ratio)
    
    if best_match and best_match[1] > 70:
        matched_proj_name = best_match[0]
        proj_data = next(p for p in c_data['projects'] if p['name'].lower() == matched_proj_name)
        return f"Yes, '{proj_data['name']}' is a project by {c_data['full_name']}.\nDetails: {proj_data['link']}"
    else:
        return f"There is no information associating {c_data['full_name']} with that project in my database."