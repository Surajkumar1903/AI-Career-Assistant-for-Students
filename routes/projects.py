"""
Project Recommendation routes
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

from utils.project_engine import recommend_projects, PROJECT_DOMAINS

projects_bp = Blueprint('projects', __name__)


@projects_bp.route('/project-suggestions', methods=['GET', 'POST'])
@login_required
def suggestions():
    """Project recommendation page"""
    projects = None
    selected_domain = ''
    selected_level  = 'beginner'

    if request.method == 'POST':
        skills          = request.form.get('skills', '')
        selected_domain = request.form.get('domain', '')
        selected_level  = request.form.get('level', 'beginner')

        skills_list = [s.strip() for s in skills.split(',') if s.strip()]
        projects = recommend_projects(skills_list, selected_domain, selected_level)

    return render_template(
        'projects.html',
        projects=projects,
        domains=PROJECT_DOMAINS,
        selected_domain=selected_domain,
        selected_level=selected_level
    )


@projects_bp.route('/api/projects', methods=['POST'])
@login_required
def api_projects():
    data    = request.get_json()
    skills  = data.get('skills', [])
    domain  = data.get('domain', '')
    level   = data.get('level', 'beginner')
    result  = recommend_projects(skills, domain, level)
    return jsonify({'projects': result})
