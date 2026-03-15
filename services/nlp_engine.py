import spacy
nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    doc = nlp(text)
    skills = [ent.text.lower() for ent in doc.ents]
    return list(set(skills))