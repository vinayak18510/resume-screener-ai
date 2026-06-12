# modules/matcher.py
from modules.skill_extractor import extract_skills

def compute_match(resume_text: str, jd_text: str) -> dict:
    """Calculates comparative Jaccard similarity variants across skill structures."""
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    
    # Set Operations
    matched_skills = resume_skills & jd_skills  # Intersection
    missing_skills = jd_skills - resume_skills  # Difference
    
    if len(jd_skills) == 0:
        score = 0.0
    else:
        score = (len(matched_skills) / len(jd_skills)) * 100
        
    return {
        'score': round(score, 1),
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'resume_skills': resume_skills,
        'jd_skills': jd_skills
    }

def get_score_label(score: float) -> tuple:
    """Assigns specific color codes based on quantitative performance scales."""
    if score >= 80: 
        return ('Excellent Match!', '#10B981')
    elif score >= 60: 
        return ('Good Match', '#6366F1')
    elif score > 40: 
        return ('Moderate Match', '#F59E0B')
    else: 
        return ('Low Match', '#EF4444')