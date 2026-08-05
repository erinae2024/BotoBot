# nlp/patterns.py

# Strict Regex Pairs for NLTK Chat
pairs = [
    # GREETINGS
    [r'(?i).*(hi+|hello+|hey+|greetings|good morning|good afternoon|good evening).*',
     ["Hello! Welcome to BotoBot! How can I help you with the 2022 Philippine Presidential Candidates or election info?"]],
    
    # QUIT
    [r'(?i).*(quit+|bye+|goodbye|exit).*',
     ["Goodbye! Stay informed and remember to vote wisely!"]],

    # ELECTION LAWS (Supports RA 9369, R.A. 9006, Republic Act 8189)
    [r'(?i).*(republic act|r\.?a\.?)\s*(\d+).*',
     ["You brought up Republic Act %2. Just to make sure we're on the same page: RA 9006 is the Fair Election Act, RA 9369 covers the Automated Election System, and RA 8189 is all about Voter Registration."]],

    # LEGAL SECTIONS (Supports Section 261(a), Sec 261(a))
    [r'(?i).*(section|sec\.?)\s*(\d+)\s*\(([a-z])\).*',
     ["Ah, Section %2(%3). That's from the Omnibus Election Code. A common one people ask about is Section 261(a), which strictly deals with vote-buying and vote-selling."]],

    # REQUIREMENTS & PRECINCTS
    [r'(?i).*(require|requirement|requirements|need|needed).*(register|vote).*',
     ["Here are the requirements to apply for a voter's ID:\n1. Bring a valid government-issued ID.\n2. Print and fill up the CEF-1 form.\n\n(https://comelec.gov.ph/?r=VoterRegistration/HowtoRegister)"]],
     
    [r'(?i).*(where|how).*(vote|precinct|polling).*',
     ["Voting is done at the voting precinct assigned to you. You can find your precinct at COMELEC's Precinct Finder: https://precinctfinder.comelec.gov.ph."]]
]