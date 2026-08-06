# nlp/patterns.py

from nltk.chat.util import reflections

pairs = [
    # 1. ELECTION LAWS 
    [r'(?i).*(republic act|r\.?a\.?)\s*(\d+).*',
     ["You brought up Republic Act %2. Just to make sure we're on the same page: RA 9006 is the Fair Election Act, RA 9369 covers the Automated Election System, and RA 8189 is all about Voter Registration."]],

    # 2. LEGAL SECTIONS
    [r'(?i).*(section|sec\.?)\s*(\d+)\s*\(([a-z])\).*',
     ["Ah, Section %2(%3). That's from the Omnibus Election Code. A common one people ask about is Section 261(a), which strictly deals with vote-buying and vote-selling."]],

    # 3. VOTING REQUIREMENTS, PRECINCTS, ELIGIBILITY
    [r'(?i).*(require|requirement|need|needed).*(register|apply|voter.*id).*',
     ["Here are the requirements to apply for a voter's ID:\n1. Bring a valid government-issued ID.\n2. Print and fill up the CEF-1 form.\n\n(https://comelec.gov.ph/?r=VoterRegistration/HowtoRegister)"]],
     
    [r'(?i).*(how).*(register|apply for.*id).*',
     ["Here are the requirements to apply for a voter's ID:\n1. Bring a valid government-issued ID.\n2. Print and fill up the CEF-1 form.\n\n(https://comelec.gov.ph/?r=VoterRegistration/HowtoRegister)"]],

    [r'(?i).*(where).*(vote|precinct|polling).*',
     ["Voting is done at the voting precinct assigned to you. You can find your precinct at COMELEC's Precinct Finder: https://precinctfinder.comelec.gov.ph."]],
     
    [r'(?i).*(how).*(find|check).*(precinct|polling).*',
     ["Voting is done at the voting precinct assigned to you. You can find your precinct at COMELEC's Precinct Finder: https://precinctfinder.comelec.gov.ph."]],

    [r'(?i).*(can)?.*(vote).*|.*(vote).*(qualifications|eligibility)',
     ["To be a registered voter in the Philippines, a person must be:\n1. At least 18 years old before or on the day of National and Local election.\n2.Be a Philippine resident for at least one (1) year in the place where they wish to vote in for at least six (6) months before the National and Local elections.\n3. Not have the following disqualifications:\n3.1.) Sentenced by final judgment to suffer imprisonment for at least one (1) year.\n\t3.2.) Officially sentenced by final judgment of having committed any crime involving disloyalty to the duly-constituted government (e.g. rebellion, sedition, violation of firearms laws, etc.).\n\t3.3) Declared insane or incompetent by competent authority (unless declared no longer insane or incompentent by proper authority).\n\n(https://comelec.gov.ph/?r=VoterRegistration/WhatisVoterRegistration/RegistrationRequirements)"]],

    [r'(?i).*(valid)?\bid\b(.*)',
     ["Here is the list of valid IDs you can use when applying for a voter\'s ID:\n1. National identification (ID) card under the philippine Identification System (PhilSys) \n2. Postal ID card\n3. PWD ID Card\n4. Student\'s ID card or library card, signed by the school authority\n5. SC\'s ID card\n6. Land Transportation Office (LTO) Driver\'s license/Student Permit\n7. National Bureau of Investigation (NBI) clearance\n8. Philippine Passport\n9. Social Security System (SSS)/Government Service Insurance System (GSIS) or other Unified Multi-Purpose ID card\n10. Integrated Bar of the Philippines (IBP) ID card\n11. License issued by the Professional Regulatory Commission (PRC)\n12. Certificate of Confirmation issued by the National Commission on Indigenous Peoples (NCIP) in case of members of ICCs or Ips\n13. Barangay Identification / Certification with photo\n\nNOTE: Barangay ID or certificate, Company ID, Cedula, and Police clearances will not be accepted.\n\n(https://comelec.gov.ph/?r=VoterRegistration/WhatisVoterRegistration/RegistrationRequirements)"]],

    # MISC ELECTION INFO
    [r'(?i)((when|how often|date)(.*)(election)|(.*)(elections)(happen|start|conduct.*|begin))',
     ['According to Article VII, Section 4 of the 1987 Constitution, the President and Vice-President are elected by direct vote of the people every six years.\n\n(https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/45/25550)']],

    [r'(?i)(.*)(term|terms)(.*)(president)(.*)|(.*)(president)(.*)(term|terms)(.*)',
     ['A Philippine president is limited to one single six-year term. The Constitution explicitly states that "The President shall not be eligible for any reelection".\n\n(https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/45/25550)']],

    [r'(?i)(.*)(qualifi.*|require.*|need)(.*)(president.*)(.*)|(.*)(president.*)(qualifi.*|require.*|need)(.*)',
     ['According to Artivle VII, Section 2 of the 1987 Constitution, in order to run as a presidential candidate a person must be, a natural born citizen of the Philippines, a registered voter, be literate, be at least 40 years old on the day of election, and have been a resident of the Philippines for at least 10 years immediately before the election.\n\n(https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/45/25550)']],
    
    # 4. GREETINGS & QUIT
    [r'(?i)^\s*(hi+|hello+|hey+|greetings|good morning|good afternoon|good evening)\s*[!?.,]*\s*$',
     ["Hello! Welcome to BotoBot! How can I help you with the 2022 Philippine Presidential Candidates or election info?"]],
    
    [r'(?i)^\s*(quit+|bye+|goodbye|exit)\s*[!?.,]*\s*$',
     ["Goodbye! Stay informed and remember to vote wisely!"]]
]