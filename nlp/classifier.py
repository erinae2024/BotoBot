# nlp/classifier.py

import nltk
from nltk.tokenize import word_tokenize
from nltk.classify import NaiveBayesClassifier

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

TRAINING_DATA = [
    # SHOW CANDIDATE LIST
    ("show the 2022 presidential candidates", "__SHOW_LIST__"),
    ("who is running for president", "__SHOW_LIST__"),
    ("who is running for pangulo", "__SHOW_LIST__"),
    ("give me the list of candidates", "__SHOW_LIST__"),
    ("sino mga kandidato", "__SHOW_LIST__"),
    ("list of candidates", "__SHOW_LIST__"),

    # SHOW PROFILE
    ("tell me about _CANDIDATE_", "__SHOW_PROFILE__"),
    ("tell me about _CANDIDATE_ please", "__SHOW_PROFILE__"),
    ("who is _CANDIDATE_", "__SHOW_PROFILE__"),
    ("sino si _CANDIDATE_", "__SHOW_PROFILE__"),
    ("_CANDIDATE_", "__SHOW_PROFILE__"),
    ("how about _CANDIDATE_", "__SHOW_PROFILE__"),
    ("i mean _CANDIDATE_", "__SHOW_PROFILE__"),
    ("details of _CANDIDATE_", "__SHOW_PROFILE__"),
    ("info about _CANDIDATE_", "__SHOW_PROFILE__"),
    ("information about _CANDIDATE_", "__SHOW_PROFILE__"),
    ("profile of _CANDIDATE_", "__SHOW_PROFILE__"),
    ("what is the platform of _CANDIDATE_", "__SHOW_PROFILE__"),
    ("ano ang plataporma ni _CANDIDATE_", "__SHOW_PROFILE__"),
    ("platform of _CANDIDATE_", "__SHOW_PROFILE__"),
    ("plataporma ni _CANDIDATE_", "__SHOW_PROFILE__"),
    ("_CANDIDATE_ platform", "__SHOW_PROFILE__"),
    ("_CANDIDATE_ 's platform", "__SHOW_PROFILE__"),
    ("what are the credentials of _CANDIDATE_", "__SHOW_PROFILE__"),
    ("credentials of _CANDIDATE_", "__SHOW_PROFILE__"),
    ("_CANDIDATE_ 's credentials", "__SHOW_PROFILE__"),
    ("ano ang mga kredensyal ni _CANDIDATE_", "__SHOW_PROFILE__"),
    ("kredensyal ni _CANDIDATE_", "__SHOW_PROFILE__"),

    # SHOW PROJECTS
    ("what are _CANDIDATE_ projects", "__SHOW_PROJECTS__"),
    ("_CANDIDATE_ projects", "__SHOW_PROJECTS__"),
    ("_CANDIDATE_ 's projects", "__SHOW_PROJECTS__"),
    ("projects of _CANDIDATE_", "__SHOW_PROJECTS__"),
    ("what has _CANDIDATE_ done", "__SHOW_PROJECTS__"),
    ("mga proyekto ni _CANDIDATE_", "__SHOW_PROJECTS__"),
    ("what are her projects", "__SHOW_PROJECTS__"),
    ("what are his projects", "__SHOW_PROJECTS__"),
    ("what are her proyekto", "__SHOW_PROJECTS__"),
    ("what are his proyekto", "__SHOW_PROJECTS__"),

    # VERIFY SPECIFIC PROJECT
    ("tell me about _PROJECT_", "__VERIFY_PROJECT__"),
    ("tell me about the _PROJECT_ project", "__VERIFY_PROJECT__"),
    ("info about _PROJECT_", "__VERIFY_PROJECT__"),
    ("information about _PROJECT_", "__VERIFY_PROJECT__"),
    ("what is _PROJECT_", "__VERIFY_PROJECT__"),
    ("what is the _PROJECT_ project", "__VERIFY_PROJECT__"),
    ("did _CANDIDATE_ create _PROJECT_", "__VERIFY_PROJECT__"),
    ("is _PROJECT_ by _CANDIDATE_", "__VERIFY_PROJECT__"),
    ("is _PROJECT_ created by _CANDIDATE_", "__VERIFY_PROJECT__"),
    ("details of _PROJECT_", "__VERIFY_PROJECT__"),
    ("does _CANDIDATE_ own _PROJECT_", "__VERIFY_PROJECT__"),
    ("is _PROJECT_ a project of _CANDIDATE_", "__VERIFY_PROJECT__"),

    # SHOW AGE
    ("how old is _CANDIDATE_", "__SHOW_AGE__"),
    ("what is _CANDIDATE_ 's age", "__SHOW_AGE__"),
    ("age of _CANDIDATE_", "__SHOW_AGE__"),

    # TAG MATCHING
    ("which candidates prioritize education", "__MATCH_TAG__"),
    ("who focuses on labor and economy", "__MATCH_TAG__"),
    ("what candidate supports health and housing", "__MATCH_TAG__"),
    ("who advocates for women and poverty", "__MATCH_TAG__"),
    ("which candidate has government experience", "__MATCH_TAG__"),
    ("who focuses on labor", "__MATCH_TAG__"),
    ("who are the candidates focused on health", "__MATCH_TAG__"),
    ("candidates focused on health", "__MATCH_TAG__"),
    ("who supports health", "__MATCH_TAG__")
]

def extract_features(text):
    # trying fix for 'credentials' question showing age
    STOP_WORDS = {"what", "is", "are", "the", "of", "a", "an", "i", "how", "about", "which"}

    words = word_tokenize(text.lower())
    return {word: True for word in words if word not in STOP_WORDS}

def train_classifier():
    formatted_data = [(extract_features(text), intent) for (text, intent) in TRAINING_DATA]
    return NaiveBayesClassifier.train(formatted_data)

def get_intent(user_input, classifier, threshold=0.25):
    features = extract_features(user_input)
    dist = classifier.prob_classify(features)
    best_intent = dist.max()
    confidence = dist.prob(best_intent)
    
    if confidence >= threshold:
        return best_intent
    return None