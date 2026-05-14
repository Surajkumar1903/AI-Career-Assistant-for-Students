"""
AI Skill Recommendation Engine
Suggests technical, soft, AI/ML, and web skills based on resume skills and target field.
Uses scikit-learn TF–IDF to rank skill phrases against a curated corpus (beginner-friendly).
"""
from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ── Curated skill pools (lowercase for matching) ─────────────────────────────
TECHNICAL_SKILLS = [
    "python", "java", "go", "rust", "c++", "sql", "postgresql", "mongodb", "redis",
    "docker", "kubernetes", "linux", "bash", "git", "ci/cd", "aws", "azure", "gcp",
    "terraform", "ansible", "kafka", "elasticsearch", "graphql", "rest api", "oauth",
    "microservices", "system design", "data structures", "algorithms",
]

SOFT_SKILLS = [
    "communication", "teamwork", "leadership", "problem solving", "critical thinking",
    "time management", "adaptability", "emotional intelligence", "stakeholder management",
    "presentation skills", "mentoring", "conflict resolution", "collaboration",
]

AIML_SKILLS = [
    "machine learning", "deep learning", "nlp", "computer vision", "pytorch", "tensorflow",
    "scikit-learn", "pandas", "numpy", "feature engineering", "model deployment", "mlops",
    "llm fine-tuning", "rag", "vector databases", "hugging face", "langchain",
]

WEB_SKILLS = [
    "html", "css", "javascript", "typescript", "react", "vue", "angular", "node.js",
    "express", "django", "flask", "fastapi", "next.js", "tailwind css", "bootstrap",
    "responsive design", "webpack", "vite", "jest", "cypress",
]

# Field-specific emphasis (extra keywords blended into the query text)
FIELD_FOCUS = {
    "web development": "react node javascript typescript css html rest api",
    "data science": "python pandas sql statistics visualization tableau machine learning",
    "ai/ml": "pytorch tensorflow nlp deep learning transformers deployment mlops",
    "ai/ml engineering": "pytorch tensorflow nlp deep learning transformers deployment mlops",
    "cloud computing": "aws azure gcp kubernetes docker terraform networking security",
    "cybersecurity": "networking linux penetration testing siem cryptography incident response",
    "mobile development": "kotlin swift flutter react native firebase rest api",
    "devops": "docker kubernetes jenkins terraform ansible ci/cd monitoring linux",
    "general": "python git sql communication teamwork problem solving",
}


def _title_case_skill(s: str) -> str:
    return s.title() if len(s) > 2 else s.upper()


def _rank_against_corpus(query: str, candidates: list[str], top_n: int = 12) -> list[str]:
    """
    Rank candidate skills by cosine similarity of TF–IDF vectors vs. the query string.
    """
    if not candidates:
        return []
    query = (query or "").lower().strip()
    if not query:
        return [_title_case_skill(c) for c in candidates[:top_n]]

    corpus = [query] + candidates
    vectorizer = TfidfVectorizer(lowercase=True, token_pattern=r"(?u)\b\w[\w\+\#./-]*\b")
    try:
        mat = vectorizer.fit_transform(corpus)
        sims = cosine_similarity(mat[0:1], mat[1:]).flatten()
    except ValueError:
        # Extremely short query — fall back to alphabetical slice
        return [_title_case_skill(c) for c in candidates[:top_n]]

    ranked_idx = sorted(range(len(candidates)), key=lambda i: sims[i], reverse=True)
    out: list[str] = []
    for i in ranked_idx[:top_n]:
        out.append(_title_case_skill(candidates[i]))
    return out


def recommend_skill_buckets(
    resume_skills: list[str],
    target_field: str = "general",
    limit_per_bucket: int = 10,
) -> dict:
    """
    Given skills already detected on a resume, suggest skills the user may be missing,
    grouped into technical, soft, AI/ML, and web development categories.
    """
    have = {s.strip().lower() for s in (resume_skills or []) if s and str(s).strip()}
    field_key = (target_field or "general").lower().strip()
    if "ai/ml" in field_key or "machine learning" in field_key:
        field_key = "ai/ml"
    focus = FIELD_FOCUS.get(field_key, FIELD_FOCUS["general"])

    # Build a rich query: user's skills + field focus (helps TF–IDF context)
    query = " ".join(have) + " " + focus

    def missing(pool: list[str]) -> list[str]:
        return [p for p in pool if p.lower() not in have]

    tech_m = missing(TECHNICAL_SKILLS)
    soft_m = missing(SOFT_SKILLS)
    aiml_m = missing(AIML_SKILLS)
    web_m = missing(WEB_SKILLS)

    return {
        "target_field": target_field or "general",
        "resume_skill_count": len(have),
        "technical": _rank_against_corpus(query, tech_m, limit_per_bucket),
        "soft_skills": _rank_against_corpus(query + " teamwork leadership communication", soft_m, limit_per_bucket),
        "aiml": _rank_against_corpus(query + " machine learning deep learning nlp", aiml_m, limit_per_bucket),
        "web_development": _rank_against_corpus(query + " react javascript css html", web_m, limit_per_bucket),
    }


def skill_category_counts(resume_skills: list[str]) -> dict:
    """
    Count how many detected resume skills fall into each bucket (for Chart.js).
    A skill is counted at most once; priority: aiml → web → technical → soft.
    """
    have = {str(s).strip().lower() for s in (resume_skills or []) if s and str(s).strip()}
    aiml_s = set(AIML_SKILLS)
    web_s = set(WEB_SKILLS)
    tech_s = set(TECHNICAL_SKILLS)
    soft_s = set(SOFT_SKILLS)

    c_aiml = c_web = c_tech = c_soft = 0
    used: set[str] = set()

    for skill in have:
        if skill in used:
            continue
        if skill in aiml_s or any(k in skill for k in ("machine learning", "deep learning", "nlp")):
            c_aiml += 1
            used.add(skill)
        elif skill in web_s or skill in ("javascript", "typescript", "html", "css"):
            c_web += 1
            used.add(skill)
        elif skill in tech_s:
            c_tech += 1
            used.add(skill)
        elif skill in soft_s:
            c_soft += 1
            used.add(skill)

    total = c_aiml + c_web + c_tech + c_soft
    if total == 0 and have:
        # Skills detected but not in our buckets — spread evenly for a visible chart
        n = len(have)
        return {"labels": ["Mapped", "Other"], "data": [max(1, n // 2), max(1, n - n // 2)]}

    return {
        "labels": ["Technical", "Soft Skills", "AI / ML", "Web Dev"],
        "data": [c_tech, c_soft, c_aiml, c_web],
    }


def career_prediction_hint(ats_score: float, skills_count: int, field: str = "") -> str:
    """
    Lightweight, explainable “career readiness” hint (not a statistical forecast).
    """
    field = field or "your target role"
    if ats_score >= 75 and skills_count >= 8:
        return (
            f"Strong profile signal for {field}: resume strength and skill breadth look interview-ready. "
            "Focus on portfolio projects and mock interviews."
        )
    if ats_score >= 55:
        return (
            f"Good momentum toward {field}. Closing skill gaps and adding measurable impact bullets "
            "will likely move you into the ‘strong candidate’ range."
        )
    return (
        f"Early-stage signal for {field}. Prioritize foundational skills, one flagship project, "
        "and a cleaner ATS keyword match to job descriptions."
    )
