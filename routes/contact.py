"""
Contact page routes
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for

from models.database import db
from models.user import ContactMessage

contact_bp = Blueprint('contact', __name__)


@contact_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name    = request.form.get('name', '').strip()
        email   = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

        if not all([name, email, subject, message]):
            flash('All fields are required.', 'danger')
            return render_template('contact.html')

        msg = ContactMessage(name=name, email=email, subject=subject, message=message)
        db.session.add(msg)
        db.session.commit()

        flash('Message sent! We will get back to you soon.', 'success')
        return redirect(url_for('contact.contact'))

    return render_template('contact.html')
