"""
PDF Report Generator
Creates downloadable PDF analysis reports using ReportLab
"""
import os
import json
from datetime import datetime


def generate_pdf_report(analysis, user) -> str:
    """
    Generate a PDF report for a resume analysis.

    Args:
        analysis: ResumeAnalysis model instance
        user: User model instance

    Returns:
        str: absolute path to the generated PDF file
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
        from reportlab.lib.enums import TA_CENTER, TA_LEFT

        # ── Output path ────────────────────────────────────────────────────────
        reports_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        filename    = f"report_{user.id}_{analysis.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        output_path = os.path.join(reports_dir, filename)

        # ── Document setup ─────────────────────────────────────────────────────
        doc    = SimpleDocTemplate(output_path, pagesize=A4,
                                   rightMargin=2*cm, leftMargin=2*cm,
                                   topMargin=2*cm, bottomMargin=2*cm)
        styles = getSampleStyleSheet()
        story  = []

        # Custom styles
        title_style = ParagraphStyle('Title', parent=styles['Title'],
                                     fontSize=22, textColor=colors.HexColor('#6366f1'),
                                     spaceAfter=6, alignment=TA_CENTER)
        h2_style    = ParagraphStyle('H2', parent=styles['Heading2'],
                                     fontSize=14, textColor=colors.HexColor('#4f46e5'),
                                     spaceBefore=12, spaceAfter=4)
        body_style  = ParagraphStyle('Body', parent=styles['Normal'],
                                     fontSize=10, spaceAfter=4)

        # ── Header ─────────────────────────────────────────────────────────────
        story.append(Paragraph("AI Career Assistant", title_style))
        story.append(Paragraph("Resume Analysis Report", styles['Heading2']))
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#6366f1')))
        story.append(Spacer(1, 0.3*cm))

        # ── User info ──────────────────────────────────────────────────────────
        story.append(Paragraph("Candidate Information", h2_style))
        info_data = [
            ['Name:', user.full_name or user.username],
            ['Email:', user.email],
            ['College:', user.college or 'N/A'],
            ['Target Field:', analysis.career_field or 'General'],
            ['Report Date:', datetime.now().strftime('%B %d, %Y')],
        ]
        info_table = Table(info_data, colWidths=[4*cm, 12*cm])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#4f46e5')),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 0.5*cm))

        # ── ATS Score ──────────────────────────────────────────────────────────
        story.append(Paragraph("ATS Score", h2_style))
        score = analysis.ats_score
        score_color = (colors.HexColor('#22c55e') if score >= 70
                       else colors.HexColor('#f59e0b') if score >= 50
                       else colors.HexColor('#ef4444'))
        score_data = [[f"Your ATS Score: {score:.1f} / 100"]]
        score_table = Table(score_data, colWidths=[16*cm])
        score_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 16),
            ('TEXTCOLOR', (0, 0), (-1, -1), score_color),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 1, score_color),
            ('PADDING', (0, 0), (-1, -1), 12),
            ('ROUNDEDCORNERS', [5]),
        ]))
        story.append(score_table)
        story.append(Spacer(1, 0.3*cm))

        # ── Skills Found ───────────────────────────────────────────────────────
        skills_found = json.loads(analysis.skills_found)
        if skills_found:
            story.append(Paragraph(f"Skills Found ({len(skills_found)})", h2_style))
            skills_text = ' • '.join(skills_found)
            story.append(Paragraph(skills_text, body_style))
            story.append(Spacer(1, 0.3*cm))

        # ── Missing Skills ─────────────────────────────────────────────────────
        skills_missing = json.loads(analysis.skills_missing)
        if skills_missing:
            story.append(Paragraph(f"Missing Skills ({len(skills_missing)})", h2_style))
            missing_text = ' • '.join(skills_missing)
            story.append(Paragraph(missing_text, body_style))
            story.append(Spacer(1, 0.3*cm))

        # ── Suggestions ────────────────────────────────────────────────────────
        suggestions = json.loads(analysis.suggestions)
        if suggestions:
            story.append(Paragraph("Improvement Suggestions", h2_style))
            for i, suggestion in enumerate(suggestions, 1):
                story.append(Paragraph(f"{i}. {suggestion}", body_style))
            story.append(Spacer(1, 0.3*cm))

        # ── Footer ─────────────────────────────────────────────────────────────
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#e2e8f0')))
        story.append(Spacer(1, 0.2*cm))
        story.append(Paragraph(
            "Generated by AI Career Assistant for Students | aicareer.app",
            ParagraphStyle('Footer', parent=styles['Normal'],
                           fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
        ))

        doc.build(story)
        return output_path

    except ImportError:
        # ReportLab not installed – create a simple text file instead
        reports_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        filename    = f"report_{user.id}_{analysis.id}.txt"
        output_path = os.path.join(reports_dir, filename)

        with open(output_path, 'w') as f:
            f.write(f"AI Career Assistant - Resume Analysis Report\n")
            f.write(f"{'='*50}\n")
            f.write(f"Name: {user.full_name or user.username}\n")
            f.write(f"ATS Score: {analysis.ats_score:.1f}/100\n")
            f.write(f"Target Field: {analysis.career_field}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d')}\n")

        return output_path
