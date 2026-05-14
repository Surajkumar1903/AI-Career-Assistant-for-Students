"""
Skill recommendation routes (AI-assisted suggestions from resume context)
"""
import json

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

from models.user import ResumeAnalysis
from utils.skill_recommend import recommend_skill_buckets

skills_bp = Blueprint("skills", __name__)


@skills_bp.route("/skill-recommendations", methods=["GET", "POST"])
@login_required
def recommendations():
    """
    Show grouped skill suggestions. Uses the latest resume analysis when available,
    or skills typed manually in the form.
    """
    latest = (
        ResumeAnalysis.query.filter_by(user_id=current_user.id)
        .order_by(ResumeAnalysis.analyzed_at.desc())
        .first()
    )

    manual_skills = ""
    target_field = (current_user.interested_field or "general").strip() or "general"
    buckets = None

    if request.method == "POST":
        manual_skills = request.form.get("skills", "").strip()
        target_field = request.form.get("target_field", target_field).strip() or "general"

        if manual_skills:
            skills_list = [s.strip() for s in manual_skills.split(",") if s.strip()]
        elif latest:
            try:
                skills_list = json.loads(latest.skills_found)
            except Exception:
                skills_list = []
        else:
            skills_list = []

        buckets = recommend_skill_buckets(skills_list, target_field=target_field)

    # GET: pre-compute from latest analysis (optional preview)
    elif latest:
        try:
            skills_list = json.loads(latest.skills_found)
        except Exception:
            skills_list = []
        if skills_list:
            buckets = recommend_skill_buckets(
                skills_list,
                target_field=(current_user.interested_field or "general"),
            )

    return render_template(
        "skills.html",
        latest=latest,
        buckets=buckets,
        manual_skills=manual_skills,
        target_field=target_field,
    )


@skills_bp.route("/api/skill-recommendations", methods=["POST"])
@login_required
def api_recommendations():
    """JSON API for AJAX / integrations."""
    data = request.get_json(silent=True) or {}
    skills = data.get("skills") or []
    field = data.get("field", "general")
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(",") if s.strip()]
    buckets = recommend_skill_buckets(skills, target_field=field)
    return jsonify(buckets)
