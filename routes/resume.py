"""
Resume upload and analysis routes
"""
import os
import re
import json
import uuid
import secrets
from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    jsonify,
    current_app,
    send_from_directory,
    session,
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from models.database import db
from models.user import Resume, ResumeAnalysis
from utils.resume_parser import parse_resume
from utils.ats_scorer import calculate_ats_score
from utils.pdf_report import generate_pdf_report
from utils.job_resume_ai import generate_tailored_resume_bundle
from utils.job_resume_export import build_job_resume_pdf, build_job_resume_docx
from utils.job_resume_match import compute_job_match, compute_match_on_generated_text
from utils.pdf_style_extract import extract_style_profile, merge_with_default_reference

resume_bp = Blueprint('resume', __name__)

JOB_RESUME_ROLES = [
    {'value': 'Python Developer', 'label': 'Python Developer'},
    {'value': 'AI/ML Intern', 'label': 'AI/ML Intern'},
    {'value': 'Web Developer', 'label': 'Web Developer'},
    {'value': 'Data Analyst', 'label': 'Data Analyst'},
    {'value': 'Full Stack Developer', 'label': 'Full Stack Developer'},
]

JOB_RESUME_BUILD_SUBDIR = 'job_resume_builds'
AUTO_RESUME_BUILD_SUBDIR = 'auto_resume_builds'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def _builder_bundle_path(token: str, subdir: str) -> str:
    base = os.path.join(current_app.config['UPLOAD_FOLDER'], subdir)
    return os.path.join(base, f'{token}.json')


def _save_builder_bundle(user_id: int, bundle: dict, subdir: str) -> str:
    token = secrets.token_hex(16)
    base = os.path.join(current_app.config['UPLOAD_FOLDER'], subdir)
    os.makedirs(base, exist_ok=True)
    path = os.path.join(base, f'{token}.json')
    out = {
        'user_id': user_id,
        'sections': bundle['sections'],
        'match': bundle['match'],
        'job_role': bundle['job_role'],
        'jd_skill_lexicon': bundle.get('jd_skill_lexicon', []),
        'used_ai': bundle.get('used_ai', False),
        'job_description_snippet': bundle.get('job_description_snippet', ''),
        'resume_contact': bundle.get('resume_contact') or {},
        'resume_raw_excerpt': bundle.get('resume_raw_excerpt') or '',
    }
    for k in ('style_profile', 'ats_before', 'ats_after', 'generator'):
        if k in bundle:
            out[k] = bundle[k]
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, default=str)
    return token


def _load_builder_bundle(token: str, user_id: int, subdir: str) -> dict | None:
    if not token:
        return None
    path = _builder_bundle_path(token, subdir)
    if not os.path.isfile(path):
        return None
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    if int(data.get('user_id', -1)) != int(user_id):
        return None
    return data


def _save_job_resume_bundle(user_id: int, bundle: dict) -> str:
    return _save_builder_bundle(user_id, bundle, JOB_RESUME_BUILD_SUBDIR)


def _load_job_resume_bundle(token: str, user_id: int) -> dict | None:
    return _load_builder_bundle(token, user_id, JOB_RESUME_BUILD_SUBDIR)


def _reference_resume_format_pdf_path() -> str:
    """Optional packaged reference PDF for typography fallback."""
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    return os.path.join(root, 'static', 'reference', 'resume_format_reference.pdf')


def _slug_role(name: str) -> str:
    s = re.sub(r'[^\w\s-]', '', name or 'role').strip().replace(' ', '_')
    return (s or 'role')[:48]


@resume_bp.route('/resume-analyzer', methods=['GET', 'POST'])
@login_required
def analyzer():
    """Resume upload and analysis page"""
    if request.method == 'POST':
        if 'resume' not in request.files:
            flash('No file selected.', 'danger')
            return redirect(request.url)

        file = request.files['resume']
        if file.filename == '':
            flash('No file selected.', 'danger')
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash('Only PDF, DOC, and DOCX files are allowed.', 'danger')
            return redirect(request.url)

        # ── Save file ─────────────────────────────────────────────────────────
        original_name = secure_filename(file.filename)
        unique_name   = f"{uuid.uuid4().hex}_{original_name}"
        save_path     = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name)
        file.save(save_path)
        file_size = os.path.getsize(save_path)

        # ── Store resume record ───────────────────────────────────────────────
        resume_record = Resume(
            user_id=current_user.id,
            filename=unique_name,
            original_name=original_name,
            file_size=file_size
        )
        db.session.add(resume_record)
        db.session.commit()

        # ── Parse & analyse ───────────────────────────────────────────────────
        target_field = request.form.get('target_field', 'general')
        parsed       = parse_resume(save_path)
        analysis     = calculate_ats_score(parsed, target_field)

        # ── Persist analysis ──────────────────────────────────────────────────
        record = ResumeAnalysis(
            user_id=current_user.id,
            resume_id=resume_record.id,
            ats_score=analysis['ats_score'],
            skills_found=json.dumps(analysis['skills_found']),
            skills_missing=json.dumps(analysis['skills_missing']),
            education=parsed.get('education', ''),
            experience=parsed.get('experience', ''),
            certifications=json.dumps(parsed.get('certifications', [])),
            suggestions=json.dumps(analysis['suggestions']),
            raw_text=parsed.get('raw_text', '')[:5000],
            career_field=target_field
        )
        db.session.add(record)
        db.session.commit()

        flash('Resume analysed successfully!', 'success')
        return redirect(url_for('resume.result', analysis_id=record.id))

    # GET – show upload form with history
    history = ResumeAnalysis.query.filter_by(user_id=current_user.id)\
                                  .order_by(ResumeAnalysis.analyzed_at.desc())\
                                  .limit(5).all()
    return render_template('analyzer.html', history=history)


@resume_bp.route('/resume-result/<int:analysis_id>')
@login_required
def result(analysis_id):
    """Show detailed analysis result"""
    analysis = ResumeAnalysis.query.filter_by(
        id=analysis_id, user_id=current_user.id
    ).first_or_404()

    skills_found   = json.loads(analysis.skills_found)
    skills_missing = json.loads(analysis.skills_missing)
    certifications = json.loads(analysis.certifications)
    suggestions    = json.loads(analysis.suggestions)

    return render_template(
        'result.html',
        analysis=analysis,
        skills_found=skills_found,
        skills_missing=skills_missing,
        certifications=certifications,
        suggestions=suggestions
    )


@resume_bp.route('/download-report/<int:analysis_id>')
@login_required
def download_report(analysis_id):
    """Generate and download PDF report"""
    analysis = ResumeAnalysis.query.filter_by(
        id=analysis_id, user_id=current_user.id
    ).first_or_404()

    report_path = generate_pdf_report(analysis, current_user)
    report_dir  = os.path.dirname(report_path)
    report_file = os.path.basename(report_path)

    return send_from_directory(report_dir, report_file, as_attachment=True)


@resume_bp.route('/api/analysis/<int:analysis_id>')
@login_required
def api_analysis(analysis_id):
    """JSON endpoint for analysis data (used by charts)"""
    analysis = ResumeAnalysis.query.filter_by(
        id=analysis_id, user_id=current_user.id
    ).first_or_404()

    return jsonify({
        'ats_score': analysis.ats_score,
        'skills_found': json.loads(analysis.skills_found),
        'skills_missing': json.loads(analysis.skills_missing),
        'suggestions': json.loads(analysis.suggestions),
        'career_field': analysis.career_field
    })


@resume_bp.route('/job-resume-builder', methods=['GET', 'POST'])
@login_required
def job_resume_builder():
    """Job-based tailored resume: JD + upload → match analysis + sections + downloads."""
    bundle = None
    token = session.get('job_resume_token')
    if token:
        bundle = _load_job_resume_bundle(token, current_user.id)
        if not bundle:
            session.pop('job_resume_token', None)

    if request.method == 'POST':
        job_role = (request.form.get('job_role') or '').strip()
        jd_text = (request.form.get('job_description') or '').strip()

        allowed = {r['value'] for r in JOB_RESUME_ROLES}
        if job_role not in allowed:
            flash('Please select a valid job role.', 'danger')
            return redirect(url_for('resume.job_resume_builder'))

        if len(jd_text) < 40:
            flash('Please paste a fuller job description (at least a few lines).', 'warning')
            return redirect(url_for('resume.job_resume_builder'))

        if 'resume' not in request.files:
            flash('No resume file selected.', 'danger')
            return redirect(url_for('resume.job_resume_builder'))

        file = request.files['resume']
        if not file.filename:
            flash('No resume file selected.', 'danger')
            return redirect(url_for('resume.job_resume_builder'))

        if not allowed_file(file.filename):
            flash('Only PDF, DOC, and DOCX files are allowed.', 'danger')
            return redirect(url_for('resume.job_resume_builder'))

        original_name = secure_filename(file.filename)
        unique_name = f"{uuid.uuid4().hex}_{original_name}"
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name)
        file.save(save_path)
        try:
            parsed = parse_resume(save_path)
            if not (parsed.get('raw_text') or '').strip():
                flash('Could not read text from that file. Try another PDF/DOCX.', 'danger')
                return redirect(url_for('resume.job_resume_builder'))

            gen_bundle = generate_tailored_resume_bundle(parsed, jd_text, job_role, current_user)
            gen_bundle['job_description_snippet'] = jd_text[:8000]
            gen_bundle['resume_contact'] = parsed.get('contact') or {}
            gen_bundle['resume_raw_excerpt'] = (parsed.get('raw_text') or '')[:6000]
            new_token = _save_job_resume_bundle(current_user.id, gen_bundle)
            session['job_resume_token'] = new_token

            if gen_bundle.get('used_ai'):
                flash('Tailored resume generated with AI (your facts only). Review before sending to employers.', 'success')
            else:
                flash('Tailored resume generated locally (set GEMINI_API_KEY for richer AI wording). Review before sending.', 'info')
        except Exception:
            current_app.logger.exception('job_resume_builder')
            flash('Could not process that resume. Try a different file or a shorter job description.', 'danger')
            return redirect(url_for('resume.job_resume_builder'))
        finally:
            try:
                os.remove(save_path)
            except OSError:
                pass

        return redirect(url_for('resume.job_resume_builder'))

    return render_template(
        'job_resume_builder.html',
        job_roles=JOB_RESUME_ROLES,
        bundle=bundle,
    )


@resume_bp.route('/job-resume-builder/download/pdf')
@login_required
def job_resume_download_pdf():
    token = session.get('job_resume_token')
    data = _load_job_resume_bundle(token, current_user.id) if token else None
    if not data:
        flash('Generate a resume first.', 'warning')
        return redirect(url_for('resume.job_resume_builder'))

    reports_dir = os.path.join(current_app.root_path, 'static', 'reports')
    os.makedirs(reports_dir, exist_ok=True)

    slug = _slug_role(data.get('job_role', 'resume'))
    fn = f"job_resume_{current_user.id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.pdf"
    out_path = os.path.join(reports_dir, fn)
    build_job_resume_pdf(data, current_user, out_path)
    return send_from_directory(reports_dir, fn, as_attachment=True, download_name=f'Tailored_Resume_{slug}.pdf')


@resume_bp.route('/job-resume-builder/download/docx')
@login_required
def job_resume_download_docx():
    token = session.get('job_resume_token')
    data = _load_job_resume_bundle(token, current_user.id) if token else None
    if not data:
        flash('Generate a resume first.', 'warning')
        return redirect(url_for('resume.job_resume_builder'))

    reports_dir = os.path.join(current_app.root_path, 'static', 'reports')
    os.makedirs(reports_dir, exist_ok=True)

    slug = _slug_role(data.get('job_role', 'resume'))
    fn = f"job_resume_{current_user.id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.docx"
    out_path = os.path.join(reports_dir, fn)
    build_job_resume_docx(data, current_user, out_path)
    return send_from_directory(reports_dir, fn, as_attachment=True, download_name=f'Tailored_Resume_{slug}.docx')


@resume_bp.route('/auto-resume-pdf-format', methods=['GET', 'POST'])
@login_required
def auto_resume_pdf_format():
    """
    Auto Resume Generator: clone typography from uploaded PDF, optimize content to JD,
    ATS before/after, PDF + DOCX download.
    """
    bundle = None
    token = session.get('auto_resume_token')
    if token:
        bundle = _load_builder_bundle(token, current_user.id, AUTO_RESUME_BUILD_SUBDIR)
        if not bundle:
            session.pop('auto_resume_token', None)

    if request.method == 'POST':
        job_role = (request.form.get('job_role') or '').strip()
        jd_text = (request.form.get('job_description') or '').strip()
        allowed = {r['value'] for r in JOB_RESUME_ROLES}
        if job_role not in allowed:
            flash('Please select a valid job role.', 'danger')
            return redirect(url_for('resume.auto_resume_pdf_format'))
        if len(jd_text) < 40:
            flash('Please paste a fuller job description.', 'warning')
            return redirect(url_for('resume.auto_resume_pdf_format'))
        if 'resume' not in request.files:
            flash('No resume file selected.', 'danger')
            return redirect(url_for('resume.auto_resume_pdf_format'))
        file = request.files['resume']
        if not file.filename:
            flash('No resume file selected.', 'danger')
            return redirect(url_for('resume.auto_resume_pdf_format'))
        if not allowed_file(file.filename):
            flash('Only PDF, DOC, or DOCX files are allowed.', 'danger')
            return redirect(url_for('resume.auto_resume_pdf_format'))
        if not file.filename.lower().endswith('.pdf'):
            flash('This tool requires a PDF so we can read layout and fonts. Use Job Resume Builder for DOCX.', 'warning')
            return redirect(url_for('resume.auto_resume_pdf_format'))

        original_name = secure_filename(file.filename)
        unique_name = f"{uuid.uuid4().hex}_{original_name}"
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name)
        file.save(save_path)
        try:
            parsed = parse_resume(save_path)
            if not (parsed.get('raw_text') or '').strip():
                flash('Could not read text from that PDF.', 'danger')
                return redirect(url_for('resume.auto_resume_pdf_format'))

            m_before = compute_job_match(parsed, jd_text)
            ats_before = int(m_before.get('ats_match_score', 0))

            style_profile = extract_style_profile(save_path)
            ref_path = _reference_resume_format_pdf_path()
            style_profile = merge_with_default_reference(
                style_profile, ref_path if os.path.isfile(ref_path) else None
            )

            gen_bundle = generate_tailored_resume_bundle(
                parsed, jd_text, job_role, current_user, style_profile=style_profile
            )
            gen_bundle['job_description_snippet'] = jd_text[:8000]
            gen_bundle['resume_contact'] = parsed.get('contact') or {}
            gen_bundle['resume_raw_excerpt'] = (parsed.get('raw_text') or '')[:6000]
            gen_bundle['generator'] = 'auto_pdf_format'
            gen_bundle['style_profile'] = style_profile
            gen_bundle['ats_before'] = ats_before
            gen_bundle['match'] = m_before
            m_after = compute_match_on_generated_text(parsed, gen_bundle['sections'], jd_text)
            gen_bundle['ats_after'] = int(m_after.get('ats_match_score', 0))

            new_token = _save_builder_bundle(current_user.id, gen_bundle, AUTO_RESUME_BUILD_SUBDIR)
            session['auto_resume_token'] = new_token

            if gen_bundle.get('used_ai'):
                flash('Optimized CV generated (same style family as your PDF). Review before sending.', 'success')
            else:
                flash('CV generated locally. Add GEMINI_API_KEY for stronger job-specific wording.', 'info')
        except Exception:
            current_app.logger.exception('auto_resume_pdf_format')
            flash('Could not process that PDF.', 'danger')
            return redirect(url_for('resume.auto_resume_pdf_format'))
        finally:
            try:
                os.remove(save_path)
            except OSError:
                pass

        return redirect(url_for('resume.auto_resume_pdf_format'))

    return render_template(
        'auto_resume_generator.html',
        job_roles=JOB_RESUME_ROLES,
        bundle=bundle,
    )


@resume_bp.route('/auto-resume-pdf-format/download/pdf')
@login_required
def auto_resume_download_pdf():
    token = session.get('auto_resume_token')
    data = _load_builder_bundle(token, current_user.id, AUTO_RESUME_BUILD_SUBDIR) if token else None
    if not data:
        flash('Generate a resume first.', 'warning')
        return redirect(url_for('resume.auto_resume_pdf_format'))

    reports_dir = os.path.join(current_app.root_path, 'static', 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    slug = _slug_role(data.get('job_role', 'resume'))
    fn = f"auto_resume_{current_user.id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.pdf"
    out_path = os.path.join(reports_dir, fn)
    build_job_resume_pdf(data, current_user, out_path)
    return send_from_directory(reports_dir, fn, as_attachment=True, download_name=f'Auto_Resume_{slug}.pdf')


@resume_bp.route('/auto-resume-pdf-format/download/docx')
@login_required
def auto_resume_download_docx():
    token = session.get('auto_resume_token')
    data = _load_builder_bundle(token, current_user.id, AUTO_RESUME_BUILD_SUBDIR) if token else None
    if not data:
        flash('Generate a resume first.', 'warning')
        return redirect(url_for('resume.auto_resume_pdf_format'))

    reports_dir = os.path.join(current_app.root_path, 'static', 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    slug = _slug_role(data.get('job_role', 'resume'))
    fn = f"auto_resume_{current_user.id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.docx"
    out_path = os.path.join(reports_dir, fn)
    build_job_resume_docx(data, current_user, out_path)
    return send_from_directory(reports_dir, fn, as_attachment=True, download_name=f'Auto_Resume_{slug}.docx')
