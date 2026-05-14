"""
Tailored resume content from real parsed resume + JD. No fabricated credentials.
"""
from __future__ import annotations

import json
import os
import re
from typing import Any

from utils.job_resume_match import compute_job_match, skills_from_jd

# JSON keys expected from model and used by exporters
SECTION_KEYS = [
    "professional_summary",
    "skills",
    "projects",
    "experience",
    "education",
    "certifications",
    "achievements",
    "recommended_skills_to_learn",
]


def _strip_json_fence(text: str) -> str:
    t = text.strip()
    if t.startswith("```"):
        t = re.sub(r"^```[a-zA-Z]*\s*", "", t)
        t = re.sub(r"\s*```$", "", t)
    return t.strip()


def _fallback_resume(parsed: dict, job_role: str, match: dict, user) -> dict[str, Any]:
    """Deterministic sections when AI is unavailable."""
    raw = (parsed.get("raw_text") or "").strip()
    skills = parsed.get("skills") or []
    skills_block = "\n".join(f"• {s}" for s in skills) if skills else "• (Add skills to your source resume.)"

    exp = (parsed.get("experience") or raw[:1200]).strip()
    edu = (parsed.get("education") or "").strip()
    certs = parsed.get("certifications") or []
    cert_block = "\n".join(f"• {c}" for c in certs) if certs else "• (None listed in uploaded resume.)"

    proj = ""
    pm = re.search(r"(projects?|portfolio).{0,1500}", raw, re.I | re.DOTALL)
    if pm:
        proj = pm.group(0).strip()[:2000]
    elif raw:
        proj = "See full resume text for project details you provided."

    name = user.full_name or user.username or "Candidate"
    rec = list(match.get("skills_missing_from_resume") or [])[:12]
    if not rec:
        rec = list(match.get("missing_keywords") or [])[:12]

    summary = (
        f"{name} is targeting the {job_role} role. "
        f"Documented strengths include {', '.join(skills[:6]) if skills else 'technical and professional skills drawn from the uploaded resume'}. "
        "The sections below restate only what appears in your original resume—reorganized for clarity and alignment with the job description keywords where accurate."
    )

    achievements = ""
    for line in raw.split("\n"):
        line = line.strip()
        if re.search(r"(award|scholarship|honor|published|rank|won|achievement|certified)", line, re.I):
            achievements += f"• {line}\n"
    if not achievements.strip():
        achievements = "• Highlight quantified wins from your experience in your next edit."

    return {
        "professional_summary": summary[:2000],
        "skills": skills_block[:4000],
        "projects": proj[:6000] or "• (No dedicated project block detected—add projects to your resume file.)",
        "experience": exp[:8000],
        "education": edu[:4000] or "• (No education section detected in parse.)",
        "certifications": cert_block[:3000],
        "achievements": achievements[:4000],
        "recommended_skills_to_learn": rec,
    }


def _gemini_tailored_resume(parsed: dict, jd_text: str, job_role: str, user, match: dict) -> dict[str, Any] | None:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or "your-gemini" in api_key.lower():
        return None

    resume_bundle = json.dumps(
        {
            "parsed_skills": parsed.get("skills"),
            "parsed_education": parsed.get("education"),
            "parsed_experience": parsed.get("experience"),
            "parsed_certifications": parsed.get("certifications"),
            "parsed_contact": parsed.get("contact"),
            "resume_raw_excerpt": (parsed.get("raw_text") or "")[:12000],
        },
        ensure_ascii=False,
    )

    prompt = f"""You are an expert resume editor for ATS and human readers.

CRITICAL RULES (must follow):
1. Use ONLY facts, skills, employers, degrees, dates, and projects that appear in the JSON resume data below. NEVER invent employers, job titles, dates, degrees, metrics, or skills the candidate does not have.
2. You MAY improve wording, ordering, and bullet clarity, and you MAY naturally weave in job-description vocabulary ONLY where it honestly describes something already in the resume (e.g. if they have Python, you can say "Python development").
3. Put any job-required skills or keywords that are NOT clearly evidenced in the resume ONLY in "recommended_skills_to_learn" — do NOT list them in "skills" as if the candidate has them.
4. Output VALID JSON ONLY (no markdown). Use exactly these keys: {json.dumps(SECTION_KEYS)}
5. Each string value uses plain text; use newline-separated bullet lines starting with "• " where appropriate for lists.
6. "recommended_skills_to_learn" must be a JSON array of strings (skills/topics to learn), derived from the job description vs resume gap — not fake resume content.
7. FORMATTING (plain text, ATS-friendly): Professional Summary = 2–4 tight sentences, no fabricated metrics. For "experience", use blocks: line 1 "Company or Organization | Date range" only if both appear in source; line 2 "Job title | Location" when present; then lines starting with "• " for bullets. For "projects", "Project title | Year" when year exists, then a line for tech stack from source, then "• " bullets. For "skills", use lines like "**Programming Languages:** Python, Java" grouping ONLY skills evidenced in the resume. For "certifications", each non-empty line as "Certification Name — Issuing org" when both parts exist in source, else one honest line per item.

Target job role label: {job_role}

Job description:
---
{jd_text[:14000]}
---

Resume data (source of truth):
{resume_bundle}

Match hints (for tone, do not contradict): ATS-style score factors already computed: missing JD skills include {match.get('skills_missing_from_resume', [])[:20]}.
"""

    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-pro")
        resp = model.generate_content(
            prompt,
            generation_config={"temperature": 0.35, "max_output_tokens": 8192},
        )
        text = getattr(resp, "text", None) or ""
        if not text.strip():
            return None
        data = json.loads(_strip_json_fence(text))
        out: dict[str, Any] = {}
        for k in SECTION_KEYS:
            v = data.get(k)
            if k == "recommended_skills_to_learn":
                if isinstance(v, list):
                    out[k] = [str(x).strip() for x in v if str(x).strip()][:30]
                else:
                    out[k] = []
            else:
                out[k] = (str(v).strip() if v is not None else "")[:20000]
        return out
    except Exception:
        return None


def generate_tailored_resume_bundle(parsed: dict, jd_text: str, job_role: str, user) -> dict[str, Any]:
    """
    Returns dict with keys: sections (dict), match (dict), job_role, used_ai (bool)
    """
    match = compute_job_match(parsed, jd_text)
    ai_sections = _gemini_tailored_resume(parsed, jd_text, job_role, user, match)
    used_ai = ai_sections is not None
    sections = ai_sections if used_ai else _fallback_resume(parsed, job_role, match, user)

    # Ensure recommended list is populated from match if model omitted
    rec = sections.get("recommended_skills_to_learn") or []
    if not rec:
        rec = list(dict.fromkeys(
            (match.get("skills_missing_from_resume") or [])
            + (match.get("missing_keywords") or [])[:15]
        ))[:24]
        sections["recommended_skills_to_learn"] = [r for r in rec if isinstance(r, str) and r.strip()][:24]

    return {
        "sections": sections,
        "match": match,
        "job_role": job_role,
        "jd_skill_lexicon": skills_from_jd(jd_text),
        "used_ai": used_ai,
    }
