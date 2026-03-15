import spacy

nlp = spacy.load("en_core_web_sm")

# Real technical skill keywords
TECH_SKILLS = {
    "python","java","sql","aws","azure","gcp","docker","kubernetes",
    "tensorflow","pytorch","scikit-learn","pandas","numpy",
    "nlp","machine learning","deep learning","data science",
    "fastapi","flask","django","react","node","javascript",
    "rest api","git","linux","llm","transformers",
    "pinecone","faiss","vector database","spacy","nltk"
}

def extract_skills(text: str):
    text = text.lower()
    doc = nlp(text)

    found = set()

    # Check multi-word skills first
    for skill in TECH_SKILLS:
        if skill in text:
            found.add(skill)

    return sorted(list(found))