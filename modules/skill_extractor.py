# modules/skill_extractor.py
import spacy
# Import your unified combined set directly from the database file
from data.skills_db import ALL_SKILLS

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def extract_skills(text: str) -> set:
    """Parses text arrays and cross-references data against the unified hard/soft skills set."""
    if not text:
        return set()
        
    doc = nlp(text)
    extracted_skills = set()
    
    for token in doc:
        cleaned_token = token.text.strip().lower()
        
        # Single-letter filter mechanism to strip out character noise like loose list indices
        # --- UPDATED CHARACTER ENGINE LOOP ---
        if len(cleaned_token) == 1:
            # Check for both uppercase and lowercase versions explicitly
            if token.text not in ['C', 'R', 'c', 'r']:
                continue
                
        # Cross-reference the token against your unified set
        if cleaned_token in ALL_SKILLS:
            extracted_skills.add(cleaned_token)
            
    return extracted_skills

# Change "frequencies" to "frequency" to match your app.py orchestrator import
def get_skill_frequency(text: str, targeted_skills: set) -> dict:
    """Computes distribution densities without character-level formatting noise."""
    if not text or not targeted_skills:
        return {}
        
    doc = nlp(text)
    frequency_matrix = {skill: 0 for skill in targeted_skills}
    
    for token in doc:
        cleaned_token = token.text.strip().lower()
        
        if len(cleaned_token) == 1:
            if token.text not in ['C', 'R']:
                continue
                
        if cleaned_token in frequency_matrix:
            frequency_matrix[cleaned_token] += 1
            
    return dict(sorted(frequency_matrix.items(), key=lambda item: item[1], reverse=True))