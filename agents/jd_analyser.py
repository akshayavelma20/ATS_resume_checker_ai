from agents.skills_db import SKILLS


def analyze_jd(jd_text: str):
    jd_text = jd_text.lower()

    job_skills = []
    for skill in SKILLS:
        if skill in jd_text:
            job_skills.append(skill)

    return job_skills
