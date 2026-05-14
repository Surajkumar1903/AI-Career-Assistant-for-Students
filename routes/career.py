"""
Career Roadmap Generator routes
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

from utils.career_engine import generate_roadmap, get_career_fields

career_bp = Blueprint('career', __name__)


@career_bp.route('/career-roadmap', methods=['GET', 'POST'])
@login_required
def roadmap():
    """Career roadmap generator page"""
    fields = get_career_fields()
    roadmap_data = None

    if request.method == 'POST':
        current_skills  = request.form.get('current_skills', '')
        interested_field = request.form.get('interested_field', 'Web Development')
        experience_level = request.form.get('experience_level', 'beginner')

        skills_list = [s.strip() for s in current_skills.split(',') if s.strip()]
        roadmap_data = generate_roadmap(skills_list, interested_field, experience_level)

    return render_template(
        'career_roadmap.html',
        fields=fields,
        roadmap=roadmap_data,
        user_field=current_user.interested_field or ''
    )


@career_bp.route('/api/roadmap', methods=['POST'])
@login_required
def api_roadmap():
    """JSON API for roadmap generation (AJAX)"""
    data = request.get_json()
    skills   = data.get('skills', [])
    field    = data.get('field', 'Web Development')
    level    = data.get('level', 'beginner')

    roadmap_data = generate_roadmap(skills, field, level)
    return jsonify(roadmap_data)
