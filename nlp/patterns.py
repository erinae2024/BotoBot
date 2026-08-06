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
    
    # SAMPLE FAKE NEWS
    [r'(?i)(.*)(ernie|ernesto|abella)(.*)(chr)(.*)(constitutional commission)(.*)',
    ['According to VERA FILES, Abella said that the Commission on Human Rights (CHR) is a constitutional commission on July 21when asked for a comment about President Duterte\'s remark about abolishing the CHR. However, the CHR is technically not a constitutional commission.\n\n(https://verafiles.org/articles/vera-files-fact-check-chr-constitutional-commission)']],

    [r'(?i)(.*)(leody|.*guzman)(.*)(npa)(.*)',
     ['According to an article in Tsek.ph and written by Akademiya at Bayan Kontra Disimpormasyon at Dayaan, Leody de Guzman is not a part of the New Peoples Army (NPA). He is an activist and workers\' leader. He also became the president of the Bukluran ng Manggagawang Pilipino\n\n(https://www.tsek.ph/totoo-o-hindi-new-peoples-army-npa-member-nga-ba-si-ka-leody-de-guzman/)']],

    [r'(?i)(.*)(isko|francisco|moreno)(.*)(muslim)(.*)',
     ["According to VERA FILES, a fake post from the Facebook page RIP Manila, posted the quote about Moreno saying he wants Muslims to stay out of Manila. However, there is no news reports about the alleged comment.\n\n(https://verafiles.org/articles/vera-files-fact-check-isko-moreno-did-not-ban-muslims-manila)"
    ]],

    [r'(?i)(.*)(norberto|gonzales)(.*)(law)(.*)(rebellion)(.*)',
     ['The claim by Gonzales that there is no law against rebellion in the Philippines is false.  The law is under Article 134-136, under the title Three (Crimes Against Public Order), Chapter One (Rebellion, Sedition and Disloyalty) of the Revised Penal Code of the Philippines.\n\n(https://www.abs-cbn.com/news/02/18/22/fact-check-hindi-totoong-walang-batas-laban-sa-rebelyon)']],

    [r'(?i)(.*)(panfilo|ping|lacson)(.*)(executive)(.*)',
     ['The claim that Lacson did not serve under the executive branch is false. This is because Lacson served under the Philippine National Police (PNP), which is under the executive department and part of the Department of Interior and Local Government (DILG) by virtue of Republic Act (RA) No. 6975, as amended by RA No. 8551, according to VERA FILES.\n\n(https://verafiles.org/articles/vera-files-fact-check-fb-post-falsely-claims-lacson-didnt-serve-under-executive-branch)']],

    [r'(?i)(.*)(bongbong|bbm|marcos)(.*)(bangui|windmills)(.*)',
     ['According to an article from Tsek.ph by UP sa Halalan 2022, the NorthWind Power Development Corporation (NPDC) were the ones who led the creation of a 70-meter wind farm at Bangui Bay, Ilocos Norte in 2005. BongBong Marcos only supported the project as governor of Ilocos Norte.\n\n(https://www.tsek.ph/si-bongbong-marcos-ang-nanguna-sa-paggawa-ng-bangui-windmills-sa-pagudpud/)']],

    [r'(?i)(.*)(jose|joey|montemayor)(.*)(covid|vaccin.*)(.*)',
     ['According to a VERA FILES article, Montemayor is against mandatory vaccination. In addition, he claimed that the number of fully vaccinated individuals in the Philippines has not reached 30 million as of early March. His claim is false, according to the data from the Department of Health (DOH) which showed that more than 63.30 million Filipinos have been vaccinated as of March 1.\n\n(https://verafiles.org/articles/vera-files-fact-check-presidential-aspirant-joey-montemayor)']],

    [r'(?i)(.*)(manny|pacman|pacquiao)(.*)(college|degree|diploma)(.*)',
     ['According to a VERA FILES article, Pacquiao did not complete his degree in three months. The truth is that he spent 16 months completing his degree through the College of Continuing, Advanced and Professional Studies (CCAPS) program of the University of Makati (UMak).\n\n(https://verafiles.org/articles/vera-files-fact-check-post-revives-untrue-claim-about-pacqui)']],

    [r'(?i)(.*)((vp)?leni|robredo)(.*)(corrupt|government)(.*)',
     ['According to a VERA Files Fact Check article, this report is false; it is merely a clipped news segment from the April 2 episode of *24 Oras Weekend* in which Robredo said (in Filipino): "What Senator Kiko and I promise you is a government that is not corrupt... Because when the government is not corrupt, and when public servants are upright and competent, even if government funds are meager, many people can be helped."\n\n(https://verafiles.org/articles/vera-files-fact-check-fb-pages-mislead-robredo-clip-during-b)']],

    # 4. GREETINGS & QUIT
    [r'(?i)^\s*(hi+|hello+|hey+|greetings|good morning|good afternoon|good evening)\s*[!?.,]*\s*$',
     ["Hello! Welcome to BotoBot! How can I help you with the 2022 Philippine Presidential Candidates or election info?"]],
    
    [r'(?i)^\s*(quit+|bye+|goodbye|exit)\s*[!?.,]*\s*$',
     ["Goodbye! Stay informed and remember to vote wisely!"]]
]