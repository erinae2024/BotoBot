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
        "full_name": "Ernesto Corpus Abella",
        "age": "72 (Born March 22, 1950)",
        "positions": [
            "Presidential Spokesperson (2016-2017)",
            "Undersecretary, DFA (2017-2021)",
        ],
        "education": [
            "Ateneo de Manila University (MA)",
            "Ateneo de Davao University (BA Pre-Med)",
            "Silliman University (M.Div.)"
        ],
        "projects": [
            "Founder of Hope of Asia",
            "Founder of The Jesus Fellowship"
        ]
    },
    "leody de guzman": {
        "full_name": "Leodegario Quitain de Guzman",
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
        ]
    },
    "isko moreno": {
        "full_name": "Francisco Moreno Domagoso",
        "age": "47 (Born October 24, 1974)",
        "positions": [
            "Mayor of Manila (2019-2022)",
            "Vice Mayor of Manila (2007-2016)",
            "Undersecretary, DSWD (2018)"
        ],
        "education": [
            "Pamantasan ng Lungsod ng Maynila (BSBA)",
            "Arellano University (Law School)"
        ],
        "projects": [
            "Manila COVID-19 Field Hospital",
            "Tondominium & Binondominium Public Housing"
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
            "Ateneo de Davao University (BS Pre-Med)"
        ],
        "projects": [
            "Founder, Partido Demokratiko Sosyalista ng Pilipinas",
            "Peace negotiations with insurgent groups"
        ]
    },
    "panfilo lacson": {
        "full_name": "Panfilo Morena Lacson",
        "age": "73 (Born June 1, 1948)",
        "positions": [
            "Senator of the Philippines (2001-13, 2016-22)",
            "Chief, Philippine National Police (1999-2001)"
        ],
        "education": [
            "Philippine Military Academy (Class of 1971)",
            "Lyceum of the Philippines (MA Gov. Mgmt)"
        ],
        "projects": [
            "National ID System Act (Sponsor)",
            "Anti-Terrorism Act of 2020 (Sponsor)"
        ]
    },
    "faisal mangondato": {
        "full_name": "Faisal Mangondato",
        "age": "59 (Born December 30, 1962)",
        "positions": [
            "Businessman",
            "KTPNAN Presidential Candidate (2022)"
        ],
        "education": [
            "Philippine Women's University"
        ],
        "projects": [
            "Advocacy for Philippine Federalism",
            "Mindanao Peace Initiatives"
        ]
    },
    "bongbong marcos": {
        "full_name": "Ferdinand Romualdez Marcos Jr.",
        "age": "64 (Born September 13, 1957)",
        "positions": [
            "Senator of the Philippines (2010-2016)",
            "Governor of Ilocos Norte (1983-86, 1998-2007)",
            "Representative, Ilocos Norte (1992-95, 2007-10)"
        ],
        "education": [
            "University of Oxford (Special Diploma)",
            "Wharton School of Business (MBA, dropout)"
        ],
        "projects": [
            "Bangui Wind Farm (Initiated during term)",
            "Sama-Sama Tayong Babangon Muli Campaign"
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
        ]
    },
}

# ==========================================
# HELPER FUNCTIONS
# ==========================================

WIDTH = 82  # Inner width of the box (between │ and │)

def box_line(label, value):
    """Formats a single labeled row that fits inside the box."""
    text = f"  {label:<11}: {value}"
    # Truncate if too long so it doesn't break the border
    if len(text) > WIDTH - 1:
        text = text[:WIDTH - 4] + "..."
    return f"│{text:<{WIDTH}}│"

def box_bullet(value, indent=16):
    """Formats a bullet-point continuation line inside the box."""
    text = f"{' ' * indent}• {value}"
    if len(text) > WIDTH - 1:
        text = text[:WIDTH - 4] + "..."
    return f"│{text:<{WIDTH}}│"

def box_blank():
    return f"│{' ' * WIDTH}│"


def show_candidate_list():
    """Returns a formatted string of all 2022 presidential candidates."""
    category = "full_name"
    list =[]
    for i, key in enumerate(candidates, start=1):
        list.append(f"{i}. {candidates[key][category]}")
    
    if not list:
        return "No candidates found."
    
    fullList = "\n".join(list)
    return fullList

    



#remove the format part 2 maybe
def show_candidate_profile(name_key):
    """Returns a formatted profile card for a given candidate."""
    c = candidates[name_key]
    border_top    = "┌" + "─" * WIDTH + "┐"
    border_mid    = "├" + "─" * WIDTH + "┤"
    border_bottom = "└" + "─" * WIDTH + "┘"

    header_text = "  CANDIDATE PROFILE"
    lines = [
        "",
        border_top,
        f"│{header_text:<{WIDTH}}│",
        border_mid,
    ]

    # --- Name & Age (always shown) ---
    lines.append(box_line("Name", c["full_name"]))
    lines.append(box_line("Age", c["age"] if c["age"] else "N/A"))

    # --- Positions (list, optional) ---
    positions = c.get("positions", [])
    if positions:
        lines.append(box_blank())
        lines.append(box_line("Position(s)", positions[0]))
        for pos in positions[1:]:
            lines.append(box_bullet(pos))

    # --- Education (list, optional) ---
    education = c.get("education", [])
    if education:
        lines.append(box_blank())
        lines.append(box_line("Education", education[0]))
        for edu in education[1:]:
            lines.append(box_bullet(edu))

    # --- Projects (list, optional) ---
    projects = c.get("projects", [])
    if projects:
        lines.append(box_blank())
        lines.append(box_line("Projects", projects[0]))
        for proj in projects[1:]:
            lines.append(box_bullet(proj))

    lines.append(box_blank())
    lines.append(border_bottom)
    return "\n".join(lines)

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
        r'.*\b(ra|republic act)\b\s*(\d+)\b.*',
        [
            "You brought up Republic Act %2. Just to make sure we're on the same page: RA 9006 is the Fair Election Act, RA 9369 covers the Automated Election System, and RA 8189 is all about Voter Registration."
        ]
    ],


    # LEGAL SUBSECTIONS
    [
        r'.*section\s*(\d+)\s*\(([a-z])\).*',
        [
            "Ah, Section %1(%2). That's from the Omnibus Election Code. A common one people ask about is Section 261(a), which strictly deals with vote-buying and vote-selling."
        ]
    ],


    # GENERAL ELECTION OFFENSES
    [
        r'.*(omnibus|bp\s*881|election\s*code|vote\s*buying|liquor\s*ban).*',
        [
            "Under the Omnibus Election Code (BP 881), things like vote-buying or violating the liquor ban are serious election offenses. Anyone caught faces 1 to 6 years in jail, and no probation is allowed."
        ]
    ],


    # VOTER QUALIFICATIONS
    [
        r'.*(who can vote|can i vote|who to vote|voter requirement|voter qualification).*',
        [
            "To be eligible to vote, you need to be a Filipino citizen and at least 18 years old. You also must have lived in the Philippines for at least a year, and in the specific city or town where you plan to vote for at least 6 months before election day."
        ]
    ],


    # STRICT MATCHING
    [
        r'^what are my rights\??$',
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
st.image("BotoBotWideLogo.png", width="stretch")
st.caption("For CBPCOMM and CBEMC-5, created by Group Ilocos Empanada: Baranquil, Cruz, Evangelio, Magdaluyo")

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
         "content": "Welcome to BotoBot! Ask me question about the 2022 Philippine presidential candidates, election laws or info, or voting processes!"}
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
    
    # Render fallback assistant validation blocks if NLTK yields an empty string
    if not bot_response:
        bot_response = "I'm not sure I understand or I can not give an answer based on the dataset available to me right now."

    # Render structural bot outputs inside chat UI container blocks
    with st.chat_message("assistant", avatar=BOT_AVATAR):
        st.markdown(bot_response)
    st.session_state.messages.append({"role": "assistant", "avatar": BOT_AVATAR, "content": bot_response})

# def run_chatbot():
#     print("\n╔══════════════════════════════════════════════════╗")
#     print("║   2022 PH Presidential Election Info Bot         ║")
#     print("║   Type 'quit' to exit at any time.               ║")
#     print("╚══════════════════════════════════════════════════╝")
#     print("\nBotoBot: Hello! I can tell you about the 2022 Philippine Presidential Candidates.")
#     print("         Try asking: 'Show me the 2022 presidential candidates'\n")

#     while True:
#         try:
#             user_input = input('You: ').strip()

#             if not user_input:
#                 continue

#             if user_input.lower() in ['quit', 'bye', 'exit', 'goodbye']:
#                 print("BotoBot: Goodbye! Stay informed and remember to vote!")
#                 break

#             response = chatbot.respond(user_input)

#             # Handle the special candidate list trigger
#             if response == '__SHOW_LIST__':
#                 print("\nBotoBot:", show_candidate_list())
#                 print("\nBotoBot: Would you like to know more about any of these candidates?")
#                 print("         Just type their name! (e.g., 'Tell me about Leni Robredo')\n")
#                 continue

#             # Check if user is asking about a specific candidate
#             candidate_key = find_candidate(user_input)
#             if candidate_key:
#                 print("\nBotoBot:", show_candidate_profile(candidate_key), "\n")
#                 continue

#             # Use NLTK response if matched
#             if response:
#                 print(f"BotoBot: {response}\n")
#             else:
#                 # Fallback if no pattern matched
#                 print("BotoBot: I'm not sure I understand. Try asking me to 'show the 2022 presidential candidates' or type a candidate's name!\n")

#         except (KeyboardInterrupt, EOFError, SystemExit):
#             print("\nBotoBot: Goodbye! Stay informed and don't forget to vote!")
#             break

# if __name__ == '__main__':
#     run_chatbot()
