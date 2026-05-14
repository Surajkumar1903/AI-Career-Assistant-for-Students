"""
Admin panel routes
"""
import json
from collections import defaultdict
from datetime import datetime, timedelta

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from functools import wraps

from models.database import db
from models.user import User, Resume, ResumeAnalysis, ContactMessage

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    """Decorator to restrict access to admin users only"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required.', 'danger')
            return redirect(url_for('dashboard.home'))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/')
@login_required
@admin_required
def panel():
    """Admin dashboard"""
    total_users    = User.query.count()
    total_resumes  = Resume.query.count()
    total_analyses = ResumeAnalysis.query.count()
    total_messages = ContactMessage.query.count()
    unread_messages = ContactMessage.query.filter_by(is_read=False).count()

    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()

    return render_template(
        'admin/panel.html',
        total_users=total_users,
        total_resumes=total_resumes,
        total_analyses=total_analyses,
        total_messages=total_messages,
        unread_messages=unread_messages,
        recent_users=recent_users
    )


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """List all users"""
    search = request.args.get('search', '')
    query  = User.query
    if search:
        query = query.filter(
            (User.username.ilike(f'%{search}%')) |
            (User.email.ilike(f'%{search}%')) |
            (User.full_name.ilike(f'%{search}%'))
        )
    all_users = query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=all_users, search=search)


@admin_bp.route('/users/<int:user_id>/toggle')
@login_required
@admin_required
def toggle_user(user_id):
    """Activate / deactivate a user"""
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("You can't deactivate yourself.", 'warning')
    else:
        user.is_active = not user.is_active
        db.session.commit()
        status = 'activated' if user.is_active else 'deactivated'
        flash(f'User {user.username} has been {status}.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/resumes')
@login_required
@admin_required
def resumes():
    """View all uploaded resumes"""
    all_resumes = Resume.query.order_by(Resume.uploaded_at.desc()).all()
    return render_template('admin/resumes.html', resumes=all_resumes)


@admin_bp.route('/messages')
@login_required
@admin_required
def messages():
    """View contact messages"""
    msgs = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    # Mark all as read
    ContactMessage.query.filter_by(is_read=False).update({'is_read': True})
    db.session.commit()
    return render_template('admin/messages.html', messages=msgs)


@admin_bp.route('/analytics')
@login_required
@admin_required
def analytics():
    """Admin analytics page"""
    from sqlalchemy import func
    # Average ATS score
    avg_score = db.session.query(func.avg(ResumeAnalysis.ats_score)).scalar() or 0
    # Resume ranking leaderboard
    leaderboard = ResumeAnalysis.query.order_by(ResumeAnalysis.ats_score.desc()).limit(25).all()

    # Analyses per day (last 14 days) for a simple bar chart
    today = datetime.utcnow().date()
    start_day = today - timedelta(days=13)
    recent = (
        ResumeAnalysis.query.filter(ResumeAnalysis.analyzed_at >= datetime.combine(start_day, datetime.min.time()))
        .order_by(ResumeAnalysis.analyzed_at.asc())
        .all()
    )
    counts: defaultdict[str, int] = defaultdict(int)
    for a in recent:
        counts[a.analyzed_at.date().isoformat()] += 1
    labels = []
    vals = []
    for i in range(14):
        d = start_day + timedelta(days=i)
        labels.append(d.strftime('%m-%d'))
        vals.append(counts.get(d.isoformat(), 0))

    return render_template(
        'admin/analytics.html',
        avg_score=round(avg_score, 1),
        leaderboard=leaderboard,
        chart_labels=json.dumps(labels),
        chart_values=json.dumps(vals),
    )


@admin_bp.route('/recommendations')
@login_required
@admin_required
def recommendations():
    """Where admins learn how recommendation content is managed (code-first)."""
    return render_template('admin/recommendations.html')


@admin_bp.route('/api/stats')
@login_required
@admin_required
def api_stats():
    return jsonify({
        'users': User.query.count(),
        'resumes': Resume.query.count(),
        'analyses': ResumeAnalysis.query.count(),
    })
