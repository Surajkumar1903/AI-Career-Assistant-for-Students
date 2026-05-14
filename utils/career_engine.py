"""
Career Roadmap Generator Engine
Generates beginner-to-advanced learning roadmaps for various tech fields
"""

CAREER_ROADMAPS = {
    "Web Development": {
        "description": "Build modern, responsive web applications from front-end to back-end.",
        "beginner": {
            "phase": "Foundation (0-3 months)",
            "topics": ["HTML5 & Semantic Markup", "CSS3 & Flexbox/Grid", "JavaScript Basics",
                       "Git & GitHub", "Responsive Design", "Bootstrap/Tailwind CSS"],
            "projects": ["Personal Portfolio Website", "Landing Page Clone", "To-Do List App"],
            "resources": ["freeCodeCamp", "The Odin Project", "MDN Web Docs"],
        },
        "intermediate": {
            "phase": "Core Skills (3-6 months)",
            "topics": ["React.js or Vue.js", "Node.js & Express", "REST APIs", "SQL & MongoDB",
                       "Authentication (JWT)", "Deployment (Netlify/Vercel)"],
            "projects": ["Blog Platform", "E-commerce Frontend", "Weather App with API"],
            "resources": ["React Docs", "Node.js Docs", "Full Stack Open"],
        },
        "advanced": {
            "phase": "Professional Level (6-12 months)",
            "topics": ["TypeScript", "Next.js / Nuxt.js", "GraphQL", "Docker & CI/CD",
                       "Testing (Jest/Cypress)", "Performance Optimization", "Microservices"],
            "projects": ["Full-Stack SaaS App", "Real-time Chat App", "Job Board Platform"],
            "resources": ["AWS Docs", "System Design Primer", "Clean Code Book"],
        },
        "certifications": ["Meta Front-End Developer (Coursera)", "Google UX Design",
                           "AWS Certified Developer", "MongoDB Developer Certification"],
        "timeline": "6-12 months to job-ready",
        "avg_salary": "$70,000 - $120,000/year",
        "top_companies": ["Google", "Meta", "Amazon", "Startups"],
    },
    "Data Science": {
        "description": "Analyse data, build models, and extract insights to drive business decisions.",
        "beginner": {
            "phase": "Foundation (0-3 months)",
            "topics": ["Python Basics", "NumPy & Pandas", "Data Visualization (Matplotlib/Seaborn)",
                       "Statistics & Probability", "SQL Basics", "Excel"],
            "projects": ["EDA on Titanic Dataset", "Sales Dashboard", "COVID-19 Data Analysis"],
            "resources": ["Kaggle Learn", "DataCamp", "Python for Data Analysis Book"],
        },
        "intermediate": {
            "phase": "Machine Learning (3-6 months)",
            "topics": ["Scikit-learn", "Supervised & Unsupervised Learning", "Feature Engineering",
                       "Model Evaluation", "Tableau/Power BI", "Web Scraping"],
            "projects": ["House Price Prediction", "Customer Churn Model", "Sentiment Analysis"],
            "resources": ["Hands-On ML Book", "Fast.ai", "Kaggle Competitions"],
        },
        "advanced": {
            "phase": "Deep Learning & Deployment (6-12 months)",
            "topics": ["TensorFlow / PyTorch", "Deep Learning", "NLP & Transformers",
                       "MLOps & Model Deployment", "Big Data (Spark)", "Cloud ML (AWS/GCP)"],
            "projects": ["Image Classification App", "NLP Chatbot", "Recommendation System"],
            "resources": ["Deep Learning Specialization", "MLflow Docs", "Papers With Code"],
        },
        "certifications": ["IBM Data Science (Coursera)", "Google Data Analytics",
                           "AWS Machine Learning Specialty", "TensorFlow Developer Certificate"],
        "timeline": "8-14 months to job-ready",
        "avg_salary": "$85,000 - $140,000/year",
        "top_companies": ["Netflix", "Uber", "Airbnb", "Research Labs"],
    },
    "AI/ML Engineering": {
        "description": "Design and deploy production-grade AI and machine learning systems.",
        "beginner": {
            "phase": "Foundation (0-3 months)",
            "topics": ["Python", "Linear Algebra & Calculus", "Statistics", "NumPy/Pandas",
                       "Scikit-learn Basics", "Jupyter Notebooks"],
            "projects": ["Iris Classification", "Linear Regression from Scratch", "MNIST Digit Recognizer"],
            "resources": ["3Blue1Brown (Math)", "Kaggle Learn", "Andrew Ng ML Course"],
        },
        "intermediate": {
            "phase": "Deep Learning (3-8 months)",
            "topics": ["Neural Networks", "CNNs & RNNs", "TensorFlow/PyTorch", "Transfer Learning",
                       "NLP Basics", "Hugging Face Transformers", "Model Evaluation"],
            "projects": ["Image Classifier", "Text Sentiment Analyzer", "Object Detection App"],
            "resources": ["Deep Learning Specialization", "Fast.ai", "PyTorch Tutorials"],
        },
        "advanced": {
            "phase": "Production AI (8-14 months)",
            "topics": ["MLOps", "LLMs & Fine-tuning", "RAG Systems", "Vector Databases",
                       "Model Serving (FastAPI/TorchServe)", "Cloud AI (AWS SageMaker/Vertex AI)"],
            "projects": ["LLM-powered Chatbot", "AI Resume Analyzer", "Real-time Object Detection"],
            "resources": ["LangChain Docs", "MLflow", "Weights & Biases"],
        },
        "certifications": ["TensorFlow Developer Certificate", "AWS ML Specialty",
                           "Google Professional ML Engineer", "DeepLearning.AI Specializations"],
        "timeline": "10-16 months to job-ready",
        "avg_salary": "$100,000 - $180,000/year",
        "top_companies": ["OpenAI", "DeepMind", "Google Brain", "Meta AI"],
    },
    "Cloud Computing": {
        "description": "Design, deploy, and manage scalable cloud infrastructure.",
        "beginner": {
            "phase": "Foundation (0-2 months)",
            "topics": ["Linux Basics", "Networking Fundamentals", "Cloud Concepts",
                       "AWS/Azure/GCP Free Tier", "Git", "Bash Scripting"],
            "projects": ["Host a Static Website on S3", "Set up EC2 Instance", "Create VPC"],
            "resources": ["AWS Free Tier", "Linux Journey", "Cloud Guru"],
        },
        "intermediate": {
            "phase": "Core Services (2-6 months)",
            "topics": ["Docker & Containers", "Kubernetes", "Terraform (IaC)",
                       "CI/CD Pipelines", "Serverless (Lambda)", "Databases (RDS/DynamoDB)"],
            "projects": ["Containerized Web App", "Auto-scaling Setup", "Serverless API"],
            "resources": ["Kubernetes Docs", "Terraform Docs", "AWS Well-Architected"],
        },
        "advanced": {
            "phase": "Architecture & Security (6-12 months)",
            "topics": ["Microservices Architecture", "Service Mesh (Istio)", "Security & IAM",
                       "Cost Optimization", "Multi-cloud Strategy", "Monitoring (Prometheus/Grafana)"],
            "projects": ["Multi-region Deployment", "Zero-downtime CI/CD", "Cost Dashboard"],
            "resources": ["AWS Solutions Architect Guide", "CNCF Landscape", "Cloud Security Alliance"],
        },
        "certifications": ["AWS Solutions Architect Associate", "Google Associate Cloud Engineer",
                           "Azure Administrator", "Kubernetes CKA"],
        "timeline": "6-10 months to job-ready",
        "avg_salary": "$90,000 - $150,000/year",
        "top_companies": ["AWS", "Microsoft", "Google", "Accenture"],
    },
    "Cybersecurity": {
        "description": "Protect systems, networks, and data from digital attacks.",
        "beginner": {
            "phase": "Foundation (0-3 months)",
            "topics": ["Networking (TCP/IP, DNS, HTTP)", "Linux Command Line", "Python Basics",
                       "Cryptography Basics", "Security Concepts (CIA Triad)", "Wireshark"],
            "projects": ["Set up Home Lab", "Network Scanner Script", "Password Manager"],
            "resources": ["TryHackMe", "Cybrary", "CompTIA Study Guide"],
        },
        "intermediate": {
            "phase": "Ethical Hacking (3-7 months)",
            "topics": ["Penetration Testing", "Kali Linux", "Web App Security (OWASP Top 10)",
                       "Metasploit", "Burp Suite", "SIEM Tools"],
            "projects": ["CTF Challenges", "Vulnerable VM Exploitation", "Web App Pentest Report"],
            "resources": ["Hack The Box", "OWASP WebGoat", "PentesterLab"],
        },
        "advanced": {
            "phase": "Specialization (7-14 months)",
            "topics": ["Malware Analysis", "Incident Response", "Threat Intelligence",
                       "Cloud Security", "Zero Trust Architecture", "SOC Operations"],
            "projects": ["Malware Sandbox", "SIEM Dashboard", "Threat Hunting Report"],
            "resources": ["SANS Institute", "MITRE ATT&CK", "NIST Framework"],
        },
        "certifications": ["CompTIA Security+", "CEH (Certified Ethical Hacker)",
                           "OSCP", "CISSP", "AWS Security Specialty"],
        "timeline": "8-14 months to job-ready",
        "avg_salary": "$80,000 - $160,000/year",
        "top_companies": ["CrowdStrike", "Palo Alto", "IBM Security", "Government Agencies"],
    },
    "Mobile Development": {
        "description": "Build native and cross-platform mobile applications.",
        "beginner": {
            "phase": "Foundation (0-2 months)",
            "topics": ["Choose Platform (Android/iOS/Cross-platform)", "Kotlin or Swift Basics",
                       "UI/UX Principles", "Git", "Android Studio / Xcode"],
            "projects": ["Hello World App", "Calculator App", "Simple To-Do App"],
            "resources": ["Android Developers Docs", "Swift Playgrounds", "Flutter Docs"],
        },
        "intermediate": {
            "phase": "Core Development (2-6 months)",
            "topics": ["React Native or Flutter", "State Management", "REST API Integration",
                       "Firebase", "Local Storage", "Push Notifications"],
            "projects": ["Weather App", "Chat App", "E-commerce App"],
            "resources": ["Flutter Cookbook", "React Native Docs", "Firebase Docs"],
        },
        "advanced": {
            "phase": "Production Apps (6-12 months)",
            "topics": ["App Store Deployment", "Performance Optimization", "Testing",
                       "CI/CD for Mobile", "In-App Purchases", "AR/VR (ARKit/ARCore)"],
            "projects": ["Full-featured Social App", "AR Navigation App", "Published App"],
            "resources": ["App Store Guidelines", "Google Play Academy", "Fastlane Docs"],
        },
        "certifications": ["Google Associate Android Developer", "Apple Developer Program",
                           "Meta React Native Certificate"],
        "timeline": "6-10 months to job-ready",
        "avg_salary": "$75,000 - $130,000/year",
        "top_companies": ["Apple", "Google", "Spotify", "Startups"],
    },
}


def get_career_fields() -> list:
    return list(CAREER_ROADMAPS.keys())


def generate_roadmap(current_skills: list, field: str, level: str = 'beginner') -> dict:
    """
    Generate a personalised career roadmap.

    Args:
        current_skills: list of skills the user already has
        field: target career field
        level: 'beginner' | 'intermediate' | 'advanced'

    Returns:
        dict with roadmap data
    """
    # Find best matching field
    field_key = None
    for key in CAREER_ROADMAPS:
        if key.lower() == field.lower():
            field_key = key
            break
    if not field_key:
        # Fuzzy match
        for key in CAREER_ROADMAPS:
            if any(word in key.lower() for word in field.lower().split()):
                field_key = key
                break
    if not field_key:
        field_key = "Web Development"

    roadmap = CAREER_ROADMAPS[field_key]
    skills_lower = [s.lower() for s in current_skills]

    # Determine starting level based on existing skills
    if level == 'auto':
        beginner_topics = roadmap['beginner']['topics']
        matches = sum(1 for t in beginner_topics if any(s in t.lower() for s in skills_lower))
        if matches >= len(beginner_topics) * 0.6:
            level = 'intermediate'
        else:
            level = 'beginner'

    # Build phases to show
    phases = []
    all_levels = ['beginner', 'intermediate', 'advanced']
    start_idx  = all_levels.index(level) if level in all_levels else 0

    for lvl in all_levels[start_idx:]:
        phase_data = roadmap[lvl]
        # Mark topics the user already knows
        enriched_topics = []
        for topic in phase_data['topics']:
            known = any(s in topic.lower() for s in skills_lower)
            enriched_topics.append({'name': topic, 'known': known})

        phases.append({
            'level': lvl.title(),
            'phase': phase_data['phase'],
            'topics': enriched_topics,
            'projects': phase_data['projects'],
            'resources': phase_data['resources'],
        })

    return {
        'field': field_key,
        'description': roadmap['description'],
        'phases': phases,
        'certifications': roadmap['certifications'],
        'timeline': roadmap['timeline'],
        'avg_salary': roadmap['avg_salary'],
        'top_companies': roadmap['top_companies'],
        'current_skills': current_skills,
        'starting_level': level,
    }
