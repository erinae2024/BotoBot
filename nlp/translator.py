# nlp/translator.py

import re
from flashtext import KeywordProcessor
from deep_translator import GoogleTranslator

TAGALOG_TRIGGERS = r'(?i)\b(boto|bumoto|halalan|eleksyon|botohan|sino|ano|paano|saan|bakit|kailan|mga|niya|tungkol|ba|proyekto)\b'

def build_entity_masker(candidates_data):
    kp = KeywordProcessor(case_sensitive=False)
    mask_map = {}
    counter = 0
    
    for key, data in candidates_data.items():
        words_to_protect = [data['full_name']] + data.get('aliases', [])
        for proj in data.get('projects', []):
            words_to_protect.append(proj['name'])
            
        for word in words_to_protect:
            placeholder = f"ENT{counter:04d}X" 
            kp.add_keyword(word, placeholder)
            mask_map[placeholder] = word
            counter += 1
            
    return kp, mask_map

def process_language(text, masker, mask_map, target_lang='en'):
    is_tagalog = bool(re.search(TAGALOG_TRIGGERS, text))
    
    masked_text = masker.replace_keywords(text)
        
    if is_tagalog or target_lang == 'tl':
        try:
            translated = GoogleTranslator(source='auto', target=target_lang).translate(masked_text)
        except Exception:
            translated = masked_text
    else:
        translated = masked_text

    for placeholder, original_kw in mask_map.items():
        translated = translated.replace(placeholder, original_kw)
        
    return translated, is_tagalog