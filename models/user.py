"""
User model - handles authentication and profile data
"""
from flask_login import UserMixin
from datetime import datetime
from models.database import db


class User(UserMixin, db.Model):
    """User account model"""
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80), unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password      = db.Column(db.String(256), nullable=False)
    full_name     = db.Column(db.String(150), default='')
    phone         = db.Column(db.String(20), default='')
    college       = db.Column(db.String(200), default='')
    degree        = db.Column(db.String(100), default='')
    graduation_year = db.Column(db.String(10), default='')
    interested_field = db.Column(db.String(100), default='')
    profile_pic   = db.Column(db.String(200), default='default.png')
    is_admin      = db.Column(db.Boolean, default=False)
    is_active     = db.Column(db.Boolean, default=True)
    theme         = db.Column(db.String(10), default='dark')
    language      = db.Column(db.String(10), default='en')
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    last_login    = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    resumes       = db.relationship('Resume', backref='owner', lazy=True, cascade='all, delete-orphan')
    analyses      = db.relationship('ResumeAnalysis', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'college': self.college,
            'degree': self.degree,
            'interested_field': self.interested_field,
            'is_admin': self.is_admin,
            'created_at': self.created_at.strftime('%Y-%m-%d'),
        }


class Resume(db.Model):
    """Uploaded resume files"""
    __tablename__ = 'resumes'

    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename    = db.Column(db.String(200), nullable=False)
    original_name = db.Column(db.String(200), nullable=False)
    file_size   = db.Column(db.Integer, default=0)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active   = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Resume {self.original_name}>'


class ResumeAnalysis(db.Model):
    """Stores resume analysis results"""
    __tablename__ = 'resume_analyses'

    id              = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    resume_id       = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=True)
    ats_score       = db.Column(db.Float, default=0.0)
    skills_found    = db.Column(db.Text, default='[]')       # JSON list
    skills_missing  = db.Column(db.Text, default='[]')       # JSON list
    education       = db.Column(db.Text, default='')
    experience      = db.Column(db.Text, default='')
    certifications  = db.Column(db.Text, default='[]')       # JSON list
    suggestions     = db.Column(db.Text, default='[]')       # JSON list
    raw_text        = db.Column(db.Text, default='')
    career_field    = db.Column(db.String(100), default='')
    analyzed_at     = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Analysis user={self.user_id} score={self.ats_score}>'


class ContactMessage(db.Model):
    """Contact form submissions"""
    __tablename__ = 'contact_messages'

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False)
    email      = db.Column(db.String(120), nullable=False)
    subject    = db.Column(db.String(200), nullable=False)
    message    = db.Column(db.Text, nullable=False)
    is_read    = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Contact {self.email}>'
