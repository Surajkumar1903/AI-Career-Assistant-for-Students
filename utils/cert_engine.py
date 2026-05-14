"""
Certification Recommendation Engine
Suggests certifications from Google, IBM, Microsoft, Coursera, AWS, Deloitte, etc.
"""

CERT_PROVIDERS = ['All', 'Google', 'IBM', 'Microsoft', 'AWS', 'Coursera', 'Deloitte', 'Cisco', 'CompTIA']

CERTIFICATIONS_DB = [
    # ── Google ─────────────────────────────────────────────────────────────────
    {
        'name': 'Google Data Analytics Professional Certificate',
        'provider': 'Google',
        'platform': 'Coursera',
        'field': 'Data Science',
        'level': 'beginner',
        'duration': '6 months',
        'cost': 'Paid (Financial Aid Available)',
        'skills': ['data analysis', 'sql', 'tableau', 'r', 'spreadsheets'],
        'url': 'https://www.coursera.org/professional-certificates/google-data-analytics',
        'rating': 4.8,
        'enrolled': '2M+',
        'description': 'Learn the foundations of data analytics with hands-on projects.',
    },
    {
        'name': 'Google IT Support Professional Certificate',
        'provider': 'Google',
        'platform': 'Coursera',
        'field': 'IT Support',
        'level': 'beginner',
        'duration': '6 months',
        'cost': 'Paid (Financial Aid Available)',
        'skills': ['networking', 'linux', 'troubleshooting', 'security'],
        'url': 'https://www.coursera.org/professional-certificates/google-it-support',
        'rating': 4.8,
        'enrolled': '3M+',
        'description': 'Prepare for a career in IT support with Google.',
    },
    {
        'name': 'Google UX Design Professional Certificate',
        'provider': 'Google',
        'platform': 'Coursera',
        'field': 'UX Design',
        'level': 'beginner',
        'duration': '6 months',
        'cost': 'Paid (Financial Aid Available)',
        'skills': ['figma', 'ux design', 'prototyping', 'user research'],
        'url': 'https://www.coursera.org/professional-certificates/google-ux-design',
        'rating': 4.8,
        'enrolled': '1M+',
        'description': 'Design user-centered products with Google\'s UX curriculum.',
    },
    {
        'name': 'TensorFlow Developer Certificate',
        'provider': 'Google',
        'platform': 'TensorFlow',
        'field': 'AI/ML',
        'level': 'intermediate',
        'duration': '3-6 months prep',
        'cost': '$100',
        'skills': ['tensorflow', 'deep learning', 'python', 'neural networks', 'cnn', 'nlp'],
        'url': 'https://www.tensorflow.org/certificate',
        'rating': 4.9,
        'enrolled': '50K+',
        'description': 'Demonstrate proficiency in using TensorFlow to solve deep learning problems.',
    },
    # ── IBM ────────────────────────────────────────────────────────────────────
    {
        'name': 'IBM Data Science Professional Certificate',
        'provider': 'IBM',
        'platform': 'Coursera',
        'field': 'Data Science',
        'level': 'beginner',
        'duration': '11 months',
        'cost': 'Paid (Financial Aid Available)',
        'skills': ['python', 'sql', 'machine learning', 'data visualization', 'pandas'],
        'url': 'https://www.coursera.org/professional-certificates/ibm-data-science',
        'rating': 4.6,
        'enrolled': '1.5M+',
        'description': 'Kickstart your data science career with IBM\'s comprehensive program.',
    },
    {
        'name': 'IBM AI Engineering Professional Certificate',
        'provider': 'IBM',
        'platform': 'Coursera',
        'field': 'AI/ML',
        'level': 'intermediate',
        'duration': '8 months',
        'cost': 'Paid (Financial Aid Available)',
        'skills': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'keras'],
        'url': 'https://www.coursera.org/professional-certificates/ai-engineer',
        'rating': 4.6,
        'enrolled': '200K+',
        'description': 'Master AI engineering skills with hands-on projects.',
    },
    {
        'name': 'IBM Full Stack Software Developer',
        'provider': 'IBM',
        'platform': 'Coursera',
        'field': 'Web Development',
        'level': 'beginner',
        'duration': '12 months',
        'cost': 'Paid (Financial Aid Available)',
        'skills': ['html', 'css', 'javascript', 'react', 'node.js', 'python', 'django'],
        'url': 'https://www.coursera.org/professional-certificates/ibm-full-stack-cloud-developer',
        'rating': 4.5,
        'enrolled': '300K+',
        'description': 'Become a full-stack developer with IBM\'s cloud-focused curriculum.',
    },
    # ── Microsoft ──────────────────────────────────────────────────────────────
    {
        'name': 'Microsoft Azure Fundamentals (AZ-900)',
        'provider': 'Microsoft',
        'platform': 'Microsoft Learn',
        'field': 'Cloud Computing',
        'level': 'beginner',
        'duration': '1-2 months',
        'cost': '$165',
        'skills': ['azure', 'cloud computing', 'networking', 'security'],
        'url': 'https://learn.microsoft.com/en-us/certifications/azure-fundamentals/',
        'rating': 4.7,
        'enrolled': '500K+',
        'description': 'Foundational knowledge of cloud services and Azure.',
    },
    {
        'name': 'Microsoft Azure AI Fundamentals (AI-900)',
        'provider': 'Microsoft',
        'platform': 'Microsoft Learn',
        'field': 'AI/ML',
        'level': 'beginner',
        'duration': '1-2 months',
        'cost': '$165',
        'skills': ['azure', 'machine learning', 'ai', 'cognitive services'],
        'url': 'https://learn.microsoft.com/en-us/certifications/azure-ai-fundamentals/',
        'rating': 4.7,
        'enrolled': '300K+',
        'description': 'Understand AI workloads and considerations on Azure.',
    },
    {
        'name': 'Microsoft Power BI Data Analyst (PL-300)',
        'provider': 'Microsoft',
        'platform': 'Microsoft Learn',
        'field': 'Data Science',
        'level': 'intermediate',
        'duration': '2-3 months',
        'cost': '$165',
        'skills': ['power bi', 'data analysis', 'dax', 'sql'],
        'url': 'https://learn.microsoft.com/en-us/certifications/power-bi-data-analyst-associate/',
        'rating': 4.6,
        'enrolled': '200K+',
        'description': 'Demonstrate skills in data modeling and visualization with Power BI.',
    },
    # ── AWS ────────────────────────────────────────────────────────────────────
    {
        'name': 'AWS Certified Cloud Practitioner',
        'provider': 'AWS',
        'platform': 'AWS Training',
        'field': 'Cloud Computing',
        'level': 'beginner',
        'duration': '1-2 months',
        'cost': '$100',
        'skills': ['aws', 'cloud computing', 's3', 'ec2', 'iam'],
        'url': 'https://aws.amazon.com/certification/certified-cloud-practitioner/',
        'rating': 4.8,
        'enrolled': '1M+',
        'description': 'Foundational understanding of AWS Cloud services and concepts.',
    },
    {
        'name': 'AWS Certified Solutions Architect – Associate',
        'provider': 'AWS',
        'platform': 'AWS Training',
        'field': 'Cloud Computing',
        'level': 'intermediate',
        'duration': '3-6 months',
        'cost': '$150',
        'skills': ['aws', 'architecture', 'networking', 'security', 'databases'],
        'url': 'https://aws.amazon.com/certification/certified-solutions-architect-associate/',
        'rating': 4.9,
        'enrolled': '800K+',
        'description': 'Design and deploy scalable systems on AWS.',
    },
    {
        'name': 'AWS Certified Machine Learning – Specialty',
        'provider': 'AWS',
        'platform': 'AWS Training',
        'field': 'AI/ML',
        'level': 'advanced',
        'duration': '6-12 months',
        'cost': '$300',
        'skills': ['aws', 'machine learning', 'sagemaker', 'deep learning', 'mlops'],
        'url': 'https://aws.amazon.com/certification/certified-machine-learning-specialty/',
        'rating': 4.8,
        'enrolled': '100K+',
        'description': 'Demonstrate expertise in building ML solutions on AWS.',
    },
    # ── Coursera / DeepLearning.AI ─────────────────────────────────────────────
    {
        'name': 'Deep Learning Specialization',
        'provider': 'Coursera',
        'platform': 'Coursera',
        'field': 'AI/ML',
        'level': 'intermediate',
        'duration': '5 months',
        'cost': 'Paid (Financial Aid Available)',
        'skills': ['deep learning', 'neural networks', 'tensorflow', 'python', 'cnn', 'rnn'],
        'url': 'https://www.coursera.org/specializations/deep-learning',
        'rating': 4.9,
        'enrolled': '1M+',
        'description': 'Andrew Ng\'s flagship deep learning course series.',
    },
    {
        'name': 'Meta Front-End Developer Professional Certificate',
        'provider': 'Coursera',
        'platform': 'Coursera',
        'field': 'Web Development',
        'level': 'beginner',
        'duration': '7 months',
        'cost': 'Paid (Financial Aid Available)',
        'skills': ['html', 'css', 'javascript', 'react', 'ux design'],
        'url': 'https://www.coursera.org/professional-certificates/meta-front-end-developer',
        'rating': 4.7,
        'enrolled': '400K+',
        'description': 'Learn front-end development from Meta engineers.',
    },
    # ── CompTIA ────────────────────────────────────────────────────────────────
    {
        'name': 'CompTIA Security+',
        'provider': 'CompTIA',
        'platform': 'CompTIA',
        'field': 'Cybersecurity',
        'level': 'beginner',
        'duration': '2-3 months',
        'cost': '$392',
        'skills': ['security', 'networking', 'cryptography', 'risk management'],
        'url': 'https://www.comptia.org/certifications/security',
        'rating': 4.8,
        'enrolled': '500K+',
        'description': 'Industry-standard entry-level cybersecurity certification.',
    },
    # ── Deloitte ───────────────────────────────────────────────────────────────
    {
        'name': 'Deloitte Data Analytics Simulation',
        'provider': 'Deloitte',
        'platform': 'Forage',
        'field': 'Data Science',
        'level': 'beginner',
        'duration': '1-2 weeks',
        'cost': 'Free',
        'skills': ['data analysis', 'excel', 'tableau', 'problem solving'],
        'url': 'https://www.theforage.com/simulations/deloitte/data-analytics-mbtn',
        'rating': 4.6,
        'enrolled': '200K+',
        'description': 'Virtual work experience in data analytics at Deloitte.',
    },
]


def recommend_certifications(skills: list, field: str = '', provider: str = '',
                              level: str = 'beginner') -> list:
    """
    Recommend certifications based on user skills, field, provider, and level.

    Returns:
        list of certification dicts sorted by relevance
    """
    skills_lower = [s.lower() for s in skills]
    results = []

    for cert in CERTIFICATIONS_DB:
        # Filter by provider
        if provider and provider != 'All' and cert['provider'].lower() != provider.lower():
            continue

        # Filter by field
        if field and field.lower() not in cert['field'].lower():
            continue

        # Calculate relevance
        cert_skills = cert['skills']
        matches = sum(1 for s in skills_lower if any(s in cs or cs in s for cs in cert_skills))
        relevance = (matches / len(cert_skills)) * 100 if cert_skills else 0

        # Level bonus
        level_bonus = 0
        if cert['level'] == level:
            level_bonus = 20
        elif (level == 'beginner' and cert['level'] == 'intermediate') or \
             (level == 'intermediate' and cert['level'] == 'advanced'):
            level_bonus = 10

        results.append({
            **cert,
            'relevance': round(relevance + level_bonus),
            'match_count': matches,
        })

    # Sort by relevance
    results.sort(key=lambda x: x['relevance'], reverse=True)
    return results[:12]
