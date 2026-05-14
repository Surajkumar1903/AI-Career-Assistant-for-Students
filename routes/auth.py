"""
Authentication routes: register, login, logout, profile
"""
import os

from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from models.database import db
from models.user import User

auth_bp = Blueprint('auth', __name__)


def _founder_banner_static_url():
    """First existing file under static/images/ used as home founder banner."""
    names = (
        'images/home-founder.png',
        'images/home-founder.jpg',
        'images/home-founder.jpeg',
        'images/home-founder.webp',
    )
    root = current_app.static_folder
    if not root:
        return None
    for rel in names:
        if os.path.isfile(os.path.join(root, rel)):
            return url_for('static', filename=rel)
    return None


@auth_bp.route('/')
def index():
    """Landing / home page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))
    return render_template('index.html', founder_image_url=_founder_banner_static_url())


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))

    if request.method == 'POST':
        username   = request.form.get('username', '').strip()
        email      = request.form.get('email', '').strip().lower()
        password   = request.form.get('password', '')
        confirm    = request.form.get('confirm_password', '')
        full_name  = request.form.get('full_name', '').strip()

        # ── Validation ────────────────────────────────────────────────────────
        if not all([username, email, password, confirm]):
            flash('All fields are required.', 'danger')
            return render_template('register.html')

        if password != confirm:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return render_template('register.html')

        if User.query.filter_by(username=username).first():
            flash('Username already taken.', 'danger')
            return render_template('register.html')

        # ── Create user ───────────────────────────────────────────────────────
        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            full_name=full_name
        )
        db.session.add(user)
        db.session.commit()

        flash('Account created! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))

    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            if not user.is_active:
                flash('Your account has been deactivated.', 'danger')
                return render_template('login.html')

            login_user(user, remember=bool(remember))
            user.last_login = datetime.utcnow()
            db.session.commit()

            next_page = request.args.get('next')
            flash(f'Welcome back, {user.full_name or user.username}!', 'success')
            return redirect(next_page or url_for('dashboard.home'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.full_name       = request.form.get('full_name', '').strip()
        current_user.phone           = request.form.get('phone', '').strip()
        current_user.college         = request.form.get('college', '').strip()
        current_user.degree          = request.form.get('degree', '').strip()
        current_user.graduation_year = request.form.get('graduation_year', '').strip()
        current_user.interested_field = request.form.get('interested_field', '').strip()
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('auth.profile'))

    return render_template('profile.html')


@auth_bp.route('/toggle-theme')
@login_required
def toggle_theme():
    """Toggle dark/light mode"""
    current_user.theme = 'light' if current_user.theme == 'dark' else 'dark'
    db.session.commit()
    return redirect(request.referrer or url_for('dashboard.home'))
