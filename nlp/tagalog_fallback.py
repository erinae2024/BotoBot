"""Offline Tagalog wording for verifiable, bounded BotoBot responses.

Prioritize reviewed templates for common demo topics over network translation.
Names, projects, and citations are copied from the fixed 2022 dataset.
"""
import re
from urllib.parse import urlparse

from nlp.translator import process_language


def _profile_in_tagalog(english_answer, candidates):
    if not english_answer.startswith('### '):
        return None
    for candidate in candidates.values():
        if english_answer.startswith('### ' + candidate['full_name'] + '\n'):
            parts = [f"### {candidate['full_name']}",
                     f"**Edad sa datos noong 2022:** {str(candidate.get('age', 'Hindi nakatala')).replace('Born ', 'ipinanganak noong ')}",
                     '**Mga posisyon sa dataset:** ' + '; '.join(candidate.get('positions', []) or ['Hindi nakatala']),
                     '**Edukasyon sa dataset:** ' + '; '.join(candidate.get('education', []) or ['Hindi nakatala']),
                     '**Mga nakatalang proyekto, programa, at gawaing lehislatibo:** '
                     + '; '.join(p.get('name', 'Hindi tinukoy') for p in candidate.get('projects', []))]
            links = [link for link in candidate.get('links', [])
                     if isinstance(link, str) and urlparse(link).scheme == 'https'
                     and urlparse(link).netloc]
            if links:
                parts.append('**Mga sanggunian:** ' + ' · '.join(
                    f'[Sanggunian {i}]({link})' for i, link in enumerate(links, 1)))
            parts.append('*Makasaysayang tala noong 2022. Hindi ito pag-endorso o awtomatikong pagpatunay ng lahat ng pahayag.*')
            return '\n\n'.join(parts)
    return None


def offline_tagalog_reply(question, english_answer, candidates):
    """Return a source-bounded Tagalog answer, or None for other topics."""

    # Check the ACTUAL answer before matching keywords in the question, to keep
    # out-of-scope and neutrality safeguards intact even with Tagalog selected.
    if english_answer.startswith('BotoBot is a research demonstration focused'):
        return ('Ang BotoBot ay pananaliksik tungkol sa **mga kandidato sa pagkapangulo noong 2022** '
                'at piling batas sa halalan. Wala itong live na datos tungkol sa kasalukuyan o '
                'susunod na eleksyon, hula, o rekomendasyon ng kandidato. '
                'Para sa pinakabagong impormasyon, pumunta sa [COMELEC](https://www.comelec.gov.ph/).')
    if english_answer.startswith('I do not recommend or endorse'):
        return ('**Hindi nagrerekomenda o nag-eendorso ng kandidato ang BotoBot.** '
                'Maaari nitong ipakita ang makasaysayang profile at mga sanggunian mula sa 2022 research dataset.')
    if english_answer.startswith('You’re welcome!'):
        return ('Walang anuman! Maaari kang magtanong tungkol sa mga kandidato noong 2022, '
                'batas sa halalan, o proseso ng pagboto.')
    if english_answer.startswith('Okay. Feel free'):
        return 'Sige! Balik ka lang kung may nais kang itanong tungkol sa 2022 research dataset.'
    if english_answer.startswith('Do you mean **how to cast a ballot**?'):
        return ('Ang tinutukoy mo ba ay **proseso ng pagboto**? '
                'Maaari kong ipaliwanag ang pangkalahatang mga hakbang. '
                'Wala akong access sa personal na talaan ng mga botante.')
    if english_answer.startswith('**Vote-buying and vote-selling:**'):
        return ('**Parusa sa pagbili o pagbebenta ng boto:** Ayon sa Section 261(a) at '
                'Section 264 ng BP 881, ang karaniwang parusang nakasaad para sa saklaw na '
                'mga paglabag sa eleksyon ay **isa hanggang anim na taong pagkakakulong**, '
                'depende sa naaangkop na batas at detalye ng kaso. '
                '[COMELEC — Omnibus Election Code]('
                'https://www.comelec.gov.ph/?r=References/RelatedLaws/OmnibusElectionCode/OECArt22). '
                '*Pangkalahatang impormasyon lamang, hindi payong legal sa isang partikular na kaso.*')
    if english_answer.startswith('**Vote-buying and vote-selling**'):
        return ('**Pagbili at pagbebenta ng boto** ay mga paglabag sa batas ayon sa '
                'Section 261(a) ng BP 881 (Omnibus Election Code). Ang pagbibigay o pagtanggap '
                'ng pera o bagay na may halaga upang impluwensiyahan ang boto ay maaaring '
                'maging paglabag. Basahin ang batas at alamin ang kasalukuyang proseso ng '
                'pagrereklamo sa [COMELEC](https://www.comelec.gov.ph/). '
                '*Pangkalahatang impormasyon lamang; hindi ito payong legal para sa isang kaso.*')
    if english_answer.startswith('**Where do I vote?'):
        return ('**Saan boboto?** Hindi matutukoy ng BotoBot ang iyong presinto dahil '
                'wala itong access sa talaan ng mga botante. Gamitin ang '
                '[COMELEC Precinct Finder](https://precinctfinder.comelec.gov.ph/) '
                'kapag available, o magtanong sa lokal na tanggapan ng COMELEC. '
                'Maaaring hindi bukas ang online service sa labas ng panahon ng halalan. '
                '**Huwag magbahagi ng personal na impormasyon rito.**')
    if english_answer.startswith('To vote in Philippine elections:'):
        return ('**Paano bumoto (pangkalahatang proseso ng halalan):**\n\n'
                '1. Pumunta sa itinakdang presinto sa araw ng halalan.\n'
                '2. Kunin ang opisyal na balota mula sa Electoral Board.\n'
                '3. Punan nang maayos ang angkop na oval ayon sa tagubilin sa balota.\n'
                '4. Sundin ang mga tagubilin sa pagproseso ng balota at voter receipt.\n\n'
                'Para sa kasalukuyang impormasyon: [COMELEC](https://www.comelec.gov.ph/).')
    if english_answer.startswith('**To register as a voter:**'):
        return ('**Pagpaparehistro bilang botante:** Tiyaking kwalipikado ka, alamin ang '
                'kasalukuyang iskedyul at mga kinakailangang dokumento sa COMELEC, at sundin '
                'ang opisyal na proseso ng pagpaparehistro. Magkaiba ang voter registration '
                'at voter-ID card. Maaaring magbago ang mga iskedyul at requirement. '
                '[COMELEC registration requirements]('
                'https://www.comelec.gov.ph/index.html?r=VoterRegistration%2FWhatisVoterRegistration%2FRegistrationRequirements).')
    if english_answer.startswith("**Voter's ID card is different"):
        return ('**Magkaiba ang voter-ID card at pagpaparehistro bilang botante.** '
                'Ayon sa COMELEC, pansamantalang nakahinto ang paggawa at pamamahagi ng '
                'voter-ID card. **Hindi kailangan ang voter-ID card para bumoto.** '
                '[Sanggunian: COMELEC]('
                'https://www.comelec.gov.ph/index.html?r=VoterRegistration%2FWhatisVoterRegistration%2FVoterIDIssuance).')
    if english_answer.startswith(('**RA 9006 —', '**Republic Act No. 9006 —')) and 'requested section' not in english_answer:
        return ('**Republic Act 9006 — Fair Election Act.** Tumutukoy ito sa mga patakaran '
                'sa kampanya, propaganda, at paggamit ng media sa halalan. '
                '[Basahin ang batas](https://lawphil.net/statutes/repacts/ra2001/ra_9006_2001.html).')
    if english_answer.startswith('**2022 Philippine presidential candidates in the research database:**'):
        return ('**Sampung kandidato sa pagkapangulo noong 2022 na nasa pananaliksik:**\n\n'
                + '\n'.join('- ' + c['full_name'] for c in candidates.values())
                + '\n\n*Hindi ito listahan ng mga kasalukuyang kandidato.*')
    if english_answer.startswith('**Voter eligibility'):
        return ('**Kwalipikasyon ng botante — Article V, Section 1:** Sa pambansang halalan, '
                'karaniwang kailangan ang pagkamamamayang Pilipino, edad na 18 pataas sa araw ng halalan, '
                'paninirahan sa Pilipinas nang hindi bababa sa isang taon at sa lugar ng pagboto nang anim na buwan '
                'bago ang halalan, at walang legal na diskwalipikasyon. Kailangan ding sumunod sa mga tuntunin ng pagpaparehistro. '
                'Hindi ko matitiyak ang iyong personal na kwalipikasyon. '
                '[Saligang Batas](https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/3/353) · [COMELEC](https://www.comelec.gov.ph/).')
    if english_answer.startswith('I do not have verified information about that Republic Act'):
        return 'Wala akong beripikadong impormasyon tungkol sa batas na iyon sa 2022 election database. Tingnan ang [Lawphil](https://lawphil.net/).'
    if english_answer.startswith('Which candidate would you like to discuss first?'):
        return 'Sino sa mga kandidatong iyon ang gusto mong talakayin muna? Magtanong tungkol sa isang kandidato sa bawat tanong.'
    if english_answer.startswith('Hello! Welcome to BotoBot!'):
        return 'Kumusta! Magtanong tungkol sa mga kandidato noong 2022, batas sa halalan, o proseso ng pagboto.'
    if english_answer.startswith('I could not confidently match') or english_answer.startswith('I could not find a verified answer'):
        return ('Hindi ko matukoy nang may sapat na katiyakan ang tanong sa 2022 research database. '
                'Subukan ang “Sino si Leni Robredo?”, “Ano ang RA 9006?”, o “Paano bumoto?”.')
    if english_answer.startswith('I cannot identify that person'):
        return ('Hindi ko matukoy ang taong iyon sa database ng mga kandidato noong 2022. '
                'Maaari mong itanong ang listahan ng mga kandidato.')
    if english_answer.startswith(('Which **2022 presidential candidate**', 'Which 2022 presidential candidate')):
        return 'Aling **kandidato sa pagkapangulo noong 2022** ang tinutukoy mo?'
    if english_answer.startswith('**Age recorded in the 2022 dataset for '):
        for candidate in candidates.values():
            if candidate['full_name'] in english_answer:
                return (f"**Edad ni {candidate['full_name']} sa dataset noong 2022:** "
                        f"{str(candidate.get('age', 'Hindi nakatala')).replace('Born ', 'ipinanganak noong ')}. "
                        "*Hindi ito ang kanyang edad sa kasalukuyan.*")
    if english_answer.startswith('Selected projects, programs, and legislative activities listed for **'):
        for candidate in candidates.values():
            if f"for **{candidate['full_name']}**" in english_answer:
                lines = [f"**Mga proyekto, programa at gawaing lehislatibo ni {candidate['full_name']} "
                         "sa datos noong 2022:**"]
                for project in candidate.get('projects', []):
                    links = project.get('link', [])
                    if isinstance(links, str):
                        links = [links]
                    safe = [link for link in links if isinstance(link, str)
                            and urlparse(link).scheme == 'https' and urlparse(link).netloc]
                    suffix = (' — ' + ' · '.join(f'[Sanggunian]({link})' for link in safe)) if safe else ''
                    lines.append('- ' + project.get('name', 'Hindi nakatala') + suffix)
                lines.append('*Mula lamang sa 2022 research dataset; hindi ito pag-endorso o '
                             'pagpapatunay ng lahat ng pahayag.*')
                return '\n\n'.join([lines[0], '\n'.join(lines[1:])])
    profile = _profile_in_tagalog(english_answer, candidates)
    if profile is not None:
        return profile
    return None


def localize_answer(question, english_answer, response_lang, candidates, masker, mask_map):
    """Core offline answers first; translation service only for remaining topics."""
    if response_lang != 'tl':
        return english_answer
    reviewed = offline_tagalog_reply(question, english_answer, candidates)
    if reviewed is not None:
        return reviewed
    try:
        translated, _ = process_language(english_answer, masker, mask_map, target_lang='tl')
    except Exception:
        translated = english_answer
    if translated != english_answer and translated.strip():
        return translated
    return ('*Hindi available ang awtomatikong pagsasalin sa ngayon; '
            'ipinapakita ang orihinal na sagot sa Ingles.*\n\n' + english_answer)
