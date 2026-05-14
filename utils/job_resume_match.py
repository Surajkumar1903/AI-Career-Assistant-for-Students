"""
Job description vs resume matching for Job-Based AI Resume Builder.
Rule-based only — no invented data.
"""
import re
from typing import Any

from utils.resume_parser import SKILL_KEYWORDS, extract_skills

# Common JD / resume noise (lowercase)
_STOP = frozenset({
    'the', 'and', 'for', 'with', 'you', 'will', 'are', 'our', 'this', 'that', 'from', 'your',
    'have', 'has', 'was', 'were', 'been', 'being', 'their', 'what', 'which', 'while', 'about',
    'into', 'through', 'during', 'before', 'after', 'above', 'below', 'between', 'under', 'again',
    'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'each',
    'both', 'few', 'more', 'most', 'other', 'some', 'such', 'only', 'own', 'same', 'than', 'too',
    'very', 'can', 'just', 'should', 'now', 'role', 'team', 'work', 'job', 'description', 'looking',
    'candidate', 'experience', 'years', 'year', 'ability', 'skills', 'strong', 'excellent', 'good',
    'required', 'preferred', 'plus', 'including', 'well', 'using', 'used', 'based', 'opportunity',
})


def skills_from_jd(jd_text: str) -> list[str]:
    """Known tech / soft skills explicitly mentioned in the job description."""
    if not jd_text:
        return []
    lower = jd_text.lower()
    found: list[str] = []
    for skill in SKILL_KEYWORDS:
        if skill.lower() in lower:
            found.append(skill.title() if len(skill) > 3 else skill.upper())
    return list(dict.fromkeys(found))


def _jd_tokens(jd_text: str) -> list[str]:
    """Meaningful tokens from JD for keyword gap analysis."""
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9+.#-]{2,}", jd_text.lower())
    out: list[str] = []
    for w in words:
        if w in _STOP:
            continue
        if w.isdigit():
            continue
        out.append(w)
    return out


def keywords_missing_from_resume(jd_text: str, resume_text: str, limit: int = 24) -> list[str]:
    """
    Important JD keywords (skills + repeated tokens) not found in resume text.
    Does not invent skills — surfaces gaps for the UI.
    """
    resume_lower = (resume_text or "").lower()
    missing: list[str] = []

    for s in skills_from_jd(jd_text):
        if s.lower() not in resume_lower:
            missing.append(s)

    freq: dict[str, int] = {}
    for tok in _jd_tokens(jd_text):
        freq[tok] = freq.get(tok, 0) + 1
    ranked = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    for tok, _ in ranked:
        if len(tok) < 4:
            continue
        if tok in _STOP:
            continue
        if tok in resume_lower:
            continue
        if tok not in [m.lower() for m in missing]:
            missing.append(tok)
        if len(missing) >= limit:
            break
    return list(dict.fromkeys(missing))[:limit]


def _keyword_coverage(jd_text: str, resume_text: str) -> tuple[float, list[str], list[str]]:
    """Fraction of JD skill-keywords present in resume."""
    jd_skills = [s.lower() for s in skills_from_jd(jd_text)]
    if not jd_skills:
        jd_tokens = [t for t in _jd_tokens(jd_text) if len(t) >= 5][:40]
        jd_skills = list(dict.fromkeys(jd_tokens))
    if not jd_skills:
        return 0.5, [], []
    rl = (resume_text or "").lower()
    matched = [s for s in jd_skills if s in rl]
    miss = [s for s in jd_skills if s not in rl]
    cov = len(matched) / len(jd_skills)
    return cov, matched, miss


def _text_overlap_score(chunk: str, terms: list[str]) -> float:
    if not chunk or not terms:
        return 0.0
    low = chunk.lower()
    hits = sum(1 for t in terms if t.lower() in low)
    return min(1.0, hits / max(min(len(terms), 12), 1))


def compute_job_match(parsed: dict, jd_text: str) -> dict[str, Any]:
    """
    Compare parsed resume to JD. All signals are heuristic / keyword based.
    """
    raw = parsed.get("raw_text") or ""
    jd = (jd_text or "").strip()
    user_skills = list(parsed.get("skills") or [])
    jd_skills_list = skills_from_jd(jd)

    cov, matched_jd_skills, missing_jd_skills = _keyword_coverage(jd, raw)
    missing_keywords = keywords_missing_from_resume(jd, raw, limit=28)

    exp = parsed.get("experience") or ""
    edu = parsed.get("education") or ""
    terms = jd_skills_list[:25] or [t for t in _jd_tokens(jd) if len(t) > 4][:25]

    experience_relevance = int(round(100 * _text_overlap_score(exp, terms)))
    project_blob = raw
    if re.search(r"\bproject\b", raw, re.I):
        m = re.search(r"(projects?|academic projects?).{0,1200}", raw, re.I | re.DOTALL)
        if m:
            project_blob = m.group(0)
    project_relevance = int(round(100 * _text_overlap_score(project_blob, terms)))

    edu_bonus = 15 if (edu and edu.strip()) else 0
    exp_bonus = 20 if (exp and exp.strip()) else 0
    cert_n = len(parsed.get("certifications") or [])

    skill_component = cov * 42
    kw_component = min(28, len(matched_jd_skills) * 3)
    ats = int(round(skill_component + kw_component * 0.4 + experience_relevance * 0.18 + project_relevance * 0.12))
    ats += min(10, edu_bonus // 3) + min(8, exp_bonus // 4) + min(5, cert_n * 2)
    ats = max(0, min(100, ats))

    return {
        "ats_match_score": ats,
        "required_skills_from_jd": jd_skills_list,
        "user_skills": user_skills,
        "skills_matched_in_resume": [s for s in jd_skills_list if s.lower() in raw.lower()],
        "skills_missing_from_resume": missing_jd_skills,
        "missing_keywords": missing_keywords,
        "experience_relevance": experience_relevance,
        "project_relevance": project_relevance,
        "matched_jd_skills": matched_jd_skills,
    }


def combined_sections_text(sections: dict) -> str:
    keys = [
        "professional_summary",
        "skills",
        "projects",
        "experience",
        "education",
        "certifications",
        "achievements",
    ]
    return "\n".join(str(sections.get(k) or "") for k in keys)


def compute_match_on_generated_text(original_parsed: dict, sections: dict, jd_text: str) -> dict:
    """JD alignment using optimized resume text (keywords reflected in output)."""
    from utils.resume_parser import extract_skills

    combined = combined_sections_text(sections)
    fake = dict(original_parsed)
    fake["raw_text"] = combined[:25000]
    fake["skills"] = list(dict.fromkeys((original_parsed.get("skills") or []) + extract_skills(combined)))
    if (not fake.get("experience") or not str(fake.get("experience", "")).strip()) and sections.get("experience"):
        fake["experience"] = str(sections.get("experience"))[:4000]
    if (not fake.get("education") or not str(fake.get("education", "")).strip()) and sections.get("education"):
        fake["education"] = str(sections.get("education"))[:3000]
    return compute_job_match(fake, jd_text)
