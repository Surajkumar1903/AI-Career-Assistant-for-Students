"""
Dashboard routes - main user hub with analytics
"""
from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
import json

from models.user import ResumeAnalysis, Resume
from utils.skill_recommend import skill_category_counts, career_prediction_hint

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def home():
    """Main dashboard with analytics cards"""
    # Fetch latest analysis for the current user
    latest = ResumeAnalysis.query.filter_by(user_id=current_user.id)\
                                 .order_by(ResumeAnalysis.analyzed_at.desc())\
                                 .first()

    # All analyses for chart data
    analyses = ResumeAnalysis.query.filter_by(user_id=current_user.id)\
                                   .order_by(ResumeAnalysis.analyzed_at.asc())\
                                   .all()
    total_analyses = len(analyses)

    resume_count = Resume.query.filter_by(user_id=current_user.id).count()

    # Build chart data
    chart_labels = [a.analyzed_at.strftime('%b %d') for a in analyses]
    chart_scores = [round(a.ats_score, 1) for a in analyses]

    skills_found = []
    skills_missing = []
    if latest:
        try:
            skills_found   = json.loads(latest.skills_found)
        except Exception:
            skills_found = []
        try:
            skills_missing = json.loads(latest.skills_missing)
        except Exception:
            skills_missing = []

    career_growth = min(100, round((latest.ats_score if latest else 0) * 1.2, 1))

    # Doughnut chart: skill category coverage from latest analysis
    doughnut = skill_category_counts(skills_found)
    skill_chart_labels = json.dumps(doughnut.get('labels', []))
    skill_chart_data = json.dumps(doughnut.get('data', []))

    pred_field = (current_user.interested_field or (latest.career_field if latest else '') or 'technology')
    career_prediction = career_prediction_hint(
        float(latest.ats_score) if latest else 0.0,
        len(skills_found),
        pred_field,
    )

    # UI metrics inspired by the dashboard mock (heuristics from real data)
    ats_val = float(latest.ats_score) if latest else 0.0
    profile_strength = min(100, round(ats_val * 0.45 + min(len(skills_found) * 4, 40) + min(resume_count * 5, 15)))
    roadmap_progress = min(100, round(career_growth * 0.85))
    interview_ready = min(100, round(min(35 + len(skills_found) * 5, 90) + (5 if total_analyses > 0 else 0)))

    recent_activities = []
    for a in reversed(analyses[-6:]):
        recent_activities.append({
            'title': 'Resume analyzed',
            'detail': f"ATS score {a.ats_score:.0f} · {a.career_field or 'general'}",
            'time': a.analyzed_at.strftime('%b %d · %H:%M'),
            'icon': 'fa-file-alt',
        })
    if not recent_activities:
        recent_activities = [
            {'title': 'Get started', 'detail': 'Upload a resume to unlock your dashboard insights.', 'time': 'Now', 'icon': 'fa-rocket'},
        ]

    recommended_courses = [
        {'title': 'Machine Learning Specialization', 'provider': 'DeepLearning.AI', 'badge': 'Popular', 'rating': '4.9'},
        {'title': 'Google Data Analytics Certificate', 'provider': 'Coursera', 'badge': 'Best seller', 'rating': '4.8'},
        {'title': 'IBM Data Science Professional', 'provider': 'Coursera', 'badge': 'IBM', 'rating': '4.6'},
    ]

    ats_score = float(latest.ats_score) if latest else 0.0
    if ats_score >= 85:
        ats_label = 'Excellent'
    elif ats_score >= 70:
        ats_label = 'Strong'
    elif ats_score >= 55:
        ats_label = 'Good'
    elif ats_score > 0:
        ats_label = 'Build momentum'
    else:
        ats_label = 'Upload resume'

    return render_template(
        'dashboard.html',
        latest=latest,
        resume_count=resume_count,
        skills_found=skills_found,
        skills_missing=skills_missing,
        chart_labels=json.dumps(chart_labels),
        chart_scores=json.dumps(chart_scores),
        career_growth=career_growth,
        total_analyses=total_analyses,
        skill_chart_labels=skill_chart_labels,
        skill_chart_data=skill_chart_data,
        career_prediction=career_prediction,
        profile_strength=profile_strength,
        roadmap_progress=roadmap_progress,
        interview_ready=interview_ready,
        recent_activities=recent_activities,
        recommended_courses=recommended_courses,
        pred_field=pred_field,
        ats_score=ats_score,
        ats_label=ats_label,
    )


@dashboard_bp.route('/api/dashboard-stats')
@login_required
def dashboard_stats():
    """JSON endpoint for live dashboard stats"""
    latest = ResumeAnalysis.query.filter_by(user_id=current_user.id)\
                                 .order_by(ResumeAnalysis.analyzed_at.desc())\
                                 .first()
    resume_count = Resume.query.filter_by(user_id=current_user.id).count()

    return jsonify({
        'ats_score': round(latest.ats_score, 1) if latest else 0,
        'resume_count': resume_count,
        'career_growth': min(100, round((latest.ats_score if latest else 0) * 1.2, 1)),
        'skills_count': len(json.loads(latest.skills_found)) if latest else 0
    })
