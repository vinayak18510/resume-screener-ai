import pdfplumber
import io
import re

def extract_text_from_pdf(uploaded_file) -> str:
    """Extracts all text from an uploaded in-memory PDF file stream."""
    text_pages = []
    
    with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_pages.append(page_text)
                
    full_text = '\n'.join(text_pages)
    cleaned_text = re.sub(r'\s+', ' ', full_text).strip()
    return cleaned_text

def get_word_count(text: str) -> int:
    """Calculates total word length of clean text."""
    return len(text.split())