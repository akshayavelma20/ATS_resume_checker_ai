def match_skills(candidate_skills, job_skills):

    if not job_skills:
        return [], 0, [], []

    matched = list(set(candidate_skills) & set(job_skills))
    score = int(len(matched) / len(job_skills) * 100)

    missing = list(set(job_skills) - set(candidate_skills))
    extra = list(set(candidate_skills) - set(job_skills))

    return matched, score, missing, extra
