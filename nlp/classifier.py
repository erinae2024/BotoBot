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
    ("who is _CANDIDATE_", "__SHOW_PROFILE__"),
    ("sino si _CANDIDATE_", "__SHOW_PROFILE__"),
    ("_CANDIDATE_", "__SHOW_PROFILE__"),
    ("how about _CANDIDATE_", "__SHOW_PROFILE__"),
    ("i mean _CANDIDATE_", "__SHOW_PROFILE__"),
    ("details of _CANDIDATE_", "__SHOW_PROFILE__"),

    # SHOW PROJECTS
    ("what are _CANDIDATE_ projects", "__SHOW_PROJECTS__"),
    ("_CANDIDATE_ projects", "__SHOW_PROJECTS__"),
    ("projects of _CANDIDATE_", "__SHOW_PROJECTS__"),
    ("what has _CANDIDATE_ done", "__SHOW_PROJECTS__"),
    ("mga proyekto ni _CANDIDATE_", "__SHOW_PROJECTS__"),
    ("what are her projects", "__SHOW_PROJECTS__"),
    ("what are his projects", "__SHOW_PROJECTS__"),
    ("what are her proyekto", "__SHOW_PROJECTS__"),
    ("what are his proyekto", "__SHOW_PROJECTS__"),

    # VERIFY SPECIFIC PROJECT
    ("tell me about _PROJECT_", "__VERIFY_PROJECT__"),
    ("what is _PROJECT_", "__VERIFY_PROJECT__"),
    ("did _CANDIDATE_ create _PROJECT_", "__VERIFY_PROJECT__"),
    ("is _PROJECT_ by _CANDIDATE_", "__VERIFY_PROJECT__"),

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
    ("who focuses on labor", "__MATCH_TAG__")
]

def extract_features(text):
    words = word_tokenize(text.lower())
    return {word: True for word in words}

def train_classifier():
    formatted_data = [(extract_features(text), intent) for (text, intent) in TRAINING_DATA]
    return NaiveBayesClassifier.train(formatted_data)

def get_intent(user_input, classifier, threshold=0.35):
    features = extract_features(user_input)
    dist = classifier.prob_classify(features)
    best_intent = dist.max()
    confidence = dist.prob(best_intent)
    
    if confidence >= threshold:
        return best_intent
    return None