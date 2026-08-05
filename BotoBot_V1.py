# BotoBot Chatbot V1
# Uses NLTK and Regular Expressions for pattern matching

import streamlit as st
import nltk
from nltk.chat.util import Chat, reflections

# ==========================================
# CANDIDATE PROFILES
# Profiles updated with 2022 election info
# ==========================================

candidates = {
    "ernesto abella": {
        "full_name": "Ernesto \"Ernie\" Corpus Abella",
        "age": "72 (Born March 22, 1950)",
        "positions": [
            "Presidential Spokesperson (2016-2017)",
            "Undersecretary, DFA (2017-2021)",
        ],
        "education": [
            "Asian Institute of Management (Master in Entrepreneurship)",
            "Silliman University (Master in Divinity)"
        ],
        "projects": [
            "Founder of Hope of Asia",
            "Founder of The Jesus Fellowship",
            "Founder of Southpoint School in Davao City",
            "Founding member of One Accord Credit Cooperative"
        ],
        "links":[
            "(https://www.gmanetwork.com/news/eleksyon2022/candidates/ernestoabella/)",
            "(https://www.abs-cbn.com/halalan2022/candidates/ernesto-abella)",
            "(https://www.inquirer.net/duterte/cabinet/)"
        ]
    },
    "leody de guzman": {
        "full_name": "Leodegario \"Ka Leody\" Quitain de Guzman",
        "age": "62 (Born July 25, 1959)",
        "positions": [
            "Chairperson, Bukluran ng Manggagawang Pilipino",
            "Chairman, Partido Lakas ng Masa (PLM)"
        ],
        "education": [
            "PMI Colleges (BS Customs Administration)"
        ],
        "projects": [
            "Manggagawa Naman Electoral Platform",
            "Labor Rights Advocacies"
        ],
        "links":[
            "(https://www.gmanetwork.com/news/eleksyon2022/candidates/leodegariodeguzman)",
            "(https://www.abs-cbn.com/halalan2022/candidates/leody-de-guzman)",
            "(https://newsinfo.inquirer.net/1589683/de-guzmanlabors-turnto-be-frontand-center)"
        ]
    },
    "isko moreno": {
        "full_name": "Francisco \"Isko\" Moreno Domagoso",
        "age": "47 (Born October 24, 1974)",
        "positions": [
            "Mayor of Manila (2019-2022)",
            "Vice Mayor of Manila (2007-2016)",
            "Undersecretary, DSWD (2018)"
        ],
        "education": [
            "Pamantasan ng Lungsod ng Maynila (Public Administration)",
            "International Academy of Management and Economics (Bachelor of Science in Business Administration)"
        ],
        "projects": [
            "Manila COVID-19 Field Hospital",
            "Tondominium & Binondominium Public Housing"
        ],
        "links":[
            "(https://www.gmanetwork.com/news/eleksyon2022/candidates/franciscodomagoso/)",
            "(https://www.abs-cbn.com/halalan2022/candidates/isko-moreno)",
            "(https://newsinfo.inquirer.net/1534385/manila-covid-19-field-hospital-ready-for-returning-overseas-filipinos)"
        ]
    },
    "norberto gonzales": {
        "full_name": "Norberto B. Gonzales",
        "age": "75 (Born April 17, 1947)",
        "positions": [
            "Secretary of National Defense (2009-2010)",
            "National Security Adviser (2005-2010)"
        ],
        "education": [
            "Ateneo de Davao University (BS Pre-Med)",
            "National Defense College of the Philippines (Master in National Security Administration)"
        ],
        "projects": [
            "Founder, Partido Demokratiko Sosyalista ng Pilipinas",
            "Peace negotiations with insurgent groups"
        ],
        "links":[
            "(https://www.gmanetwork.com/news/eleksyon2022/candidates/norbertogonzales/)",
            "(https://www.abs-cbn.com/halalan2022/candidates/norberto-gonzales)",
            "(https://www.rappler.com/people/n50319899-norberto-gonzales/)"
        ]
    },
    "panfilo lacson": {
        "full_name": "Panfilo \"Ping\" Morena Lacson",
        "age": "73 (Born June 1, 1948)",
        "positions": [
            "Senator of the Philippines (2001-13, 2016-22)",
            "Presidential Assistant on Rehabilitation and Recovery (2013-2015)",
            "Chief, Philippine National Police (1999-2001)",
            "Chief, Presidential Anti-Organized Crime Task Force (1998-2001)",
            "Project Officer, Special Project Alpha (1996-1997)",
            "Chief, Presidential Anti-Crime Commission Task Force Habagat (1992-1995)",
            "Provincial Director, Laguna PC (1992)",
            "Commander, Ceby Metropolitan District Command (1989-1992)",
            "PC-INP Anti-Carnapping Task Force (1986-1988)",
            "Metrocom Intelligence and Security Group (1971-1986)"
        ],
        "education": [
            "Philippine Military Academy (Bachelor of Science)",
            "Lyceum of the Philippines (Masters in Government Management)"
        ],
        "projects": [
            "RA 11055: National ID Law (Principal Sponsor)",
            "RA 11479: Anti-Terrorism Act of 2020 (Sponsor and Co-author)",
            "RA 11053: Anti-Hazing Law of 2018 (Sponsor and Author)",
            "RA 10969: Free Irrigation Service Act",
            "RA 10351: Sin Tax Law",
        ],
        "links":[
            "(https://www.gmanetwork.com/news/eleksyon2022/candidates/panfilolacson/)",
            "(https://www.abs-cbn.com/halalan2022/candidates/ping-lacson)",
            "(https://ldr.senate.gov.ph/senator/panfilo-m-lacson)"

        ]
    },
    "faisal mangondato": {
        "full_name": "Faisal Mangondato",
        "age": "59 (Born December 30, 1962)",
        "positions": [
            "National President, Katipunan Party",
            "President, Kalaw Printext Marketing in Marantao, Lanao del Sur",
            "Managing Director, Kalaw Travel and Tour"
        ],
        "education": [
            "Philippine Women's University (BS Medical Technology)"
        ],
        "projects": [
            "Advocacy for Philippine Federalism"        
        ],
        "links":[
            "(https://www.gmanetwork.com/news/eleksyon2022/candidates/faisalmangondato/)",
            "(https://www.abs-cbn.com/halalan2022/candidates/faisal-mangondato)",
            "(https://newsinfo.inquirer.net/1591346/faisal-mangondatos-voice-is-loudest-for-mindanao)"
        ]
    },
    "bongbong marcos": {
        "full_name": "Ferdinand Romualdez Marcos Jr.",
        "age": "64 (Born September 13, 1957)",
        "positions": [
            "Senator of the Philippines (2010-2016)",
            "Congressman, 2nd District, Ilocos Norte (1992-95, 2007-10)"
            "Governor of Ilocos Norte (1983-86, 1998-2007)",
            "Vice Governor, Ilocos Norte (1981-1983)"
        ],
        "education": [
            "University of Oxford (Special Diploma in Social Studies)"
        ],
        "projects": [
            "RA 10363: Creating Seven Additional Branches of the Regional Court (Co-Author)",
            "RA 10632: Postponing the Sangguniang Kabataan Election (Author)",
            "RA 10884: Balanced Housing Development Program Amendments (Author)",
        ],
        "links":[
            "(https://www.gmanetwork.com/news/eleksyon2022/candidates/ferdinandjrmarcos/)",
            "(https://www.abs-cbn.com/halalan2022/candidates/bongbong-marcos)",
            "(https://ldr.senate.gov.ph/bills/senate-bill-no-1186-16th-congress-republic)",
            "(https://issuances-library.senate.gov.ph/bills/senate-bill-no-2947-16th-congress-republic)",
            "(https://issuances-library.senate.gov.ph/bills/senate-bill-no-3034-15th-congress-republic)",
            "(https://verafiles.org/articles/vera-files-fact-check-posts-claiming-bongbong-marcos-authore)"
        ]
    },
    "jose montemayor jr": {
        "full_name": "Jose C. Montemayor Jr.",
        "age": "65 (Born approx. 1956)",
        "positions": [
            "Cardiologist",
            "Lawyer",
            "DPP Presidential Candidate (2022)"
        ],
        "education": [
            "University of the Philippines (Medicine)",
            "Far Eastern University",
            "Philippine Law School"
        ],
        "projects": [
            "Free Medical and Legal Missions",
            "COVID-19 Alternative Policy Advocacies"
        ],
        "links":[
            "(https://www.gmanetwork.com/news/eleksyon2022/candidates/josejrmontemayor/)",
            "(https://www.abs-cbn.com/halalan2022/candidates/jose-montemayor)"
        ]
    },
    "manny pacquiao": {
        "full_name": "Emmanuel Dapidran Pacquiao",
        "age": "43 (Born December 17, 1978)",
        "positions": [
            "Senator of the Philippines (2016-2022)",
            "Representative, Sarangani (2010-2016)",
            "8-Division World Boxing Champion"
        ],
        "education": [
            "University of Makati (BA Political Science)"
        ],
        "projects": [
            "Pacman Village (Free Housing Project)",
            "Pabahay Programs"
        ],
        "links":[
            "(https://www.gmanetwork.com/news/eleksyon2022/candidates/emmanuelpacquiao/)",
            "(https://www.abs-cbn.com/halalan2022/candidates/manny-pacquiao)"
        ]
    },
    "leni robredo": {
        "full_name": "Maria Leonor Gerona Robredo",
        "age": "57 (Born April 23, 1965)",
        "positions": [
            "Vice President of the Philippines (2016-2022)",
            "Representative, Camarines Sur (2013-2016)"
        ],
        "education": [
            "University of the Philippines (BA Economics)",
            "University of Nueva Caceres (Law)"
        ],
        "projects": [
            "Angat Buhay Program",
            "Bayanihan E-Konsulta",
            "Vaccine Express"
        ],
        "links":[
            "(https://www.gmanetwork.com/news/eleksyon2022/candidates/marialeonorrobredo/)",
            "(https://www.abs-cbn.com/halalan2022/candidates/leni-robredo)"
        ]
    },
}

# ==========================================
# HELPER FUNCTIONS
# ==========================================
"""
WIDTH = 82  # Inner width of the box (between │ and │)

def box_line(label, value):
    # Formats a single labeled row that fits inside the box.
    text = f"  {label:<11}: {value}"
    # Truncate if too long so it doesn't break the border
    if len(text) > WIDTH - 1:
        text = text[:WIDTH - 4] + "..."
    return f"│{text:<{WIDTH}}│"

def box_bullet(value, indent=16):
    # Formats a bullet-point continuation line inside the box.
    text = f"{' ' * indent}• {value}"
    if len(text) > WIDTH - 1:
        text = text[:WIDTH - 4] + "..."
    return f"│{text:<{WIDTH}}│"

def box_blank():
    return f"│{' ' * WIDTH}│"
"""


def show_candidate_list():
    # Returns a formatted string of all 2022 presidential candidates.
    category = "full_name"
    list =[]
    for i, key in enumerate(candidates, start=1):
        list.append(f"{i}. {candidates[key][category]}")
    
    if not list:
        return "No candidates found."

    list.append("\n\n(https://www.comelec.gov.ph/php-tpls-attachments/2022NLE/TentativeListsofCandidates/NATIONAL_01112022.pdf)")
    
    fullList = "\n".join(list)
    return fullList

    
def show_candidate_profile(name_key):
    # Returns a list of info about the Presidential candidate being asked about
    c = candidates[name_key]
    info = []

    info.append(f"Name: {c["full_name"]}")  
    info.append(f"Age: {c["age"]}")

    positions = c.get("positions", [])
    positionsList = ", ".join(positions)
    info.append(f"Position(s): {positionsList}")

    education = c.get("education", [])
    educationList = ", ".join(education)
    info.append(f"Education: {educationList}")

    projects = c.get("projects", [])
    projectsList = ", ".join(projects)
    info.append(f"Projects: {projectsList}")

    links = c.get("links", [])
    linksList = "\n".join(links)
    info.append(linksList)

    return "\n\n".join(info)
   

def find_candidate(user_input):
    """
    Checks if the user's input matches any candidate name.
    Returns the matching key or None.
    """
    user_input_lower = user_input.lower()
    for key in candidates:
        if key in user_input_lower:
            return key
        for word in key.split():
            if len(word) > 3 and word in user_input_lower:
                return key
    return None

# ==========================================
# MEMBER ASSIGNMENT ZONE
# Pairs list following the sampleBot.py format.
# ==========================================

# TODO: add pair for find_candidate(), show_candidate_profile()

pairs = [
    # --- GREETINGS ---
    [r'hi|hello|hey|good morning|good afternoon|good evening|magandang bati',
     ['Hello! Welcome to BotoBot!',
      'Hi there! How can I help you today?',
      'Isang magandang bati rin sa iyo! May tanong ka ba tungkol sa pagboboto, eleksyon, mga batas, o mga 2022 presidential na kandidato?']], #filipino example

    # --- HOW ARE YOU ---
    [r'how are you(\?)?|how are you doing(\?)?',
     ['I\'m doing okay, thanks for asking! Ready to share information about elections, voting, laws, or the 2022 presidential candidates!.',
      'All good! How can I help you today? You can ask me about about elections, voting, laws, or the 2022 presidential candidates!']],

    # --- WHAT CAN YOU DO ---
    [r'what can you do|what do you know|help|what are your features',
     ['I can show information about voting or voter\'s registration, presidential elections, related laws, and the list of the Philippine presidential candidates during 2022. I can also provide their profile information. You can try asking: "Show me the 2022 presidential candidates"']],

    # --- SHOW CANDIDATES LIST ---
    [r'.*(show|list|who are|give me|display|tell me).*(2022|presidential).*(candidates?|running|presidenti?a?l?s?).*'
     r'|.*(2022|presidential).*(candidates?).*(philippines?|list|show)?.*'
     r'|.*(candidates?).*(2022|president).*(philippines?)?.*',
     ['__SHOW_LIST__']],

    #integrating other members' pairs here -----------------------------------

    # --- VOTER'S REGISTRATION ---
    [r'^What(.*)(requirement|requirements|need|needed)(.*)(register)?(.*)(vote|voting)',['Here are the requirements to apply for a voter\'s ID:\n1. Bring a valid government-issued ID.\n2. Print and fill up the CEF-1 form (through computer or by pen) before going to the Office of the Election Officer (OEO) OR go the OEO and fill up the CEF-1 form there.\n\n(https://comelec.gov.ph/?r=VoterRegistration/HowtoRegister)']],
    [r'^How(.*)(apply|register)(.*)vote(ID)?',['This is how you apply for a voter\'s ID:\n1. Bring a valid government-issued ID.\n2. Print and fill up the CEF-1 form (through computer or by pen) before going to the Office of the Election Officer (OEO) OR go the OEO and fill up the CEF-1 form there.\n\n(https://comelec.gov.ph/?r=VoterRegistration/HowtoRegister)']],
    [r'^Who(.*)(can|register|qualified|eligible)(.*)vote',
     ['To be a registered voter in the Philippines, a person must be:\n1. At least 18 years old before or on the day of National and Local election.\n2.Be a Philippine resident for at least one (1) year in the place where they wish to vote in for at least six (6) months before the National and Local elections.\n3. Not have the following disqualifications:\n\t3.1. Sentenced by final judgment to suffer imprisonment for at least one (1) year.\n\t3.2. Officially sentenced by final judgment of having committed any crime involving disloyalty to the duly-constituted government (e.g. rebellion, sedition, violation of firearms laws, etc.).\n\t3.3. Declared insane or incompetent by competent authority (unless declared no longer insane or incompentent by proper authority).\n\n(https://comelec.gov.ph/?r=VoterRegistration/WhatisVoterRegistration/RegistrationRequirements)']],
    [r'^What(.*)(ID[s]?)?(use|valid)(.*)*(ID[s]?)?(.*)',
     ['Here is the list of valid IDs you can use when applying for a voter\'s ID:\n1. National identification (ID) card under the philippine Identification System (PhilSys) \n2. Postal ID card\n3. PWD ID Card\n4. Student\'s ID card or library card, signed by the school authority\n5. SC\'s ID card\n6. Land Transportation Office (LTO) Driver\'s license/Student Permit\n7. National Bureau of Investigation (NBI) clearance\n8. Philippine Passport\n9. Social Security System (SSS)/Government Service Insurance System (GSIS) or other Unified Multi-Purpose ID card\n10. Integrated Bar of the Philippines (IBP) ID card\n11. License issued by the Professional Regulatory Commission (PRC)\n12. Certificate of Confirmation issued by the National Commission on Indigenous Peoples (NCIP) in case of members of ICCs or Ips\n13. Barangay Identification / Certification with photo\n\nNOTE: Barangay ID or certificate, Company ID, Cedula, and Police clearances will not be accepted.\n\n(https://comelec.gov.ph/?r=VoterRegistration/WhatisVoterRegistration/RegistrationRequirements)']],
    [r'^Where (can|do) I vote', ['Voting is done at the voting precinct assigned to you.']],
    [r'^Where(.*)voting precinct', ['You can find your voting precinct at COMELEC\'s Precinct Finder with this link: https://precinctfinder.comelec.gov.ph.']],
    [r'^Where(.*)(apply|register|get|)(.*)voter\'s ID',
     ['You can apply for a voter\'s ID at your local COMELEC office a.k.a Office of the Election Officer(OEO).\nFor a list of local offices, visit these links:\nhttps://comelec.gov.ph/?r=ContactInformation/FieldOffices/NCROffices (NCR)\nhttps://comelec.gov.ph/?r=ContactInformation/FieldOffices/ProvincialOffices (provincial)']],

    # --- LAWS ---
    # REPUBLIC ACTS
    [
        r'(?i)^(?:what is|what are|tell me about|explain|can you explain)\s+(?:ra|republic act)\s*(\d+)\??$',
        [
            "You brought up Republic Act %2. Just to make sure we're on the same page: RA 9006 is the Fair Election Act, RA 9369 covers the Automated Election System, and RA 8189 is all about Voter Registration."
        ]
    ],


    # LEGAL SUBSECTIONS
    [
        r'(?i)^(?:what is|what are|tell me about|explain|can you explain)\s+section\s*(\d+)\s*\(([a-z])\)\??$',
        [
            "Ah, Section %1(%2). That's from the Omnibus Election Code. A common one people ask about is Section 261(a), which strictly deals with vote-buying and vote-selling."
        ]
    ],


    # GENERAL ELECTION OFFENSES
    [
        r'(?i)^(?:what are|what is|tell me about|explain|what are the penalties for)\s+(?:the\s+)?(?:omnibus election code|bp\s*881|election code|vote buying|liquor ban)(?:.*)?\??$',
        [
            "Under the Omnibus Election Code (BP 881), things like vote-buying or violating the liquor ban are serious election offenses. Anyone caught faces 1 to 6 years in jail, and no probation is allowed."
        ]
    ],


    # VOTER QUALIFICATIONS
    [
        r'(?i)^(?:who can vote|can i vote|what are the voter requirements|what are the voter qualifications|who is qualified to vote)\??$',
        [
            "To be eligible to vote, you need to be a Filipino citizen and at least 18 years old. You also must have lived in the Philippines for at least a year, and in the specific city or town where you plan to vote for at least 6 months before election day."
        ]
    ],


    # STRICT MATCHING
    [
        r'(?i)^what are my rights\??$',
        [
            "Under the 1987 Constitution, suffrage (the right to vote) is a fundamental right granted to all eligible citizens. No literacy, property, or other substantive requirements shall be imposed."
        ]
    ],

    # -- ELECTION --
    [r'(when|how often|at what date|at what time) (do|are) (elections|presidential elections|national elections) (take place|held|conducted|started|happen)(\?)*', ['According to Article VII, Section 4 of the 1987 Constitution, the President and Vice-President are elected by direct vote of the people every six years.']],

    [r'(how many|what number of) terms (can|does|) (a|the|any) (president|presidential candidate) serve(\?)*', ['A Philippine president is limited to one single six-year term. The Constitution explicitly states that "the President shall not be eligible for any reelection."']],

    [r'(what is the difference|what are the differences|difference|differences) between (a|the) ((presidential election|presidential election year) and (a|the) (midterm election|midterm election year)|(midterm election|midterm election year) and (a|the) (presidential election|presidential election year))(\?)*', ['The presidential election happen every six years in order to select a new president, while the midterm election happens every 3 years in order to replace 12 seats in the senate.']],

    [r'(can|is it possible for) (a candidate|an independent candidate) (run for|join for) a national position (without a|with no) (political party|party)(\?)*', ['Yes. Under Philippine election law, an individual does not need to be a member of a registered political party to run for office. Anyone who meets the legal qualifications may file a Certificate of Candidacy (COC) as an independent candidate.']],

    [r'(what |what are the )*(qualifications|requirements)( required | needed )*(in order |for a person )*to run (for|as a) (president|presidential candidate)(\?)*', ['In order to run as a presidential candidate a person must be, a natural born citizen of the Philippines, a registered voter, be literate, be at least 40 years old on the day of election, and have been a resident of the Philippines for at least 10 years immediately before the election.']],


    #--TESTING--
    [r'(.*)ipinangako ba ni leni robredo na magiging corrupt yung pamahalaan niya(.*)',['Ayon sa artikulo ng VERA Files Fact Check, ang bailta na ito ay hindi totoo, at ginupit na news clip lamang galing sa Abril 2 na episodyo ng \'24 Oras Weekend\' kung saan sinabi ni Robredo: \"Ang pinapangako po namin ni Senator Kiko sa inyo, isang pamahalaan na hindi lang korap… Na \'pag ang gobyerno \'di korap, \'pag ang mga lingkod-bayan matitino at mahuhusay, kahit kakarampot ang pera ng pamahalaan, marami ang matutulungan."\n\n(https://verafiles.org/articles/vera-files-fact-check-fb-pages-mislead-robredo-clip-during-b)']],

    [r'(.*)sino si leody de guzman(.*)', ['__SHOW_PROFILE__']],

    [r'(.*)ano ang mga kailangan para makaboto(.*)', ['Narito ang mga kinakailangan upang mag-aplay para sa voter’s ID:\n1. Magdala ng balidong ID na inisyu ng gobyerno.\n2. I-print at punan ang CEF-1 form (gamit ang kompyuter o panulat) bago pumunta sa Office ng Election Officer (OEO), o pumunta sa OEO at punan ang CEF-1 form doon.\n\n(https://comelec.gov.ph/?r=VoterRegistration/HowtoRegister)']],

    [r'(.*)ano ang section 261\(a\)(.*)',['Ah, Seksyon 261(a). Mula \'yan sa Omnibus Election Code. Isa sa mga karaniwang tinatanong ng mga tao ay ang Seksyon 261(a), kung saan tinatalakay nito ang vote-buying at vote-selling.\n(https://comelec.gov.ph/?r=References/RelatedLaws/OmnibusElectionCode/OECArt22)']],
    

    # --- QUIT ---
    [r'quit|bye|goodbye|exit|see you',
     ['Goodbye! Stay informed and vote for a better future for the Philippines!',
      'Bye-bye! Remember to always vote wisely!',
      'See you later! Keep learning about Philippine politics!']],
]

# ==========================================
# CORE CHATBOT EXECUTION
# ==========================================

# chat icons
USER_AVATAR = "UserMascot.png"
BOT_AVATAR = "BotoBotMascot.png"

# 3. Configure the Streamlit UI layout
st.set_page_config(page_title="BotoBot Chatbot", page_icon=BOT_AVATAR)
#st.title("🤖 BotoBot Chatbot")
st.image("BotoBot_WideLogoTransparent.png", width="stretch")
st.caption("An NLP-powered chatbot for voter education. This is a prototype developed by DLSU Computer Science Students")

# 4. Initialize NLTK Chat engine in Streamlit's session resource state
@st.cache_resource
def get_bot():
    return Chat(pairs, reflections)

nltk_chatbot = get_bot()

# 5. Initialize conversation history memory bucket
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", 
         "avatar": BOT_AVATAR, 
         "content": "Welcome to BotoBot! Ask me a question about the 2022 Philippine presidential candidates, election laws or info, or voting processes!"}
    ]

# 6. Render persistent chat history logs directly to UI layout containers
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message.get("avatar")):
        st.markdown(message["content"])

# 7. Accept user input triggers and map chat workflows
if prompt := st.chat_input("Type your message here..."):

# Render user prompt interface elements immediately
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "avatar": USER_AVATAR, "content": prompt})
    
    # Process prompt using NLTK reflection engine matching
    bot_response = nltk_chatbot.respond(prompt)

    # Handle the special candidate list trigger
    if bot_response == '__SHOW_LIST__':
        bot_response =(show_candidate_list())

    if bot_response == '__SHOW_PROFILE__':
            bot_response =(show_candidate_profile('bongbong marcos'))
    
    # Render fallback assistant validation blocks if NLTK yields an empty string
    if not bot_response:
        bot_response = "I'm not sure I understand or I can not give an answer based on the dataset available to me right now."

    # Render structural bot outputs inside chat UI container blocks
    with st.chat_message("assistant", avatar=BOT_AVATAR):
        st.markdown(bot_response)
    st.session_state.messages.append({"role": "assistant", "avatar": BOT_AVATAR, "content": bot_response})
