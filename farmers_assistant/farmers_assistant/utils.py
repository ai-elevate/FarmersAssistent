## utils.py
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def process_text(text: str) -> str:
    """
    Function to process text data for machine learning models.
    """
    # Convert text to lowercase
    text = text.lower()
    # Remove punctuation
    text = ''.join(e for e in text if e.isalnum() or e.isspace())
    return text

def calculate_similarity(text1: str, text2: str) -> float:
    """
    Function to calculate cosine similarity between two texts.
    """
    vectorizer = TfidfVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()
    csim = cosine_similarity(vectors)
    return csim[0][1]

def get_top_n_advice(advice_list: List[str], user_preferences: List[str], n: int) -> List[str]:
    """
    Function to get top n advice based on user preferences.
    """
    advice_scores = []
    for advice in advice_list:
        score = 0
        for preference in user_preferences:
            score += calculate_similarity(advice, preference)
        advice_scores.append((advice, score))
    advice_scores.sort(key=lambda x: x[1], reverse=True)
    top_n_advice = [advice for advice, score in advice_scores[:n]]
    return top_n_advice
