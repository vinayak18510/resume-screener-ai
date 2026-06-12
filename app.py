# app.py
import streamlit as st
import pdfplumber
from dotenv import load_dotenv

# 1. Pipeline Structural Imports
from modules.skill_extractor import extract_skills, get_skill_frequency
from modules.matcher import compute_match
from modules.chart_builder import create_skill_frequency_chart
from modules.ai_suggestions import get_ai_suggestions

# Load global environment credentials
load_dotenv()

# Configure uniform workspace layout parameters
st.set_page_config(
    page_title="Resume AI Screener & Matrix Dashboard",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Resume AI Screener & Alignment Matrix")
st.markdown("---")

# 2. Workspace Viewports & Text Container Boundaries
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Candidate Profile Repository")
    uploaded_file = st.file_uploader("Upload Target Resume (PDF Format Only)", type=["pdf"])
    
    resume_text = ""
    if uploaded_file is not None:
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                # Loop through pages and extract structural text layers
                for page in pdf.pages:
                    text_content = page.extract_text()
                    if text_content:
                        resume_text += text_content + "\n"
            st.success(f"'{uploaded_file.name}' loaded successfully into text buffers!")
        except Exception as e:
            st.error(f"PDF Extraction Failure: {str(e)}")

with col2:
    st.subheader("📋 Target Job Specification Matrix")
    jd_text = st.text_area("Paste the explicit hiring criteria or role specifications details here:", height=200)

# 3. Main Analytical Execution Processing Blocks
if st.button("Analyze Alignment Matrix", use_container_width=True):
    if not resume_text:
        st.warning("Action Required: Please supply a valid candidate resume PDF to initialize scanning parameters.")
    elif not jd_text:
        st.warning("Action Required: Please input a destination job profile matrix description to run computations.")
    else:
        st.markdown("### 📊 Live Analytics Portfolio Breakdown")
        
        # A. RUN THE LINGUISTIC NLP PROCESSING LOOPS
        # We explicitly name this 'extracted_skills' so all subsequent references map perfectly
        extracted_skills = extract_skills(resume_text)
        jd_skills = extract_skills(jd_text)
        
        # B. CALCULATE ALIGNMENT INDICES (SET INTERSECTIONS)
        # Using standard variable names to hold set properties
        missing_skills = jd_skills - extracted_skills
        intersecting_skills = extracted_skills.intersection(jd_skills)
        
        # Basic alignment matrix simulation math
        total_jd_count = len(jd_skills) if len(jd_skills) > 0 else 1
        alignment_score = round((len(intersecting_skills) / total_jd_count) * 100, 2)
        
        # Display Metric Badges
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        metric_col1.metric("Overall Alignment Score", f"{alignment_score}%")
        metric_col2.metric("Matched Key Competencies", len(intersecting_skills))
        metric_col3.metric("Highlighted Skill Deficits", len(missing_skills))
        
        st.markdown("---")
        
        # C. COMPUTE BALANCED FREQUENCY METRICS (FIXED TWO-ARGUMENT PASS)
        # We pass both the raw text content AND the matched skills set tracking variables
        resume_freq = get_skill_frequency(resume_text, extracted_skills)
        
        # D. RENDER DYNAMIC VISUAL CHART BARS
        if resume_freq:
            st.markdown("### 📊 Profile Keyword Distribution Densities")
            # Assumes your custom chart module handles plotting loops natively via Plotly Express
            chart_fig = create_skill_frequency_chart(resume_freq)
            st.plotly_chart(chart_fig, use_container_width=True)
        else:
            st.info("Visual Distribution Notice: No structural keyword dataset densities captured over current criteria profiles.")
            
        st.markdown("---")
        
        # E. LAUNCH DIRECT API HTTPS COACHING ENGINE
        st.markdown("### 🧠 Generative Matrix Optimization Advice")
        with st.expander("View Detailed Optimization Strategies", expanded=True):
            with st.spinner("Authorizing direct secure HTTPS endpoint handshake keys... Generating roadmap..."):
                coaching_payload = get_ai_suggestions(
                    resume_text=resume_text,
                    jd_text=jd_text,
                    missing_skills=missing_skills,
                    score=alignment_score
                )
                st.markdown(coaching_payload)