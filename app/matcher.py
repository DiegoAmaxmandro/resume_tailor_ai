import re
from sklearn.feature_extraction.text import CountVectorizer

def clean_text(text):
    # Lowercase and remove special characters
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return text

def extract_keywords(text, top_n=20):
    text = clean_text(text)
    vectorizer = CountVectorizer(stop_words ='english', max_features = top_n, ngram_range=(1, 2))
    X = vectorizer.fit_transform([text])
    return set(vectorizer.get_feature_names_out())

def match_score(resume_text, job_text):
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_text)

    if not job_keywords:
        return 0

    matches = resume_keywords & job_keywords
    score = len(matches) / len(job_keywords) * 100
    return round(score, 2), matches