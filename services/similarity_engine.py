def match_skills(resume_skills, jd_skills):
    resume_set = set(resume_skills)
    jd_set = set(jd_skills)

    matched = list(resume_set & jd_set)
    missing = list(jd_set - resume_set)
    extra = list(resume_set - jd_set)

    score = int((len(matched) / max(len(jd_set), 1)) * 100)

    return matched, score, missing, extra