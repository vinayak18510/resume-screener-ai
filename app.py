# app.py
import streamlit as st
from modules.pdf_parser import extract_text_from_pdf, get_word_count
from modules.skill_extractor import get_skill_frequency
from modules.matcher import compute_match, get_score_label
from modules.ai_suggestions import get_ai_suggestions
from modules.chart_builder import create_skill_frequency_chart, create_match_gauge

st.set_page_config(page_title='Resume AI Screener', page_icon='🔍', layout='wide', initial_sidebar_state='collapsed')

# Custom Dark Theme Styles
st.markdown("""
<style>
    main { background-color: #0F172A; }
    .stApp { background-color: #0F172A; }
    h1, h2, h3, p, label { color: #E2E8F0 !important; }
    .stButton>button {
        background: linear-gradient(135deg, #6366F1, #8B5CF6);
        color: white; border: none; border-radius: 8px;
        padding: 0.6rem 2rem; font-size: 1rem; font-weight: 600;
        width: 100%; transition: all 0.3s;
    }
    .stButton>button:hover { opacity: 0.85; transform: translateY(-1px); }
    .skill-chip {
        display: inline-block; padding: 4px 12px;
        border-radius: 20px; margin: 3px; font-size: 0.85rem;
        font-weight: 500; color: white;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 style="text-align:center;">🔍 Resume AI Screener</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color: #94A3B8;">Upload your resume, paste a target job description, and get instant alignment analytics</p>', unsafe_allow_html=True)
st.markdown('---')

col1, col2 = st.columns(2)
with col1:
    st.subheader('📄 Upload Resume')
    uploaded_file = st.file_uploader('Drop your PDF resume here', type=['pdf'], help='Max file size: 10MB')
    if uploaded_file:
        st.success(f"'{uploaded_file.name}' loaded successfully!")

with col2:
    st.subheader('💼 Job Description')
    jd_text = st.text_area('Paste the target job details here', height=200, placeholder='Looking for a data professional fluent in Python, SQL...')

st.markdown('<br>', unsafe_allow_html=True)
analyse_btn = st.button('Analyze Alignment Matrix', use_container_width=True)

if analyse_btn:
    if not uploaded_file:
        st.error('Please upload a resume PDF first!')
        st.stop()
    if not jd_text.strip():
        st.error('Please include a job description profile target!')
        st.stop()
        
    with st.spinner('Parsing structure variables...'):
        resume_text = extract_text_from_pdf(uploaded_file)
        if not resume_text:
            st.error('Could not extract text. Please ensure the document is not an unflattened image/scan.')
            st.stop()
            
        result = compute_match(resume_text, jd_text)
        score = result['score']
        label, color = get_score_label(score)
        resume_freq = get_skill_frequency(resume_text)
        suggestions = get_ai_suggestions(resume_text, jd_text, result['missing_skills'], score)
        
        st.markdown('---')
        st.subheader('📊 Processing Matrix Analytics')
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric('Match Percentage Score', f"{score}%")
        m2.metric('Intersecting Skills Found', len(result['matched_skills']))
        m3.metric('Identified Gaps Matrix', len(result['missing_skills']))
        m4.metric('Total File Words Checked', get_word_count(resume_text))
        
        gauge_col, info_col = st.columns([1, 2])
        with gauge_col:
            st.plotly_chart(create_match_gauge(score), use_container_width=True)
        with info_col:
            st.markdown(f"### Hierarchy Status: <span style='color:{color};'>{label}</span>", unsafe_allow_html=True)
            st.markdown(f"Your experience map satisfies **{score}%** of the current target constraints.")
            
        st.markdown('---')
        skills_col1, skills_col2 = st.columns(2)
        
        with skills_col1:
            st.subheader('✅ Intersecting Skills')
            if result['matched_skills']:
                chips = ''.join([f'<span class="skill-chip" style="background: #064E3B; color: #6EE7B7">{s}</span>' for s in sorted(result['matched_skills'])])
                st.markdown(chips, unsafe_allow_html=True)
            else:
                st.info('No overlapping technical skills detected.')
                
        with skills_col2:
            st.subheader('⚠️ Missing Skill Alignment')
            if result['missing_skills']:
                chips = ''.join([f'<span class="skill-chip" style="background: #450A0A; color: #FCA5A5">{s}</span>' for s in sorted(result['missing_skills'])])
                st.markdown(chips, unsafe_allow_html=True)
            else:
                st.success('Zero skill gaps found relative to this profile!')
                
        st.markdown('---')
        st.subheader('📈 Profile Keyword Distribution densities')
        if resume_freq:
            st.plotly_chart(create_skill_frequency_chart(resume_freq), use_container_width=True)
        else:
            st.info('Insufficient quantitative instances to generate distribution profiles.')
            
        st.markdown('---')
        st.subheader('🤖 Generative Matrix Optimization Advice')
        with st.expander('View Detailed Optimization Strategies', expanded=True):
            st.markdown(suggestions)