import spacy
from data.skills_db import ALL_SKILLS


nlp = spacy.load('en_core_web_sm')

def extract_skills(text: str) -> set:
    """Extracts custom predefined skills using structural lower-case mapping and NLP lemmatization."""
    text_lower = text.lower()
    found_skills = set()
    

    for skill in ALL_SKILLS:
        if skill in text_lower:
            found_skills.add(skill)
            

    doc = nlp(text_lower)
    for token in doc:
        if not token.is_stop and not token.is_punct:
            if token.lemma_ in ALL_SKILLS:
                found_skills.add(token.lemma_)
                
    return found_skills

def get_skill_frequency(text: str) -> dict:
    """Tabulates quantitative keyword instances across text inputs."""
    text_lower = text.lower()
    freq = {}
    for skill in ALL_SKILLS:
        count = text_lower.count(skill)
        if count > 0:
            freq[skill] = count
    return freq