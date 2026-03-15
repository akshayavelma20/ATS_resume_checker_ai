from agents.skills_db import SKILLS


def parse_resume(text: str):
    text = text.lower()

    found_skills = []
    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)

    # Placeholder experience logic
    # Later you can extract real years using regex
    experience = 3

    return {
        "skills": found_skills,
        "experience": experience
    }

