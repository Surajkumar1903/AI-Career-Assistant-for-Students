"""
LinkedIn Optimizer routes
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

from utils.linkedin_engine import generate_linkedin_content

linkedin_bp = Blueprint('linkedin', __name__)


@linkedin_bp.route('/linkedin-optimizer', methods=['GET', 'POST'])
@login_required
def optimizer():
    """LinkedIn profile optimizer page"""
    content = None

    if request.method == 'POST':
        name         = request.form.get('name', current_user.full_name or current_user.username)
        role         = request.form.get('role', '')
        skills       = request.form.get('skills', '')
        experience   = request.form.get('experience', '')
        achievements = request.form.get('achievements', '')
        education    = request.form.get('education', '')

        skills_list = [s.strip() for s in skills.split(',') if s.strip()]
        content = generate_linkedin_content(name, role, skills_list, experience, achievements, education)

    return render_template('linkedin.html', content=content)


@linkedin_bp.route('/api/linkedin', methods=['POST'])
@login_required
def api_linkedin():
    """JSON API for LinkedIn content generation"""
    data = request.get_json()
    content = generate_linkedin_content(
        data.get('name', ''),
        data.get('role', ''),
        data.get('skills', []),
        data.get('experience', ''),
        data.get('achievements', ''),
        data.get('education', '')
    )
    return jsonify(content)
