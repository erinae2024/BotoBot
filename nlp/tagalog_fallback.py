"""Cited, offline Tagalog backup for four demonstration prompts only.

The main method remains entity-preserving translation. These fixed templates avoid
leaving the most common Cebu booth/demo prompts untranslated when Google fails.
"""
import re


def offline_tagalog_reply(question, english_answer, candidates):
    q = question.lower()
    if re.search(r'\b(paano bumoto|how to vote)\b', q):
        return ('**Paano bumoto (pangkalahatang proseso ng halalan):**\n\n'
                '1. Pumunta sa itinakdang presinto sa araw ng halalan.\n'
                '2. Kunin ang opisyal na balota mula sa Electoral Board.\n'
                '3. Bilugan o punan nang maayos ang angkop na oval ayon sa tagubilin sa balota.\n'
                '4. Sundin ang mga tagubilin ng COMELEC sa pagpapasok ng balota at beripikasyon.\n\n'
                'Para sa kasalukuyang impormasyon: [COMELEC](https://www.comelec.gov.ph/).')
    if re.search(r"\bvoter[’']?s?\s*id\b|\bvoter[- ]?id\b", q):
        return ('**Magkaiba ang voter-ID card at pagpaparehistro bilang botante.** '
                'Ayon sa COMELEC, pansamantalang nakahinto ang paggawa at pamamahagi ng voter-ID card. '
                '**Hindi kailangan ang voter-ID card para bumoto.** '\
                '\n\n[Sanggunian: COMELEC](https://www.comelec.gov.ph/index.html?r=VoterRegistration%2FWhatisVoterRegistration%2FVoterIDIssuance).')
    if re.search(r'\b(?:ra|r\.a\.|republic act)\s*9006\b', q):
        return ('**Republic Act 9006 — Fair Election Act.** Tumutukoy ito sa makatarungang '
                'pagpapatakbo ng kampanya at mga panuntunan kaugnay ng eleksiyon. '
                '[Basahin ang batas](https://lawphil.net/statutes/repacts/ra2001/ra_9006_2001.html).')
    if re.search(r'\b(mga kandidato|list.*candidates|presidential candidates)\b', q) and 'candidates in the research database' in english_answer:
        return ('**Sampung kandidato sa pagkapangulo noong 2022 na nasa pananaliksik:**\n\n'
                + '\n'.join('- ' + c['full_name'] for c in candidates.values())
                + '\n\n*Pangkasaysayang listahan noong 2022; hindi ito listahan ng mga kandidato sa kasalukuyan.*')
    return None
