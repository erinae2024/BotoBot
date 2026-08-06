# nlp/patterns.py

from nltk.chat.util import reflections

pairs = [
    # ==========================================
    # 1. SPECIFIC ELECTION LAWS & SECTIONS
    # ==========================================
    
    # Catches specifically tracked election laws
    [r'(?i).*(republic act|r\.?a\.?)\s*(9006|9369|8189|7166).*',
     ["Yes, Republic Act %2 is a relevant election law! For context: RA 9006 is the Fair Election Act, RA 9369 covers the Automated Election System, RA 8189 is Voter Registration, and RA 7166 covers Synchronized Elections."]],

    # Catches irrelevant or untracked RAs 
    [r'(?i).*(republic act|r\.?a\.?)\s*(\d+).*',
     ["You mentioned Republic Act %2. However, I only track laws specifically relevant to Philippine elections. The main election laws I can help you with are RA 9006 (Fair Election Act), RA 9369 (Automated Elections), and RA 8189 (Voter Registration)."]],

    # Legal Sections
    [r'(?i).*(section|sec\.?)\s*(\d+)(?:\s*\(([a-z])\))?.*',
     ["Ah, Section %2. That's from the Omnibus Election Code. A common subsection people ask about is Section 261(a), which strictly deals with vote-buying and vote-selling."]],

    # BP 881 & Omnibus Election Code 
    [r'(?i).*(omnibus election code|bp\s*881|liquor ban).*',
     ["Under the Omnibus Election Code (BP 881), things like vote-buying or violating the liquor ban are serious election offenses. Anyone caught faces 1 to 6 years in jail, and no probation is allowed."]],

    # ELECTION OFFENSES (Vote Buying / Selling)
    [r'(?i).*(vote[- ]?buying|vote[- ]?selling|buy(ing)?\s+votes?|sell(ing)?\s+votes?|bili ng boto|bayad.*boto|boto.*bayad).*|.*(vote).*(money|pesos|bribe).*|.*(money|pesos|bribe).*(vote).*',
     ["According to Article XXII (26), Section 261, vote-buying and vote-selling are election offenses where you or another person offers to give money or something valuable to make someone vote for or against a candidate. If you witness or experience someone doing this, immediately do the following:\n1.) If possible, document the offense by taking photos or videos.\n2.) Take note of details such as date and time, place, and what exactly happened.\n\nElection offense reports and other similar problems can be reported using MovePH's #PHVoteWatch Google Form (https://docs.google.com/forms/d/e/1FAIpQLSe7d5ayZyUsWwe8dxHR69swD_IERN0v34WwvM3WwENEgiNicA/viewform).\n\n(https://www.rappler.com/moveph/things-to-do-if-witness-vote-buying-violations-irregularities/)"]],

    # ==========================================
    # 2. VOTING REQUIREMENTS, PRECINCTS, ELIGIBILITY
    # ==========================================

    [r'(?i).*(require|requirement|need|needed).*(register|apply|voter.*id).*|.*(register|apply|voter.*id).*(require|requirement|need|needed).*',
     ["Here are the requirements to apply for a voter's ID:\n1. Bring a valid government-issued ID.\n2. Print and fill up the CEF-1 form (through computer or by pen) before going to the Office of the Election Officer (OEO) OR go the OEO and fill up the CEF-1 form there.\n\n(https://comelec.gov.ph/?r=VoterRegistration/HowtoRegister)"]],
     
    [r'(?i).*(how).*(register|apply for.*id).*|.*(voter.*id|vote).*(registration).*|.*(registration).*(voter.*id|vote).*',
     ["This is how you apply for a voter's ID:\n1. Bring a valid government-issued ID.\n2. Print and fill up the CEF-1 form (through computer or by pen) before going to the Office of the Election Officer (OEO) OR go the OEO and fill up the CEF-1 form there.\n\n(https://comelec.gov.ph/?r=VoterRegistration/HowtoRegister)"]],

    [r'(?i).*(where).*(vote|precinct|polling).*|.*(vote|precinct|polling).*(where).*',
     ["Voting is done at the voting precinct assigned to you. You can find your precinct at COMELEC's Precinct Finder: https://precinctfinder.comelec.gov.ph."]],
     
    [r'(?i).*(how).*(find|check).*(precinct|polling).*|.*(find|check).*(precinct|polling).*(how).*',
     ["Voting is done at the voting precinct assigned to you. You can find your precinct at COMELEC's Precinct Finder: https://precinctfinder.comelec.gov.ph."]],

    [r'(?i).*(qualif|eligib|who can|can (i|we|anyone)|requirement).*(vote|voter).*|.*(vote|voter).*(qualif|eligib|who can|can (i|we|anyone)|requirement).*',
     ["To be a registered voter in the Philippines, a person must be:\n1. At least 18 years old before or on the day of National and Local election.\n2. Be a Philippine resident for at least one (1) year in the place where they wish to vote in for at least six (6) months before the National and Local elections.\n3. Not have the following disqualifications:\n3.1.) Sentenced by final judgment to suffer imprisonment for at least one (1) year.\n\t3.2.) Officially sentenced by final judgment of having committed any crime involving disloyalty to the duly-constituted government (e.g. rebellion, sedition, violation of firearms laws, etc.).\n\t3.3) Declared insane or incompetent by competent authority.\n\n(https://comelec.gov.ph/?r=VoterRegistration/WhatisVoterRegistration/RegistrationRequirements)"]],

    [r'(?i).*(valid|list of|what).*(id|ids).*(vote|voter|register|apply).*|.*(vote|voter|register|apply).*(valid|list of|what).*(id|ids).*',
     ["Here is the list of valid IDs you can use when applying for a voter's ID:\n1. National identification (ID) card (PhilSys)\n2. Postal ID card\n3. PWD ID Card\n4. Student's ID card or library card\n5. Senior Citizen's ID card\n6. LTO Driver's license/Student Permit\n7. NBI clearance\n8. Philippine Passport\n9. SSS/GSIS or UMID card\n10. IBP ID card\n11. PRC License\n12. NCIP Certificate of Confirmation\n13. Barangay Identification / Certification with photo\n\nNOTE: Cedula and Police clearances will not be accepted.\n\n(https://comelec.gov.ph/?r=VoterRegistration/WhatisVoterRegistration/RegistrationRequirements)"]],


    # ==========================================
    # 3. GENERAL ELECTION & CONSTITUTIONAL INFO
    # ==========================================

    # Rights & Suffrage 
    [r'(?i).*(my rights|right to vote|suffrage|voter.*rights|rights.*voter).*',
     ["Under the 1987 Constitution, suffrage (the right to vote) is a fundamental right granted to all eligible citizens. No literacy, property, or other substantive requirements shall be imposed."]],

    # Independent Candidates
    [r'(?i).*(independent|no party|without a party|without party).*',
     ["Yes. Under Philippine election law, an individual does not need to be a member of a registered political party to run for office. Anyone who meets the legal qualifications may file a Certificate of Candidacy (COC) as an independent candidate."]],

    # Midterm vs Presidential 
    [r'(?i).*(difference).*(midterm|presidential).*(midterm|presidential).*|.*(midterm|presidential).*(midterm|presidential).*(difference).*',
     ["The presidential election happens every six years to select a new president, while the midterm election happens every 3 years in order to replace 12 seats in the senate."]],

    # Election Dates/Frequency
    [r'(?i).*(when|how often|date).*(election).*|.*(election).*(happen|start|conduct.*|begin|when).*',
     ['According to Article VII, Section 4 of the 1987 Constitution, the President and Vice-President are elected by direct vote of the people every six years.\n\n(https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/45/25550)']],

    # Term Limits
    [r'(?i).*(term|terms).*(president).*|.*(president).*(term|terms).*',
     ['A Philippine president is limited to one single six-year term. The Constitution explicitly states that "The President shall not be eligible for any reelection".\n\n(https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/45/25550)']],

    # Presidential Qualifications
    [r'(?i).*(qualifi.*|require.*|need).*(president.*).*|.*(president.*).*(qualifi.*|require.*|need).*',
     ['According to Article VII, Section 2 of the 1987 Constitution, in order to run as a presidential candidate a person must be a natural-born citizen of the Philippines, a registered voter, literate, at least 40 years old on the day of election, and a resident of the Philippines for at least 10 years immediately before the election.\n\n(https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/45/25550)']],
    

    # ==========================================
    # 4. FAKE NEWS FACT CHECKS
    # ==========================================

    [r'(?i).*(ernie|ernesto|abella).*(chr|constitutional commission).*|.*(chr|constitutional commission).*(ernie|ernesto|abella).*',
     ['According to VERA FILES, Abella said that the Commission on Human Rights (CHR) is a constitutional commission on July 21 when asked for a comment about President Duterte\'s remark about abolishing the CHR. However, the CHR is technically not a constitutional commission.\n\n(https://verafiles.org/articles/vera-files-fact-check-chr-constitutional-commission)']],

    [r'(?i).*(leody|guzman).*(npa).*|.*(npa).*(leody|guzman).*',
     ['According to an article in Tsek.ph written by Akademiya at Bayan Kontra Disimpormasyon at Dayaan, Leody de Guzman is not a part of the New People\'s Army (NPA). He is an activist and workers\' leader.\n\n(https://www.tsek.ph/totoo-o-hindi-new-peoples-army-npa-member-nga-ba-si-ka-leody-de-guzman/)']],

    [r'(?i).*(isko|francisco|moreno).*(muslim).*|.*(muslim).*(isko|francisco|moreno).*',
     ["According to VERA FILES, a fake post from the Facebook page RIP Manila posted a quote claiming Moreno said he wants Muslims to stay out of Manila. However, there are no news reports about the alleged comment.\n\n(https://verafiles.org/articles/vera-files-fact-check-isko-moreno-did-not-ban-muslims-manila)"]],

    [r'(?i).*(norberto|gonzales).*(rebellion).*|.*(rebellion).*(norberto|gonzales).*',
     ['The claim by Gonzales that there is no law against rebellion in the Philippines is false. The law is under Article 134-136, Title Three, Chapter One of the Revised Penal Code of the Philippines.\n\n(https://www.abs-cbn.com/news/02/18/22/fact-check-hindi-totoong-walang-batas-laban-sa-rebelyon)']],

    [r'(?i).*(panfilo|ping|lacson).*(executive).*|.*(executive).*(panfilo|ping|lacson).*',
     ['The claim that Lacson did not serve under the executive branch is false. Lacson served under the Philippine National Police (PNP), which is under the executive department and part of the DILG according to VERA FILES.\n\n(https://verafiles.org/articles/vera-files-fact-check-fb-post-falsely-claims-lacson-didnt-serve-under-executive-branch)']],

    [r'(?i).*(bongbong|bbm|marcos).*(bangui|windmill).*|.*(bangui|windmill).*(bongbong|bbm|marcos).*',
     ['According to an article from Tsek.ph, the NorthWind Power Development Corporation (NPDC) led the creation of a 70-meter wind farm at Bangui Bay in 2005. Bongbong Marcos supported the project as governor.\n\n(https://www.tsek.ph/si-bongbong-marcos-ang-nanguna-sa-paggawa-ng-bangui-windmills-sa-pagudpud/)']],

    [r'(?i).*(jose|joey|montemayor).*(covid|vaccin).*|.*(covid|vaccin).*(jose|joey|montemayor).*',
     ['According to a VERA FILES article, Montemayor claimed the number of fully vaccinated individuals had not reached 30 million as of early March. His claim is false; DOH data showed more than 63.30 million Filipinos had been vaccinated.\n\n(https://verafiles.org/articles/vera-files-fact-check-presidential-aspirant-joey-montemayor)']],

    [r'(?i).*(manny|pacman|pacquiao).*(college|degree|diploma).*|.*(college|degree|diploma).*(manny|pacman|pacquiao).*',
     ['According to a VERA FILES article, Pacquiao did not complete his degree in three months. He spent 16 months completing his degree through the CCAPS program of the University of Makati (UMak).\n\n(https://verafiles.org/articles/vera-files-fact-check-post-revives-untrue-claim-about-pacqui)']],

    [r'(?i).*(leni|robredo).*(corrupt).*|.*(corrupt).*(leni|robredo).*',
     ['According to a VERA Files Fact Check, this report is false; it is a clipped news segment where Robredo actually promised a government that is not corrupt.\n\n(https://verafiles.org/articles/vera-files-fact-check-fb-pages-mislead-robredo-clip-during-b)']],


    # ==========================================
    # 5. GREETINGS & QUIT
    # ==========================================

    [r'(?i)^\s*(hi+|hello+|hey+|greetings|good morning|good afternoon|good evening)\s*[!?.,]*\s*$',
     ["Hello! Welcome to BotoBot! How can I help you with the 2022 Philippine Presidential Candidates or election info?"]],
    
    [r'(?i)^\s*(quit+|bye+|goodbye|exit)\s*[!?.,]*\s*$',
     ["Goodbye! Stay informed and remember to vote wisely!"]]
]