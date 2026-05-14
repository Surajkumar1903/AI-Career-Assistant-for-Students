"""
LinkedIn Profile Optimizer Engine
Generates professional LinkedIn content sections
"""


def generate_linkedin_content(name: str, role: str, skills: list,
                               experience: str, achievements: str, education: str) -> dict:
    """
    Generate all LinkedIn profile sections.

    Returns:
        dict with headline, about, skills_section, post_caption, bio
    """
    skills_str = ', '.join(skills[:10]) if skills else 'various technologies'
    top_skills = skills[:5] if skills else ['Problem Solving', 'Communication', 'Teamwork']

    # ── Headline ───────────────────────────────────────────────────────────────
    if role and skills:
        headline = f"{role} | {' • '.join(top_skills[:3])} | Passionate about Technology & Innovation"
    elif role:
        headline = f"{role} | Aspiring Tech Professional | Open to Opportunities"
    else:
        headline = f"Aspiring Software Developer | {skills_str[:60]} | Lifelong Learner"

    # ── About Section ──────────────────────────────────────────────────────────
    about_parts = []
    about_parts.append(f"👋 Hi, I'm {name or 'a passionate tech professional'}!")
    about_parts.append("")

    if role:
        about_parts.append(f"🚀 I'm a {role} with a strong passion for building innovative solutions "
                           f"that make a real difference.")
    else:
        about_parts.append("🚀 I'm a passionate technology enthusiast dedicated to continuous learning "
                           "and building impactful solutions.")

    if experience:
        about_parts.append("")
        about_parts.append(f"💼 {experience[:200].strip()}")

    if skills:
        about_parts.append("")
        about_parts.append(f"🛠️ Technical Skills: {skills_str}")

    if achievements:
        about_parts.append("")
        about_parts.append(f"🏆 Key Achievements: {achievements[:200].strip()}")

    if education:
        about_parts.append("")
        about_parts.append(f"🎓 {education[:150].strip()}")

    about_parts.append("")
    about_parts.append("📫 Open to exciting opportunities and collaborations. Let's connect!")

    about = '\n'.join(about_parts)

    # ── Skills Section ─────────────────────────────────────────────────────────
    skill_categories = {
        'Technical Skills': [s for s in skills if s.lower() not in
                             ['communication', 'teamwork', 'leadership', 'problem solving',
                              'time management', 'adaptability', 'creativity']],
        'Soft Skills': [s for s in skills if s.lower() in
                       ['communication', 'teamwork', 'leadership', 'problem solving',
                        'time management', 'adaptability', 'creativity']],
    }
    if not skill_categories['Soft Skills']:
        skill_categories['Soft Skills'] = ['Communication', 'Problem Solving', 'Teamwork']

    skills_section = "**Top Skills:**\n"
    for cat, cat_skills in skill_categories.items():
        if cat_skills:
            skills_section += f"\n{cat}:\n"
            skills_section += '\n'.join(f"• {s}" for s in cat_skills[:8])
            skills_section += '\n'

    # ── Post Caption ───────────────────────────────────────────────────────────
    post_captions = [
        f"🚀 Excited to share my journey as a {role or 'developer'}!\n\n"
        f"I've been working with {skills_str[:80]} and the learning never stops. "
        f"Every challenge is an opportunity to grow.\n\n"
        f"What's the one skill you're currently mastering? Drop it in the comments! 👇\n\n"
        f"#TechCareer #{''.join(s.replace(' ', '') for s in top_skills[:3])} #Learning #Growth",

        f"💡 3 things I've learned as a {role or 'tech professional'}:\n\n"
        f"1️⃣ Consistency beats perfection every time\n"
        f"2️⃣ Your network is your net worth\n"
        f"3️⃣ {skills[0] if skills else 'Coding'} skills open doors you never imagined\n\n"
        f"What would you add to this list? 🤔\n\n"
        f"#CareerGrowth #TechLife #Motivation",
    ]

    # ── Professional Bio ───────────────────────────────────────────────────────
    bio = (
        f"{name or 'A passionate professional'} is a {role or 'technology enthusiast'} "
        f"with expertise in {skills_str[:100]}. "
    )
    if experience:
        bio += f"{experience[:150].strip()} "
    if achievements:
        bio += f"Notable achievements include {achievements[:100].strip()}. "
    bio += (
        f"Committed to continuous learning and delivering high-quality solutions, "
        f"{name.split()[0] if name else 'they'} is always looking for new challenges "
        f"and opportunities to make an impact."
    )

    return {
        'headline':       headline,
        'about':          about,
        'skills_section': skills_section,
        'post_captions':  post_captions,
        'bio':            bio,
        'name':           name,
        'role':           role,
        'skills':         skills,
    }
