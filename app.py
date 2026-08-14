# nlp/patterns.py

from nltk.chat.util import reflections

pairs = [
    # ==========================================
    # 1. VOTING REQUIREMENTS, PRECINCTS, ELIGIBILITY (Evaluated FIRST)
    # ==========================================

    # Voter Eligibility (Catches 'eligible', 'eligble', 'qualified', 'requirements to vote', 'sino pwede bumoto')
    [r'(?i).*(qualif|elig|requirement|who can|who is|sino.*(pwede|pede|qualified)).*(vote|voter|bumoto|boto).*|.*(vote|voter|bumoto|boto).*(qualif|elig|requirement).*',
     ["To be a registered voter in the Philippines, a person must be:\n1. At least 18 years old before or on the day of National and Local election.\n2. Be a Philippine resident for at least one (1) year in the place where they wish to vote in for at least six (6) months before the National and Local elections.\n3. Not have the following disqualifications:\n3.1.) Sentenced by final judgment to suffer imprisonment for at least one (1) year.\n\t3.2.) Officially sentenced by final judgment of having committed any crime involving disloyalty to the duly-constituted government (e.g. rebellion, sedition, violation of firearms laws, etc.).\n\t3.3) Declared insane or incompetent by competent authority.\n\n(https://comelec.gov.ph/?r=VoterRegistration/WhatisVoterRegistration/RegistrationRequirements)"]],

    [r'(?i).*(require|requirement|need|needed).*(register|apply|voter.*id).*|.*(register|apply|voter.*id).*(require|requirement|need|needed).*',
     ["Here are the requirements to apply for a voter's ID:\n1. Bring a valid government-issued ID.\n2. Print and fill up the CEF-1 form (through computer or by pen) before going to the Office of the Election Officer (OEO) OR go the OEO and fill up the CEF-1 form there.\n\n(https://comelec.gov.ph/?r=VoterRegistration/HowtoRegister)"]],
     
    [r'(?i).*(how).*(register|apply for.*id).*|.*(voter.*id|vote).*(registration).*|.*(registration).*(voter.*id|vote).*',
     ["This is how you apply for a voter's ID:\n1. Bring a valid government-issued ID.\n2. Print and fill up the CEF-1 form (through computer or by pen) before going to the Office of the Election Officer (OEO) OR go the OEO and fill up the CEF-1 form there.\n\n(https://comelec.gov.ph/?r=VoterRegistration/HowtoRegister)"]],

    [r'(?i).*(where).*(vote|precinct|polling).*|.*(vote|precinct|polling).*(where).*',
     ["Voting is done at the voting precinct assigned to you. You can find your precinct at COMELEC's Precinct Finder.\n\n(https://precinctfinder.comelec.gov.ph)"]],
     
    [r'(?i).*(how).*(find|check).*(precinct|polling).*|.*(find|check).*(precinct|polling).*(how).*',
     ["Voting is done at the voting precinct assigned to you. You can find your precinct at COMELEC's Precinct Finder.\n\n(https://precinctfinder.comelec.gov.ph)"]],

    [r'(?i).*(valid|list of|what).*(id|ids).*(vote|voter|register|apply).*|.*(vote|voter|register|apply).*(valid|list of|what).*(id|ids).*',
     ["Here is the list of valid IDs you can use when applying for a voter's ID:\n1. National identification (ID) card (PhilSys)\n2. Postal ID card\n3. PWD ID Card\n4. Student's ID card or library card\n5. Senior Citizen's ID card\n6. LTO Driver's license/Student Permit\n7. NBI clearance\n8. Philippine Passport\n9. SSS/GSIS or UMID card\n10. IBP ID card\n11. PRC License\n12. NCIP Certificate of Confirmation\n13. Barangay Identification / Certification with photo\n\nNOTE: Cedula and Police clearances will not be accepted.\n\n(https://comelec.gov.ph/?r=VoterRegistration/WhatisVoterRegistration/RegistrationRequirements)"]],

    # Voting Process Trigger ("how to vote", "paano bumoto")
    [r'(?i).*(how to vote|paano (bumoto|mag vote|magboto|iboto)).*',
     ["To vote in Philippine elections:\n1. Go to your assigned voting precinct on election day.\n2. Get your official ballot from the Electoral Board.\n3. Fully shade the oval next to your chosen candidate's name.\n4. Feed your ballot into the Vote Counting Machine (VCM) and verify your voter receipt.\n\nCheck your precinct here:\n\n(https://precinctfinder.comelec.gov.ph)"]],

    # ==========================================
    # 2. CANDIDATE LISTINGS (Strict Trigger)
    # ==========================================
    
    # Candidate List Trigger (Strictly targets requests for the list of candidates, avoiding eligibility interception)
    [r'(?i).*(who|sino).*(candidate|kandidato).*|.*\b(who to vote|who can i vote for|sino (pede|pwede|dapat) iboto|list of candidates|mga kandidato|who are the candidates)\b.*',
     ["Here are the 2022 Presidential Candidates in my database:\n* Ernesto \"Ernie\" Corpus Abella\n* Maria Leonor \"Leni\" Gerona Robredo\n* Leodegario Quitain de Guzman\n* Francisco Moreno Domagoso\n* Norberto B. Gonzales\n* Panfilo \"Ping\" Morena Lacson\n* Faisal Mangondato\n* Ferdinand Romualdez Marcos Jr.\n* Jose \"Joey\" Cabrera Montemayor Jr.\n* Emmanuel \"Manny\" Dapidran Pacquiao Sr."]],

    # ==========================================
    # 3. SPECIFIC ELECTION LAWS & SECTIONS
    # ==========================================

    [r'(?i).*(laws?|batas).*(elect|halalan).*|.*(elect|halalan).*(laws?|batas).*',
     ["Key Philippine election laws include:\n* **RA 9006** (Fair Election Act): https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/2/3603\n* **RA 9369** (Automated Election System Law): https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/2/7412\n* **RA 8189** (Voter's Registration Act): https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/2/4068\n* **BP 881** (Omnibus Election Code): https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/2/53271"]],
    
    [r'(?i).*(republic act|r\.?a\.?)\s*(9006).*',
     ["Yes, Republic Act 9006 is a relevant election law! Also known as the Fair Election Act, it governs campaign rules and legal media usage during the election period.\n\n(https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/2/3603)"]],

    [r'(?i).*(republic act|r\.?a\.?)\s*(9369).*',
     ["Yes, Republic Act 9369 is a relevant election law! This act covers the authorization and implementation of the Automated Election System (AES) in the Philippines.\n\n(https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/2/7412)"]],

    [r'(?i).*(republic act|r\.?a\.?)\s*(8189).*',
     ["Yes, Republic Act 8189 is a relevant election law! Known as The Voter's Registration Act, it dictates the system of continuing registration for eligible voters.\n\n(https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/2/4068)"]],

    [r'(?i).*(republic act|r\.?a\.?)\s*(7166).*',
     ["Yes, Republic Act 7166 is a relevant election law! This act provides for Synchronized National and Local Elections and outlines the electoral reforms necessary to facilitate them.\n\n(https://www.officialgazette.gov.ph/1991/11/26/republic-act-no-7166/)"]],

    [r'(?i).*(republic act|r\.?a\.?)\s*(\d+).*',
     ["You mentioned Republic Act %2. However, I only track laws specifically relevant to Philippine elections. The main election laws I can help you with are RA 9006 (Fair Election Act), RA 9369 (Automated Elections), and RA 8189 (Voter Registration)."]],

    [r'(?i).*(section|sec\.?)\s*(\d+)(?:\s*\(([a-z])\))?.*',
     ["Ah, Section %2. That's from the Omnibus Election Code. A common subsection people ask about is Section 261(a), which strictly deals with vote-buying and vote-selling."]],

    [r'(?i).*(omnibus election code|bp\s*881|liquor ban).*',
     ["Under the Omnibus Election Code (BP 881), things like vote-buying or violating the liquor ban are serious election offenses. Anyone caught faces 1 to 6 years in jail, and no probation is allowed.\n\n(https://www.comelec.gov.ph/?r=References/RelatedLaws/OmnibusElectionCode/OECArt22)"]],

    [r'(?i).*(vote[- ]?buying|vote[- ]?selling|buy(ing)?\s+votes?|sell(ing)?\s+votes?|bili ng boto|bayad.*boto|boto.*bayad).*|.*(vote).*(money|pesos|bribe).*|.*(money|pesos|bribe).*(vote).*',
     ["According to Article XXII (26), Section 261, vote-buying and vote-selling are election offenses where you or another person offers to give money or something valuable to make someone vote for or against a candidate. If you witness or experience someone doing this, immediately do the following:\n1.) If possible, document the offense by taking photos or videos.\n2.) Take note of details such as date and time, place, and what exactly happened.\n\nElection offense reports and other similar problems can be reported using MovePH's #PHVoteWatch Google Form (https://docs.google.com/forms/d/e/1FAIpQLSe7d5ayZyUsWwe8dxHR69swD_IERN0v34WwvM3WwENEgiNicA/viewform).\n\n(https://www.rappler.com/moveph/things-to-do-if-witness-vote-buying-violations-irregularities/)"]],

    # ==========================================
    # 4. GENERAL ELECTION & CONSTITUTIONAL INFO
    # ==========================================

    [r'(?i).*(my rights|right to vote|suffrage|voter.*rights|rights.*voter).*',
     ["Under Article V of the 1987 Constitution, suffrage (the right to vote) is a fundamental right granted to all eligible citizens. No literacy, property, or other substantive requirements shall be imposed.\n\n(https://www.officialgazette.gov.ph/constitutions/1987-constitution/)"]],

    [r'(?i).*(independent|no party|without a party|without party).*',
     ["Yes. Under Philippine election law, an individual does not need to be a member of a registered political party to run for office. Anyone who meets the legal qualifications may file a Certificate of Candidacy (COC) as an independent candidate.\n\n(https://comelec.gov.ph/?r=References/RelatedLaws/OmnibusElectionCode/OECArt9)"]],

    [r'(?i).*(difference).*(midterm|presidential).*(midterm|presidential).*|.*(midterm|presidential).*(midterm|presidential).*(difference).*',
     ["The presidential election happens every six years to select a new president, while the midterm election happens every 3 years in order to replace 12 seats in the senate. These terms are defined under Articles VI and VII of the 1987 Constitution.\n\n(https://www.officialgazette.gov.ph/constitutions/1987-constitution/)"]],

    [r'(?i).*(when|how often|date).*(elect).*|.*(elect).*(happen|start|conduct.*|begin|when).*',
     ['According to Article VII, Section 4 of the 1987 Constitution, the President and Vice-President are elected by direct vote of the people every six years.\n\n(https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/45/25550)']],

    [r'(?i).*(term|terms).*(president).*|.*(president).*(term|terms).*',
     ['A Philippine president is limited to one single six-year term. The Constitution explicitly states that "The President shall not be eligible for any reelection".\n\n(https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/45/25550)']],

    [r'(?i).*(qualifi.*|require.*|need).*(president.*).*|.*(president.*).*(qualifi.*|require.*|need).*',
     ['According to Article VII, Section 2 of the 1987 Constitution, in order to run as a presidential candidate a person must be a natural-born citizen of the Philippines, a registered voter, literate, at least 40 years old on the day of election, and a resident of the Philippines for at least 10 years immediately before the election.\n\n(https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/45/25550)']],

    # ==========================================
    # 5. FAKE NEWS FACT CHECKS
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
    # 6. HELP, CAPABILITIES, GREETINGS, THANKS, & QUIT
    # ==========================================

    [r'(?i).*(what can (you|u) do|what do (you|u) do|what are your (features|capabilities)|help|capabilities|features|tulong|patulong|alalay|saklolo|kaya mo|pwedeng (itanong|itask)|paano.*gamitin|guide me).*',
     ["I can help you with 2022 Philippine Presidential election information! Here is what you can ask me:\n\n"
      "* **Candidate Profiles & Age:** Ask 'Who is Leni Robredo?' or 'How old is Ping Lacson?'\n"
      "* **Candidate Projects:** Ask 'What are Yorme's projects?' or 'What are Pacquiao's projects?'\n"
      "* **Platform & Advocacy Search:** Ask 'Which candidates prioritize education?' or 'Who focuses on labor?'\n"
      "* **Voting Process & Eligibility:** Ask 'How to vote?' or 'Requirements for voter ID'\n"
      "* **Election Laws & Offenses:** Ask 'What is RA 9006?' or 'What is vote buying?'\n"
      "* **Fact Checking:** Ask 'College degree of Manny Pacquiao' or 'Bangui windmills built by Bongbong Marcos'"]],

    [r'(?i).*\b(hi+|hello+|hey+|greetings|good morning|good afternoon|good evening|magandang (umaga|hapon|gabi|bati)|gandang)\b.*',
     ["Hello! Welcome to BotoBot! How can I help you with the 2022 Philippine Presidential Candidates or election info?"]],
    
    [r'(?i).*\b(thank|thanks|thx|tnx|ty|salam+a+t+|slmt|salamuch|appreciate)\b.*',
     ["You're very welcome! Feel free to ask if you have any more questions."]],
    
    [r'(?i).*\b(quit+|bye+|goodbye|exit|paalam|see you|babay|cge|sige|gege)\b.*',
     ["Goodbye! Stay informed and remember to vote wisely!"]]
]
