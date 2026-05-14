"""
AI Chatbot Engine
Rule-based chatbot with optional Gemini/OpenAI API integration
"""
import os
import re

# ── Intent patterns ────────────────────────────────────────────────────────────
INTENTS = {
    'greeting': {
        'patterns': [r'\bhello\b', r'\bhi\b', r'\bhey\b', r'\bgreetings\b', r'\bgood\s+(morning|afternoon|evening)\b'],
        'responses': [
            "Hello! 👋 I'm your AI Career Assistant. How can I help you today?",
            "Hi there! Ready to boost your career? Ask me anything about resumes, skills, or career paths!",
            "Hey! Great to see you. What career question can I help you with?",
        ]
    },
    'resume': {
        'patterns': [r'\bresume\b', r'\bcv\b', r'\bats\b', r'\bapplicant tracking\b'],
        'responses': [
            "📄 For resume help, use **Resume Analyzer** or **Job-Based AI Resume Builder** (tailor to a real job description). Upload your PDF and we:\n"
            "• Calculate your ATS score\n• Identify missing skills\n• Suggest improvements\n\n"
            "A good ATS score is 70+. Want tips on improving yours?",
            "Your resume is your first impression! Key tips:\n"
            "1. Use keywords from the job description\n"
            "2. Quantify achievements (e.g., 'Improved performance by 30%')\n"
            "3. Keep it to 1-2 pages\n4. Use a clean, ATS-friendly format",
        ]
    },
    'skills': {
        'patterns': [r'\bskill\b', r'\blearn\b', r'\btech\b', r'\btechnology\b'],
        'responses': [
            "🛠️ Top in-demand skills for 2024:\n\n"
            "**Tech Skills:** Python, React, AWS, Docker, Machine Learning\n"
            "**Data Skills:** SQL, Pandas, Tableau, Power BI\n"
            "**Soft Skills:** Communication, Problem Solving, Leadership\n\n"
            "Which area interests you most?",
            "For skill recommendations, check the **Career Roadmap** page! "
            "I'll create a personalized learning path based on your current skills and goals.",
        ]
    },
    'interview': {
        'patterns': [r'\binterview\b', r'\bquestion\b', r'\bprepare\b', r'\bprep\b'],
        'responses': [
            "🎯 Interview prep tips:\n\n"
            "1. **Research the company** thoroughly\n"
            "2. **Practice STAR method** for behavioral questions\n"
            "3. **Review technical concepts** for your role\n"
            "4. **Prepare questions** to ask the interviewer\n\n"
            "Visit the **Interview Prep** page for 100+ practice questions!",
            "Common interview mistakes to avoid:\n"
            "❌ Not researching the company\n"
            "❌ Giving vague answers without examples\n"
            "❌ Not asking questions at the end\n"
            "❌ Arriving late or being unprepared\n\n"
            "Want specific questions for a role?",
        ]
    },
    'linkedin': {
        'patterns': [r'\blinkedin\b', r'\bprofile\b', r'\bnetwork\b', r'\bconnect\b'],
        'responses': [
            "💼 LinkedIn optimization tips:\n\n"
            "• **Headline:** Include your role + top 3 skills\n"
            "• **About:** Tell your story in 3-5 paragraphs\n"
            "• **Photo:** Professional headshot increases views by 14x\n"
            "• **Skills:** Add 5+ relevant skills\n\n"
            "Use the **LinkedIn Optimizer** page for AI-generated content!",
        ]
    },
    'career': {
        'patterns': [r'\bcareer\b', r'\bjob\b', r'\bpath\b', r'\broadmap\b', r'\bfield\b'],
        'responses': [
            "🚀 Popular career paths in tech:\n\n"
            "• **Web Development** – $70K-$120K/year\n"
            "• **Data Science** – $85K-$140K/year\n"
            "• **AI/ML Engineering** – $100K-$180K/year\n"
            "• **Cloud Computing** – $90K-$150K/year\n"
            "• **Cybersecurity** – $80K-$160K/year\n\n"
            "Visit **Career Roadmap** for a personalized learning path!",
        ]
    },
    'certification': {
        'patterns': [r'\bcertif\b', r'\bcourse\b', r'\bcoursera\b', r'\budemy\b', r'\baws\b'],
        'responses': [
            "🏆 Top certifications to boost your career:\n\n"
            "• **AWS Solutions Architect** – Cloud\n"
            "• **Google Data Analytics** – Data Science\n"
            "• **TensorFlow Developer** – AI/ML\n"
            "• **CompTIA Security+** – Cybersecurity\n"
            "• **Meta Front-End Developer** – Web Dev\n\n"
            "Check the **Certifications** page for personalized recommendations!",
        ]
    },
    'project': {
        'patterns': [r'\bproject\b', r'\bbuild\b', r'\bportfolio\b', r'\bpractice\b'],
        'responses': [
            "💡 Great project ideas for your portfolio:\n\n"
            "**Beginner:** Portfolio website, To-do app, Weather app\n"
            "**Intermediate:** Blog platform, Chat app, E-commerce store\n"
            "**Advanced:** SaaS app, AI chatbot, Real-time dashboard\n\n"
            "Visit **Project Suggestions** for personalized recommendations based on your skills!",
        ]
    },
    'salary': {
        'patterns': [r'\bsalary\b', r'\bpay\b', r'\bincome\b', r'\bearning\b', r'\bcompensation\b'],
        'responses': [
            "💰 Average tech salaries (US, 2024):\n\n"
            "• Software Engineer: $95K-$150K\n"
            "• Data Scientist: $85K-$140K\n"
            "• ML Engineer: $100K-$180K\n"
            "• Cloud Architect: $120K-$200K\n"
            "• Cybersecurity Analyst: $80K-$130K\n\n"
            "Salaries vary by location, experience, and company size.",
        ]
    },
    'help': {
        'patterns': [r'\bhelp\b', r'\bwhat can you\b', r'\bfeature\b', r'\bdo\b'],
        'responses': [
            "🤖 I can help you with:\n\n"
            "📄 **Resume Analysis** – ATS score & improvements\n"
            "🗺️ **Career Roadmap** – Personalized learning path\n"
            "🎯 **Interview Prep** – 100+ practice questions\n"
            "💼 **LinkedIn Optimizer** – Professional profile content\n"
            "💡 **Project Ideas** – Portfolio project suggestions\n"
            "🏆 **Certifications** – Top cert recommendations\n\n"
            "What would you like to explore?",
        ]
    },
}

FALLBACK_RESPONSES = [
    "That's a great question! For detailed guidance, try exploring the specific feature pages. "
    "I'm best at helping with resumes, career paths, interview prep, and LinkedIn optimization. "
    "What specific area can I help you with?",
    "I'm still learning! For the best results, try the dedicated tools:\n"
    "• Resume Analyzer for ATS scoring\n"
    "• Career Roadmap for learning paths\n"
    "• Interview Prep for practice questions",
    "Hmm, I'm not sure about that. Could you rephrase? I can help with career advice, "
    "resume tips, skill recommendations, and interview preparation.",
]


def _match_intent(message: str) -> str | None:
    """Find the best matching intent for a message"""
    message_lower = message.lower()
    for intent, data in INTENTS.items():
        for pattern in data['patterns']:
            if re.search(pattern, message_lower):
                return intent
    return None


def _get_ai_response(message: str, user) -> str | None:
    """Try to get a response from Gemini API"""
    api_key = os.getenv('GEMINI_API_KEY', '')
    if not api_key or api_key == 'your-gemini-api-key-here':
        return None

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')

        system_context = (
            f"You are an AI Career Assistant for students. The user is {user.full_name or user.username}. "
            f"Their interested field is {user.interested_field or 'technology'}. "
            "Keep responses concise, helpful, and career-focused. Use emojis sparingly."
        )

        response = model.generate_content(f"{system_context}\n\nUser: {message}")
        return response.text
    except Exception:
        return None


def get_chatbot_response(message: str, user) -> str:
    """
    Main chatbot response function.
    Tries AI API first, falls back to rule-based responses.
    """
    import random

    # Try AI API
    ai_response = _get_ai_response(message, user)
    if ai_response:
        return ai_response

    # Rule-based fallback
    intent = _match_intent(message)
    if intent:
        responses = INTENTS[intent]['responses']
        return random.choice(responses)

    return random.choice(FALLBACK_RESPONSES)
