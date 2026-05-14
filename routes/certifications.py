"""
Certification Recommendation routes
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required

from utils.cert_engine import recommend_certifications, CERT_PROVIDERS

certifications_bp = Blueprint('certifications', __name__)


@certifications_bp.route('/certifications', methods=['GET', 'POST'])
@login_required
def certs():
    """Certification recommendation page"""
    recommendations = None
    selected_provider = ''
    selected_field    = ''

    if request.method == 'POST':
        skills            = request.form.get('skills', '')
        selected_field    = request.form.get('field', '')
        selected_provider = request.form.get('provider', '')
        level             = request.form.get('level', 'beginner')

        skills_list = [s.strip() for s in skills.split(',') if s.strip()]
        recommendations = recommend_certifications(skills_list, selected_field, selected_provider, level)

    return render_template(
        'certifications.html',
        recommendations=recommendations,
        providers=CERT_PROVIDERS,
        selected_provider=selected_provider,
        selected_field=selected_field
    )


@certifications_bp.route('/api/certifications', methods=['POST'])
@login_required
def api_certs():
    data     = request.get_json()
    skills   = data.get('skills', [])
    field    = data.get('field', '')
    provider = data.get('provider', '')
    level    = data.get('level', 'beginner')
    result   = recommend_certifications(skills, field, provider, level)
    return jsonify({'certifications': result})
