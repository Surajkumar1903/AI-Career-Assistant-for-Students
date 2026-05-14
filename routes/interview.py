"""
Interview Question Generator routes
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required

from utils.interview_engine import generate_questions, QUESTION_CATEGORIES

interview_bp = Blueprint('interview', __name__)


@interview_bp.route('/interview-prep', methods=['GET', 'POST'])
@login_required
def prep():
    """Interview preparation page"""
    questions = None
    selected_category = 'hr'
    selected_level    = 'beginner'
    selected_role     = ''

    if request.method == 'POST':
        selected_category = request.form.get('category', 'hr')
        selected_level    = request.form.get('level', 'beginner')
        selected_role     = request.form.get('role', '')
        count             = int(request.form.get('count', 10))

        questions = generate_questions(selected_category, selected_level, selected_role, count)

    return render_template(
        'interview.html',
        questions=questions,
        categories=QUESTION_CATEGORIES,
        selected_category=selected_category,
        selected_level=selected_level,
        selected_role=selected_role
    )


@interview_bp.route('/api/questions', methods=['POST'])
@login_required
def api_questions():
    """JSON API for question generation"""
    data     = request.get_json()
    category = data.get('category', 'hr')
    level    = data.get('level', 'beginner')
    role     = data.get('role', '')
    count    = int(data.get('count', 10))

    questions = generate_questions(category, level, role, count)
    return jsonify({'questions': questions, 'category': category, 'level': level})
