"""
AI Chatbot assistant routes
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

from utils.chatbot_engine import get_chatbot_response

chatbot_bp = Blueprint('chatbot', __name__)


@chatbot_bp.route('/chatbot')
@login_required
def chat():
    return render_template('chatbot.html')


@chatbot_bp.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    """Handle chatbot messages"""
    data    = request.get_json()
    message = data.get('message', '').strip()

    if not message:
        return jsonify({'error': 'Empty message'}), 400

    response = get_chatbot_response(message, current_user)
    return jsonify({'response': response, 'user': current_user.username})
