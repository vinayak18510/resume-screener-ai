# modules/ai_suggestions.py
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def get_ai_suggestions(resume_text: str, jd_text: str, missing_skills: set, score: float) -> str:
    """Sends prompt data directly to Google's HTTPS REST gateway.
    
    Bypasses local library authentication bugs by targeting the active 
    production model path via standard network payloads.
    """
    
    # 1. Fetch developer credentials from the local environment
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return "Initialization Error: No GEMINI_API_KEY found in your .env file."
        
    missing_str = ', '.join(missing_skills) if missing_skills else 'None'
    
    # 2. Construct the structured engineering optimization prompt
    prompt = f"""
    You are an expert career coach and technical recruiter.
    A candidate has uploaded their resume and is applying for a job.
    
    CURRENT MATCH SCORE: {score}%
    MISSING SKILLS: {missing_str}
    
    JOB DESCRIPTION (first 800 chars):
    {jd_text[:800]}
    
    RESUME CONTENT (first 800 chars):
    {resume_text[:800]}
    
    Please provide:
    1. TOP 3 PRIORITY SKILLS to learn (with why each matters for this role)
    2. HOW TO ADD them (projects, courses, certifications)
    3. RESUME FORMATTING TIPS specific to this candidate
    4. ONE actionable project idea that would showcase the missing skills
    
    Be specific, encouraging, and actionable. Format with clear markdown headings.
    """
    
    # 3. Establish the absolute direct Google REST channel gateway
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    # 4. Format JSON request parameters
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    
    # 5. Execute the network request directly past local environment wrappers
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response_data = response.json()
        
        if response.status_code == 200:
            # Parse and return the generated markdown response text cleanly
            return response_data['candidates'][0]['content']['parts'][0]['text']
        else:
            # Catch structural or explicit key-level constraints from Google's router
            error_msg = response_data.get('error', {}).get('message', 'Unknown API Error')
            return f"API Endpoint Error ({response.status_code}): {error_msg}"
            
    except Exception as e:
        return f"Network Connection Error: {str(e)}"