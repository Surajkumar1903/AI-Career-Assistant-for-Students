"""
Interview Question Generator Engine
Generates HR, Technical, Python, AI/ML, and Web Dev questions
"""
import random

QUESTION_CATEGORIES = {
    'hr':         'HR & Behavioral',
    'technical':  'Technical General',
    'python':     'Python Programming',
    'aiml':       'AI / Machine Learning',
    'webdev':     'Web Development',
    'dsa':        'Data Structures & Algorithms',
    'database':   'Database & SQL',
    'system':     'System Design',
}

QUESTIONS_DB = {
    'hr': {
        'beginner': [
            "Tell me about yourself.",
            "Why do you want to work here?",
            "What are your strengths and weaknesses?",
            "Where do you see yourself in 5 years?",
            "Why are you leaving your current job?",
            "Describe a challenge you faced and how you overcame it.",
            "How do you handle stress and pressure?",
            "What motivates you?",
            "Are you a team player? Give an example.",
            "What do you know about our company?",
            "Why should we hire you?",
            "What are your salary expectations?",
            "Do you have any questions for us?",
            "Describe your ideal work environment.",
            "How do you prioritize your tasks?",
        ],
        'intermediate': [
            "Describe a time you led a team through a difficult project.",
            "How do you handle conflict with a colleague?",
            "Tell me about a time you failed and what you learned.",
            "How do you stay updated with industry trends?",
            "Describe a situation where you had to meet a tight deadline.",
            "How do you handle feedback and criticism?",
            "Tell me about a time you went above and beyond.",
            "How do you manage multiple projects simultaneously?",
            "Describe your leadership style.",
            "How do you build relationships with stakeholders?",
        ],
        'advanced': [
            "How would you handle a situation where your team disagrees with your decision?",
            "Describe a time you drove organizational change.",
            "How do you mentor junior team members?",
            "Tell me about a time you had to make a difficult ethical decision.",
            "How do you align your team's goals with company objectives?",
            "Describe your approach to performance management.",
            "How do you handle underperforming team members?",
            "Tell me about a time you influenced without authority.",
        ],
    },
    'python': {
        'beginner': [
            "What is Python? What are its key features?",
            "What is the difference between a list and a tuple?",
            "Explain Python's indentation rules.",
            "What are Python data types?",
            "What is the difference between '==' and 'is'?",
            "What are Python decorators?",
            "Explain list comprehensions with an example.",
            "What is the difference between append() and extend()?",
            "What are *args and **kwargs?",
            "What is a lambda function?",
            "How does Python handle memory management?",
            "What is the difference between range() and xrange()?",
            "Explain the concept of mutable vs immutable objects.",
            "What is PEP 8?",
            "How do you handle exceptions in Python?",
        ],
        'intermediate': [
            "Explain Python's GIL (Global Interpreter Lock).",
            "What are generators and how do they differ from iterators?",
            "Explain the difference between @staticmethod and @classmethod.",
            "What is monkey patching in Python?",
            "Explain Python's MRO (Method Resolution Order).",
            "What are context managers? How do you create one?",
            "Explain the difference between deepcopy and shallow copy.",
            "What is metaclass in Python?",
            "How does Python's garbage collection work?",
            "Explain the difference between multiprocessing and multithreading.",
            "What are Python descriptors?",
            "Explain the LEGB rule in Python.",
        ],
        'advanced': [
            "How would you optimize a Python application for performance?",
            "Explain Python's asyncio and event loop.",
            "What are coroutines and how do they work?",
            "How do you profile Python code?",
            "Explain the difference between __new__ and __init__.",
            "What are abstract base classes (ABCs)?",
            "How do you implement a singleton pattern in Python?",
            "Explain Python's data model and dunder methods.",
        ],
    },
    'aiml': {
        'beginner': [
            "What is the difference between AI, ML, and Deep Learning?",
            "Explain supervised vs unsupervised learning.",
            "What is overfitting and how do you prevent it?",
            "What is a confusion matrix?",
            "Explain the bias-variance tradeoff.",
            "What is cross-validation?",
            "What is the difference between classification and regression?",
            "What is gradient descent?",
            "Explain precision, recall, and F1 score.",
            "What is feature engineering?",
            "What is a neural network?",
            "What is the difference between batch and stochastic gradient descent?",
            "What is regularization? Explain L1 and L2.",
            "What is a decision tree?",
            "What is the curse of dimensionality?",
        ],
        'intermediate': [
            "Explain how Random Forest works.",
            "What is the difference between bagging and boosting?",
            "Explain the backpropagation algorithm.",
            "What are CNNs and how do they work?",
            "What is transfer learning?",
            "Explain LSTM and when to use it.",
            "What is attention mechanism in transformers?",
            "How does k-means clustering work?",
            "What is PCA and when would you use it?",
            "Explain the ROC-AUC curve.",
            "What is the difference between generative and discriminative models?",
            "What is dropout and why is it used?",
        ],
        'advanced': [
            "Explain the transformer architecture in detail.",
            "What is BERT and how does it differ from GPT?",
            "How would you handle class imbalance in a dataset?",
            "Explain reinforcement learning and its key components.",
            "What is a GAN and how does it work?",
            "How do you deploy ML models to production?",
            "What is MLOps and why is it important?",
            "Explain the concept of model interpretability.",
            "What are vector databases and how are they used in AI?",
            "Explain RAG (Retrieval-Augmented Generation).",
        ],
    },
    'webdev': {
        'beginner': [
            "What is the difference between HTML, CSS, and JavaScript?",
            "Explain the CSS box model.",
            "What is responsive design?",
            "What is the difference between GET and POST requests?",
            "What is a REST API?",
            "Explain the difference between == and === in JavaScript.",
            "What is the DOM?",
            "What is CSS Flexbox?",
            "What is the difference between let, const, and var?",
            "What is a callback function?",
            "What is JSON?",
            "What is the difference between synchronous and asynchronous code?",
            "What is localStorage vs sessionStorage?",
            "What is CORS?",
            "What is a cookie?",
        ],
        'intermediate': [
            "Explain the event loop in JavaScript.",
            "What are Promises and async/await?",
            "What is React's virtual DOM?",
            "Explain React hooks (useState, useEffect).",
            "What is state management? Explain Redux.",
            "What is server-side rendering vs client-side rendering?",
            "Explain RESTful API design principles.",
            "What is GraphQL and how does it differ from REST?",
            "What is JWT authentication?",
            "Explain the concept of microservices.",
            "What is WebSocket and when would you use it?",
            "What is a CDN?",
        ],
        'advanced': [
            "How would you optimize a web application's performance?",
            "Explain the critical rendering path.",
            "What is Web Assembly?",
            "How do you implement caching strategies?",
            "Explain Progressive Web Apps (PWAs).",
            "What is the difference between OAuth and OpenID Connect?",
            "How would you design a scalable web architecture?",
            "What are Web Components?",
        ],
    },
    'technical': {
        'beginner': [
            "What is Object-Oriented Programming?",
            "Explain the four pillars of OOP.",
            "What is the difference between a stack and a queue?",
            "What is version control and why is it important?",
            "What is the difference between compiled and interpreted languages?",
            "What is an API?",
            "What is the difference between TCP and UDP?",
            "What is an operating system?",
            "What is a database?",
            "What is the difference between SQL and NoSQL?",
        ],
        'intermediate': [
            "Explain SOLID principles.",
            "What is the difference between process and thread?",
            "What are design patterns? Name a few.",
            "Explain the MVC architecture.",
            "What is caching and what are common caching strategies?",
            "What is a load balancer?",
            "Explain the CAP theorem.",
            "What is a message queue?",
            "What is containerization?",
            "Explain CI/CD pipelines.",
        ],
        'advanced': [
            "How would you design a URL shortener like bit.ly?",
            "How would you design a distributed cache?",
            "Explain eventual consistency.",
            "How would you handle database sharding?",
            "What is the difference between horizontal and vertical scaling?",
            "How would you design a notification system?",
            "Explain the two-phase commit protocol.",
            "How would you design a rate limiter?",
        ],
    },
    'dsa': {
        'beginner': [
            "What is the time complexity of binary search?",
            "Explain the difference between an array and a linked list.",
            "What is a hash table?",
            "What is Big O notation?",
            "Explain bubble sort.",
            "What is a binary tree?",
            "What is recursion?",
            "What is a stack? Give a real-world example.",
            "What is a queue? Give a real-world example.",
            "What is the difference between BFS and DFS?",
        ],
        'intermediate': [
            "Explain quicksort and its time complexity.",
            "What is a balanced binary search tree?",
            "Explain dynamic programming with an example.",
            "What is a graph? Explain adjacency list vs matrix.",
            "What is Dijkstra's algorithm?",
            "Explain the sliding window technique.",
            "What is a heap and when would you use it?",
            "Explain the two-pointer technique.",
        ],
        'advanced': [
            "Explain the Knuth-Morris-Pratt (KMP) algorithm.",
            "What is a segment tree?",
            "Explain topological sorting.",
            "What is a trie and when would you use it?",
            "Explain the union-find data structure.",
            "What is the traveling salesman problem?",
            "Explain amortized analysis.",
        ],
    },
    'database': {
        'beginner': [
            "What is a primary key?",
            "What is a foreign key?",
            "What is normalization?",
            "What is the difference between INNER JOIN and LEFT JOIN?",
            "What is an index in a database?",
            "What is a transaction?",
            "What are ACID properties?",
            "What is the difference between DELETE and TRUNCATE?",
            "What is a stored procedure?",
            "What is a view in SQL?",
        ],
        'intermediate': [
            "Explain database denormalization and when to use it.",
            "What is a composite index?",
            "Explain the difference between clustered and non-clustered indexes.",
            "What is query optimization?",
            "Explain the difference between OLTP and OLAP.",
            "What is database replication?",
            "What is a deadlock and how do you prevent it?",
            "Explain the difference between optimistic and pessimistic locking.",
        ],
        'advanced': [
            "How would you design a database schema for a social media platform?",
            "Explain database partitioning strategies.",
            "What is eventual consistency in distributed databases?",
            "How do you handle database migrations in production?",
            "Explain the differences between PostgreSQL and MySQL.",
            "What is a time-series database?",
        ],
    },
    'system': {
        'beginner': [
            "What is system design?",
            "What is scalability?",
            "What is the difference between latency and throughput?",
            "What is a monolithic vs microservices architecture?",
            "What is a reverse proxy?",
        ],
        'intermediate': [
            "How would you design a URL shortener?",
            "How would you design a file storage system like Dropbox?",
            "Explain the concept of consistent hashing.",
            "How would you design a rate limiter?",
            "What is a service mesh?",
        ],
        'advanced': [
            "How would you design Twitter's timeline feature?",
            "How would you design a distributed key-value store?",
            "How would you design a real-time collaborative editor?",
            "How would you design a global CDN?",
            "How would you design a payment processing system?",
        ],
    },
}


def generate_questions(category: str, level: str, role: str = '', count: int = 10) -> list:
    """
    Generate interview questions.

    Args:
        category: question category key
        level: 'beginner' | 'intermediate' | 'advanced'
        role: optional job role for context
        count: number of questions to return

    Returns:
        list of question strings
    """
    cat_data = QUESTIONS_DB.get(category, QUESTIONS_DB['hr'])
    level_key = level if level in cat_data else 'beginner'

    # Combine current level + one level up for variety
    pool = list(cat_data[level_key])
    levels = ['beginner', 'intermediate', 'advanced']
    idx = levels.index(level_key)
    if idx < len(levels) - 1:
        next_level = levels[idx + 1]
        if next_level in cat_data:
            pool += cat_data[next_level][:3]

    random.shuffle(pool)
    selected = pool[:count]

    # Add role-specific prefix if provided
    if role:
        selected = [f"[{role}] {q}" if i < 2 else q for i, q in enumerate(selected)]

    return selected
