"""
Project Recommendation Engine
Suggests beginner/intermediate/advanced projects based on user skills
"""

PROJECT_DOMAINS = [
    'Web Development', 'Data Science', 'AI/ML', 'Mobile Development',
    'Cloud/DevOps', 'Cybersecurity', 'Game Development', 'Automation'
]

PROJECTS_DB = {
    'Web Development': {
        'beginner': [
            {
                'title': 'Personal Portfolio Website',
                'description': 'Build a responsive portfolio showcasing your skills, projects, and contact info.',
                'technologies': ['HTML', 'CSS', 'JavaScript', 'Bootstrap'],
                'duration': '1-2 weeks',
                'difficulty': '⭐',
                'github_topics': ['portfolio', 'html-css', 'responsive-design'],
            },
            {
                'title': 'To-Do List App',
                'description': 'A task management app with add, edit, delete, and filter functionality.',
                'technologies': ['HTML', 'CSS', 'JavaScript', 'LocalStorage'],
                'duration': '3-5 days',
                'difficulty': '⭐',
                'github_topics': ['todo-app', 'javascript', 'localstorage'],
            },
            {
                'title': 'Weather App',
                'description': 'Fetch and display real-time weather data using a public API.',
                'technologies': ['HTML', 'CSS', 'JavaScript', 'OpenWeather API'],
                'duration': '1 week',
                'difficulty': '⭐⭐',
                'github_topics': ['weather-app', 'api', 'javascript'],
            },
        ],
        'intermediate': [
            {
                'title': 'Blog Platform',
                'description': 'Full-stack blog with user auth, CRUD posts, comments, and categories.',
                'technologies': ['React', 'Node.js', 'Express', 'MongoDB', 'JWT'],
                'duration': '3-4 weeks',
                'difficulty': '⭐⭐⭐',
                'github_topics': ['blog', 'react', 'nodejs', 'mongodb'],
            },
            {
                'title': 'E-commerce Store',
                'description': 'Online shop with product listings, cart, checkout, and payment integration.',
                'technologies': ['React', 'Node.js', 'PostgreSQL', 'Stripe API'],
                'duration': '4-6 weeks',
                'difficulty': '⭐⭐⭐',
                'github_topics': ['ecommerce', 'react', 'stripe'],
            },
            {
                'title': 'Real-time Chat App',
                'description': 'Chat application with rooms, private messages, and online status.',
                'technologies': ['React', 'Node.js', 'Socket.io', 'MongoDB'],
                'duration': '2-3 weeks',
                'difficulty': '⭐⭐⭐',
                'github_topics': ['chat-app', 'socketio', 'realtime'],
            },
        ],
        'advanced': [
            {
                'title': 'SaaS Project Management Tool',
                'description': 'Trello-like app with boards, drag-and-drop, team collaboration, and analytics.',
                'technologies': ['Next.js', 'TypeScript', 'PostgreSQL', 'Redis', 'Docker'],
                'duration': '8-12 weeks',
                'difficulty': '⭐⭐⭐⭐⭐',
                'github_topics': ['saas', 'nextjs', 'typescript', 'project-management'],
            },
            {
                'title': 'Video Streaming Platform',
                'description': 'YouTube-like platform with upload, streaming, recommendations, and subscriptions.',
                'technologies': ['React', 'Node.js', 'AWS S3', 'FFmpeg', 'Redis'],
                'duration': '10-14 weeks',
                'difficulty': '⭐⭐⭐⭐⭐',
                'github_topics': ['video-streaming', 'aws', 'ffmpeg'],
            },
        ],
    },
    'Data Science': {
        'beginner': [
            {
                'title': 'Titanic Survival Prediction',
                'description': 'Classic ML project predicting passenger survival using classification algorithms.',
                'technologies': ['Python', 'Pandas', 'Scikit-learn', 'Matplotlib'],
                'duration': '1 week',
                'difficulty': '⭐⭐',
                'github_topics': ['titanic', 'machine-learning', 'classification'],
            },
            {
                'title': 'COVID-19 Data Dashboard',
                'description': 'Interactive dashboard visualizing COVID-19 statistics by country.',
                'technologies': ['Python', 'Pandas', 'Plotly', 'Dash'],
                'duration': '1-2 weeks',
                'difficulty': '⭐⭐',
                'github_topics': ['covid19', 'data-visualization', 'dashboard'],
            },
            {
                'title': 'Sales Data Analysis',
                'description': 'Analyse retail sales data to find trends, top products, and seasonal patterns.',
                'technologies': ['Python', 'Pandas', 'Matplotlib', 'Seaborn'],
                'duration': '1 week',
                'difficulty': '⭐',
                'github_topics': ['data-analysis', 'pandas', 'visualization'],
            },
        ],
        'intermediate': [
            {
                'title': 'House Price Prediction',
                'description': 'Predict house prices using regression with feature engineering and model tuning.',
                'technologies': ['Python', 'Scikit-learn', 'XGBoost', 'Pandas', 'Seaborn'],
                'duration': '2-3 weeks',
                'difficulty': '⭐⭐⭐',
                'github_topics': ['regression', 'house-prices', 'xgboost'],
            },
            {
                'title': 'Customer Churn Prediction',
                'description': 'Predict which customers are likely to leave using classification models.',
                'technologies': ['Python', 'Scikit-learn', 'SHAP', 'Pandas'],
                'duration': '2-3 weeks',
                'difficulty': '⭐⭐⭐',
                'github_topics': ['churn-prediction', 'classification', 'shap'],
            },
        ],
        'advanced': [
            {
                'title': 'Recommendation System',
                'description': 'Build a collaborative filtering recommendation engine like Netflix.',
                'technologies': ['Python', 'Surprise', 'TensorFlow', 'FastAPI', 'Redis'],
                'duration': '4-6 weeks',
                'difficulty': '⭐⭐⭐⭐',
                'github_topics': ['recommendation-system', 'collaborative-filtering'],
            },
            {
                'title': 'Stock Price Forecasting',
                'description': 'Time-series forecasting of stock prices using LSTM and Prophet.',
                'technologies': ['Python', 'TensorFlow', 'Prophet', 'yfinance', 'Plotly'],
                'duration': '3-5 weeks',
                'difficulty': '⭐⭐⭐⭐',
                'github_topics': ['stock-prediction', 'lstm', 'time-series'],
            },
        ],
    },
    'AI/ML': {
        'beginner': [
            {
                'title': 'Handwritten Digit Recognizer',
                'description': 'Train a neural network to recognize handwritten digits using MNIST dataset.',
                'technologies': ['Python', 'TensorFlow/Keras', 'NumPy', 'Matplotlib'],
                'duration': '1 week',
                'difficulty': '⭐⭐',
                'github_topics': ['mnist', 'neural-network', 'deep-learning'],
            },
            {
                'title': 'Sentiment Analysis Tool',
                'description': 'Classify movie/product reviews as positive or negative.',
                'technologies': ['Python', 'NLTK', 'Scikit-learn', 'Flask'],
                'duration': '1-2 weeks',
                'difficulty': '⭐⭐',
                'github_topics': ['sentiment-analysis', 'nlp', 'text-classification'],
            },
        ],
        'intermediate': [
            {
                'title': 'Image Classification App',
                'description': 'Web app that classifies uploaded images using a pre-trained CNN.',
                'technologies': ['Python', 'TensorFlow', 'Flask', 'React', 'Transfer Learning'],
                'duration': '2-3 weeks',
                'difficulty': '⭐⭐⭐',
                'github_topics': ['image-classification', 'cnn', 'transfer-learning'],
            },
            {
                'title': 'AI Resume Analyzer',
                'description': 'Extract skills from resumes and calculate ATS compatibility score.',
                'technologies': ['Python', 'spaCy', 'PyPDF2', 'Flask', 'scikit-learn'],
                'duration': '3-4 weeks',
                'difficulty': '⭐⭐⭐',
                'github_topics': ['resume-parser', 'nlp', 'ats'],
            },
        ],
        'advanced': [
            {
                'title': 'LLM-Powered Chatbot',
                'description': 'Build a domain-specific chatbot using LangChain and a vector database.',
                'technologies': ['Python', 'LangChain', 'OpenAI/Gemini', 'ChromaDB', 'FastAPI'],
                'duration': '4-6 weeks',
                'difficulty': '⭐⭐⭐⭐⭐',
                'github_topics': ['langchain', 'llm', 'rag', 'chatbot'],
            },
            {
                'title': 'Real-time Object Detection',
                'description': 'Detect and track objects in live video streams using YOLO.',
                'technologies': ['Python', 'YOLOv8', 'OpenCV', 'FastAPI', 'React'],
                'duration': '3-5 weeks',
                'difficulty': '⭐⭐⭐⭐',
                'github_topics': ['yolo', 'object-detection', 'computer-vision'],
            },
        ],
    },
    'Automation': {
        'beginner': [
            {
                'title': 'Web Scraper',
                'description': 'Scrape product prices or news headlines and save to CSV.',
                'technologies': ['Python', 'BeautifulSoup', 'Requests', 'Pandas'],
                'duration': '3-5 days',
                'difficulty': '⭐⭐',
                'github_topics': ['web-scraping', 'beautifulsoup', 'python'],
            },
        ],
        'intermediate': [
            {
                'title': 'Email Automation System',
                'description': 'Automate sending personalized emails with attachments and scheduling.',
                'technologies': ['Python', 'smtplib', 'schedule', 'Jinja2'],
                'duration': '1-2 weeks',
                'difficulty': '⭐⭐⭐',
                'github_topics': ['email-automation', 'python', 'scheduling'],
            },
        ],
        'advanced': [
            {
                'title': 'RPA Bot',
                'description': 'Robotic Process Automation bot for repetitive browser tasks.',
                'technologies': ['Python', 'Selenium', 'PyAutoGUI', 'Playwright'],
                'duration': '3-4 weeks',
                'difficulty': '⭐⭐⭐⭐',
                'github_topics': ['rpa', 'selenium', 'automation'],
            },
        ],
    },
}


def recommend_projects(skills: list, domain: str = '', level: str = 'beginner') -> list:
    """
    Recommend projects based on user skills, domain, and level.

    Returns:
        list of project dicts
    """
    skills_lower = [s.lower() for s in skills]
    results = []

    # Determine which domains to search
    if domain and domain in PROJECTS_DB:
        domains_to_search = [domain]
    else:
        # Auto-detect domain from skills
        domains_to_search = list(PROJECTS_DB.keys())

    for dom in domains_to_search:
        dom_projects = PROJECTS_DB.get(dom, {})
        level_projects = dom_projects.get(level, [])

        for project in level_projects:
            # Calculate relevance score
            tech_lower = [t.lower() for t in project['technologies']]
            matches = sum(1 for s in skills_lower if any(s in t or t in s for t in tech_lower))
            relevance = (matches / len(tech_lower)) * 100 if tech_lower else 0

            results.append({
                **project,
                'domain': dom,
                'level': level,
                'relevance': round(relevance),
                'match_count': matches,
            })

    # Sort by relevance
    results.sort(key=lambda x: x['relevance'], reverse=True)
    return results[:9]  # Return top 9
