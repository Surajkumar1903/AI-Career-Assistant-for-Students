"""
AI Career Assistant for Students
Main Flask Application Entry Point
"""

from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
import os

from models.database import db
from models.user import User
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.resume import resume_bp
from routes.career import career_bp
from routes.interview import interview_bp
from routes.linkedin import linkedin_bp
from routes.projects import projects_bp
from routes.certifications import certifications_bp
from routes.admin import admin_bp
from routes.chatbot import chatbot_bp
from routes.contact import contact_bp
from routes.skills import skills_bp

# Load environment variables
load_dotenv()

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)

    # ─── Configuration ────────────────────────────────────────────────────────
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-me')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload
    app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'doc', 'docx'}
    # Auth pages: “Continue with Google / LinkedIn” open these URLs (override in .env for OAuth later).
    app.config['SOCIAL_GOOGLE_URL'] = os.getenv(
        'SOCIAL_GOOGLE_URL', 'https://accounts.google.com/'
    ).strip() or 'https://accounts.google.com/'
    app.config['SOCIAL_LINKEDIN_URL'] = os.getenv(
        'SOCIAL_LINKEDIN_URL', 'https://www.linkedin.com/'
    ).strip() or 'https://www.linkedin.com/'

    # ─── Ensure upload folder exists ──────────────────────────────────────────
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), 'static', 'reports'), exist_ok=True)

    # ─── Initialize extensions ────────────────────────────────────────────────
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ─── Register Blueprints ──────────────────────────────────────────────────
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(career_bp)
    app.register_blueprint(interview_bp)
    app.register_blueprint(linkedin_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(certifications_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(skills_bp)

    # ─── Create database tables ───────────────────────────────────────────────
    with app.app_context():
        db.create_all()
        _seed_admin(app)

    return app


def _seed_admin(app):
    """Create default admin user if not exists"""
    from models.user import User
    from werkzeug.security import generate_password_hash
    admin = User.query.filter_by(email='admin@aicareer.com').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@aicareer.com',
            password=generate_password_hash('Admin@123'),
            is_admin=True,
            full_name='System Admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("[OK] Default admin created: admin@aicareer.com / Admin@123")


# ─── Run ──────────────────────────────────────────────────────────────────────
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
