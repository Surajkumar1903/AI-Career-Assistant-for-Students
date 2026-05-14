"""
ATS (Applicant Tracking System) Scorer
Calculates a score 0-100 and provides improvement suggestions
"""

# ── Field-specific required skills ────────────────────────────────────────────
FIELD_SKILLS = {
    'web development': [
        'html', 'css', 'javascript', 'react', 'node.js', 'git', 'responsive design',
        'rest api', 'sql', 'bootstrap', 'typescript', 'vue', 'angular'
    ],
    'data science': [
        'python', 'pandas', 'numpy', 'scikit-learn', 'machine learning', 'sql',
        'matplotlib', 'statistics', 'tensorflow', 'deep learning', 'r', 'tableau'
    ],
    'ai/ml': [
        'python', 'tensorflow', 'pytorch', 'machine learning', 'deep learning',
        'nlp', 'computer vision', 'scikit-learn', 'keras', 'transformers',
        'pandas', 'numpy', 'statistics', 'linear algebra'
    ],
    'cloud computing': [
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'linux',
        'ci/cd', 'jenkins', 'ansible', 'networking', 'security'
    ],
    'cybersecurity': [
        'networking', 'linux', 'python', 'ethical hacking', 'penetration testing',
        'firewalls', 'cryptography', 'siem', 'incident response', 'comptia'
    ],
    'mobile development': [
        'android', 'ios', 'react native', 'flutter', 'kotlin', 'swift',
        'java', 'dart', 'firebase', 'rest api', 'git'
    ],
    'devops': [
        'docker', 'kubernetes', 'jenkins', 'git', 'linux', 'aws', 'ci/cd',
        'terraform', 'ansible', 'monitoring', 'bash', 'python'
    ],
    'general': [
        'python', 'sql', 'excel', 'communication', 'teamwork', 'git',
        'problem solving', 'leadership', 'time management'
    ],
}

# ── Scoring weights ────────────────────────────────────────────────────────────
WEIGHTS = {
    'skills_match':   40,   # % of required skills found
    'education':      15,   # education section present
    'experience':     20,   # experience section present
    'certifications': 10,   # certifications found
    'word_count':     10,   # resume length (200-800 words ideal)
    'contact_info':    5,   # email/phone present
}

IMPROVEMENT_TIPS = [
    "Add a professional summary at the top of your resume.",
    "Quantify your achievements with numbers (e.g., 'Improved performance by 30%').",
    "Use action verbs to start bullet points (e.g., Developed, Implemented, Led).",
    "Tailor your resume keywords to match the job description.",
    "Keep your resume to 1-2 pages for better readability.",
    "Add links to your GitHub, LinkedIn, or portfolio.",
    "Include relevant certifications and online courses.",
    "Use a clean, ATS-friendly format without tables or graphics.",
    "List your most recent experience first (reverse chronological order).",
    "Proofread for grammar and spelling errors.",
    "Add measurable impact to each work experience bullet.",
    "Include both technical and soft skills sections.",
]


def calculate_ats_score(parsed: dict, target_field: str = 'general') -> dict:
    """
    Calculate ATS score and return analysis results.

    Args:
        parsed: dict from resume_parser.parse_resume()
        target_field: career field to match skills against

    Returns:
        dict with ats_score, skills_found, skills_missing, suggestions
    """
    field_key    = target_field.lower()
    required     = FIELD_SKILLS.get(field_key, FIELD_SKILLS['general'])
    found_skills = [s.lower() for s in parsed.get('skills', [])]

    # ── Skills match score ─────────────────────────────────────────────────────
    matched  = [r for r in required if any(r in f or f in r for f in found_skills)]
    missing  = [r for r in required if r not in matched]
    skill_pct = (len(matched) / len(required)) * 100 if required else 0
    skills_score = (skill_pct / 100) * WEIGHTS['skills_match']

    # ── Education score ────────────────────────────────────────────────────────
    edu_score = WEIGHTS['education'] if parsed.get('education', '').strip() else 0

    # ── Experience score ───────────────────────────────────────────────────────
    exp_score = WEIGHTS['experience'] if parsed.get('experience', '').strip() else 0

    # ── Certifications score ───────────────────────────────────────────────────
    cert_score = WEIGHTS['certifications'] if parsed.get('certifications') else 0

    # ── Word count score ───────────────────────────────────────────────────────
    wc = parsed.get('word_count', 0)
    if 200 <= wc <= 800:
        wc_score = WEIGHTS['word_count']
    elif wc < 200:
        wc_score = WEIGHTS['word_count'] * (wc / 200)
    else:
        wc_score = WEIGHTS['word_count'] * max(0.5, 1 - (wc - 800) / 2000)

    # ── Contact info score ─────────────────────────────────────────────────────
    contact = parsed.get('contact', {})
    contact_score = WEIGHTS['contact_info'] if contact.get('email') else 0

    # ── Total ──────────────────────────────────────────────────────────────────
    total = skills_score + edu_score + exp_score + cert_score + wc_score + contact_score
    total = min(100.0, round(total, 1))

    # ── Suggestions ────────────────────────────────────────────────────────────
    suggestions = []
    if skill_pct < 60:
        suggestions.append(f"Add more {target_field} skills. Missing: {', '.join(missing[:5])}.")
    if not parsed.get('education', '').strip():
        suggestions.append("Add an Education section with your degree and institution.")
    if not parsed.get('experience', '').strip():
        suggestions.append("Add an Experience or Projects section to showcase your work.")
    if not parsed.get('certifications'):
        suggestions.append("Add relevant certifications to boost your ATS score.")
    if wc < 200:
        suggestions.append("Your resume is too short. Add more details about your experience and skills.")
    if not contact.get('email'):
        suggestions.append("Make sure your email address is clearly visible.")

    # Add general tips
    import random
    extra = random.sample(IMPROVEMENT_TIPS, min(3, len(IMPROVEMENT_TIPS)))
    suggestions.extend(extra)

    return {
        'ats_score':      total,
        'skills_found':   [s.title() for s in matched],
        'skills_missing': [s.title() for s in missing],
        'suggestions':    suggestions[:8],
        'breakdown': {
            'skills':         round(skills_score, 1),
            'education':      edu_score,
            'experience':     exp_score,
            'certifications': cert_score,
            'word_count':     round(wc_score, 1),
            'contact':        contact_score,
        }
    }
