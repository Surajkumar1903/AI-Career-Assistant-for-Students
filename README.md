# AI Career Assistant for Students

An AI-powered web application that helps students navigate their career journey — from resume analysis and job-based resume building to interview prep, skill tracking, and LinkedIn optimization.

## Features

- **Resume Analyzer** — ATS scoring, keyword matching, and improvement suggestions
- **Job-Based Resume Builder** — AI-generated resumes tailored to specific job descriptions
- **Career Roadmap** — Personalized career path recommendations
- **Interview Prep** — Practice questions and feedback
- **Skills Tracker** — Track and visualize your skill progress
- **Certifications** — Recommended certifications based on your goals
- **LinkedIn Optimizer** — Tips to improve your LinkedIn profile
- **AI Chatbot** — Career guidance chatbot powered by Gemini / OpenAI
- **Projects Showcase** — Manage and display your projects
- **Admin Panel** — User management, analytics, and messaging

## Tech Stack

- **Backend:** Python, Flask, SQLAlchemy, Flask-Login
- **AI:** Google Gemini API, OpenAI API
- **NLP:** spaCy, NLTK, scikit-learn
- **PDF/DOCX:** pdfplumber, PyPDF2, python-docx, reportlab
- **Frontend:** HTML, CSS, JavaScript (Jinja2 templates)
- **Database:** SQLite (dev) — easily swappable to PostgreSQL

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/ai-career-assistant.git
cd ai-career-assistant

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Set up environment variables
copy .env.example .env
# Edit .env and add your API keys

# Run the app
python app.py
```

The app will be available at `http://localhost:5000`.

## Environment Variables

Copy `.env.example` to `.env` and fill in your values:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Flask secret key (use a long random string) |
| `GEMINI_API_KEY` | Google Gemini API key |
| `OPENAI_API_KEY` | OpenAI API key (optional) |
| `DATABASE_URL` | Database URL (default: SQLite) |
| `MAIL_SERVER` | SMTP server for contact emails |
| `MAIL_USERNAME` | Email address for sending notifications |
| `MAIL_PASSWORD` | Email app password |

## License

MIT
