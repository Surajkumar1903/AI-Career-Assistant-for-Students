"""
Resume Parser - extracts text and structured data from PDF/DOCX resumes
Uses PyPDF2 / pdfplumber for PDF and python-docx for Word files
"""
import re
import os

# ── PDF extraction ─────────────────────────────────────────────────────────────
def _extract_pdf(path: str) -> str:
    """Try pdfplumber first, fall back to PyPDF2"""
    text = ''
    try:
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'
        if text.strip():
            return text
    except Exception:
        pass

    try:
        import PyPDF2
        with open(path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += (page.extract_text() or '') + '\n'
    except Exception:
        pass

    return text


def _extract_docx(path: str) -> str:
    """Extract text from .docx file"""
    try:
        from docx import Document
        doc = Document(path)
        return '\n'.join(p.text for p in doc.paragraphs)
    except Exception:
        return ''


def extract_text(path: str) -> str:
    """Dispatch to correct extractor based on file extension"""
    ext = os.path.splitext(path)[1].lower()
    if ext == '.pdf':
        return _extract_pdf(path)
    elif ext in ('.doc', '.docx'):
        return _extract_docx(path)
    return ''


# ── Section extractors ─────────────────────────────────────────────────────────
SKILL_KEYWORDS = [
    # Programming languages
    'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 'rust',
    'swift', 'kotlin', 'php', 'r', 'scala', 'matlab',
    # Web
    'html', 'css', 'react', 'angular', 'vue', 'node.js', 'nodejs', 'express',
    'django', 'flask', 'fastapi', 'spring', 'laravel', 'bootstrap', 'tailwind',
    # Data / AI
    'machine learning', 'deep learning', 'nlp', 'computer vision', 'tensorflow',
    'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn',
    'opencv', 'hugging face', 'transformers', 'bert', 'gpt',
    # Cloud / DevOps
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'github',
    'gitlab', 'ci/cd', 'terraform', 'ansible',
    # Databases
    'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle',
    'elasticsearch', 'cassandra',
    # Tools
    'linux', 'bash', 'powershell', 'jira', 'confluence', 'figma', 'postman',
    'tableau', 'power bi', 'excel', 'spark', 'hadoop',
    # Soft skills
    'communication', 'teamwork', 'leadership', 'problem solving', 'critical thinking',
    'time management', 'adaptability', 'creativity',
]

CERT_PATTERNS = [
    r'aws\s+certified', r'google\s+certified', r'microsoft\s+certified',
    r'coursera', r'udemy', r'edx', r'ibm\s+certified', r'cisco\s+ccna',
    r'pmp', r'scrum\s+master', r'comptia', r'oracle\s+certified',
    r'deloitte', r'salesforce', r'tensorflow\s+developer',
]


def extract_skills(text: str) -> list:
    """Find skills mentioned in resume text"""
    text_lower = text.lower()
    found = []
    for skill in SKILL_KEYWORDS:
        if skill.lower() in text_lower:
            found.append(skill.title() if len(skill) > 3 else skill.upper())
    return list(dict.fromkeys(found))  # deduplicate preserving order


def extract_education(text: str) -> str:
    """Extract education section"""
    patterns = [
        r'(education|academic|qualification).*?(?=experience|skills|project|certification|$)',
    ]
    for pat in patterns:
        match = re.search(pat, text, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(0)[:500].strip()
    # Fallback: look for degree keywords
    lines = text.split('\n')
    edu_lines = [l for l in lines if any(k in l.lower() for k in
                 ['bachelor', 'master', 'b.tech', 'm.tech', 'b.sc', 'm.sc',
                  'bca', 'mca', 'phd', 'diploma', 'university', 'college'])]
    return '\n'.join(edu_lines[:5])


def extract_experience(text: str) -> str:
    """Extract experience section"""
    match = re.search(
        r'(experience|work history|employment).*?(?=education|skills|project|certification|$)',
        text, re.IGNORECASE | re.DOTALL
    )
    if match:
        return match.group(0)[:800].strip()
    return ''


def extract_certifications(text: str) -> list:
    """Find certifications mentioned in resume"""
    found = []
    text_lower = text.lower()
    for pat in CERT_PATTERNS:
        matches = re.findall(pat, text_lower)
        found.extend(matches)
    return list(set(found))


def extract_contact_info(text: str) -> dict:
    """Extract email and phone from resume"""
    email_match = re.search(r'[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}', text)
    phone_match = re.search(r'(\+?\d[\d\s\-().]{8,15}\d)', text)
    return {
        'email': email_match.group(0) if email_match else '',
        'phone': phone_match.group(0) if phone_match else '',
    }


def parse_resume(path: str) -> dict:
    """
    Main entry point – parse a resume file and return structured data.
    Returns a dict with: raw_text, skills, education, experience, certifications, contact
    """
    raw_text = extract_text(path)

    # Prefer NLTK-backed token count when available (see utils/nlp_helpers.py)
    try:
        from utils.nlp_helpers import tokenize_words

        tw = tokenize_words(raw_text)
        wc = len(tw) if tw else len(raw_text.split())
    except Exception:
        wc = len(raw_text.split())

    return {
        'raw_text':       raw_text,
        'skills':         extract_skills(raw_text),
        'education':      extract_education(raw_text),
        'experience':     extract_experience(raw_text),
        'certifications': extract_certifications(raw_text),
        'contact':        extract_contact_info(raw_text),
        'word_count':     wc,
    }
