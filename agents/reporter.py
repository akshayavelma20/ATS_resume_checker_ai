def generate_report(score, matched, missing):

    if score > 80:
        decision = "Strong Fit"
        summary = (
            f"Candidate strongly matches the job requirements with skills in "
            f"{', '.join(matched)}."
        )

    elif score > 60:
        decision = "Potential Fit"
        summary = (
            f"Candidate meets important requirements such as "
            f"{', '.join(matched)}, but lacks {', '.join(missing)}."
        )

    else:
        decision = "Needs Review"
        summary = (
            f"Candidate is missing critical skills like "
            f"{', '.join(missing)}."
        )

    return decision, summary
