from services.nlp_engine import extract_entities

def process_resume(text):
    skills = extract_entities(text)
    return {"skills": skills}
