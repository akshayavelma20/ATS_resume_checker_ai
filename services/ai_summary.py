from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_ai_summary(score, matched, missing):
    prompt = f"""
You are an ATS Resume Evaluator.

Score: {score}%
Matched Skills: {', '.join(matched)}
Missing Skills: {', '.join(missing)}

Write a SHORT professional evaluation:
1. One sentence overall fit
2. One sentence strengths
3. One sentence improvements
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return response.choices[0].message.content

    except Exception:
        return "AI summary unavailable."