# modules/matcher.py
from modules.skill_extractor import extract_skills

def compute_match(resume_text: str, jd_text: str) -> dict:
    """Calculates comparative Jaccard similarity variants across skill structures."""
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    
    # ---------------------------------------------------------
    # DIAGNOSTIC PRINTS: Watch your VS Code terminal when you click analyze!
    print("\n============== SCREENER DIAGNOSTICS ==============")
    print(f"RAW RESUME TEXT SAMPLE: {repr(resume_text[:150])}")
    print(f"EXTRACTED RESUME SKILLS: {resume_skills}")
    print(f"EXTRACTED JD SKILLS: {jd_skills}")
    print("==================================================\n")
    # ---------------------------------------------------------

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
    }