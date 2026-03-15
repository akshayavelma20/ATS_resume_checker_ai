from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import shutil
import os
import re

# ===== File Parsing =====
import docx2txt
from PyPDF2 import PdfReader

# ===== NLP =====
import spacy
nlp = spacy.load("en_core_web_sm")

# ===== Embeddings =====
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# ===== LLM (Local - Ollama, optional) =====
import requests

# ================= APP =================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= UTILITIES =================

def extract_pdf_text(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def extract_docx_text(file_path):
    return docx2txt.process(file_path)


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    return text


def extract_keywords(text):
    doc = nlp(text)
    keywords = set()

    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"] and len(token.text) > 2:
            keywords.add(token.lemma_.lower())

    return list(keywords)


def compute_similarity(text1, text2):
    emb1 = model.encode([text1])
    emb2 = model.encode([text2])
    score = cosine_similarity(emb1, emb2)[0][0]
    return float(score)


def generate_local_summary(score, matched, missing):
    try:
        prompt = f"""
        Candidate ATS Score: {score}%
        Matched Skills: {', '.join(matched)}
        Missing Skills: {', '.join(missing)}

        Write a short professional hiring summary.
        """

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        if response.status_code == 200:
            return response.json()["response"]

        return "Summary unavailable."

    except:
        return "Summary unavailable (LLM not running)."


# ================= API =================

@app.get("/")
def home():
    return {"message": "Smart Match ATS API Running"}


@app.post("/match")
async def match_resume(
    jd_text: str = Form(...),
    file: Optional[UploadFile] = File(None),
    resume_text: Optional[str] = Form(None)
):
    # ===== Get Resume Text =====
    text = ""

    if file:
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if file.filename.endswith(".pdf"):
            text = extract_pdf_text(temp_path)
        elif file.filename.endswith(".docx"):
            text = extract_docx_text(temp_path)
        else:
            os.remove(temp_path)
            return {"error": "Unsupported file type"}

        os.remove(temp_path)

    elif resume_text:
        text = resume_text

    else:
        return {"error": "Provide resume file or resume_text"}

    # ===== Clean =====
    resume_clean = clean_text(text)
    jd_clean = clean_text(jd_text)

    # ===== NLP Keywords =====
    resume_keywords = extract_keywords(resume_clean)
    jd_keywords = extract_keywords(jd_clean)

    resume_set = set(resume_keywords)
    jd_set = set(jd_keywords)

    matched = list(resume_set & jd_set)
    missing = list(jd_set - resume_set)
    extra = list(resume_set - jd_set)

    # ===== Similarity =====
    sim_score = compute_similarity(resume_clean, jd_clean)
    final_score = int(sim_score * 100)

    # ===== Level =====
    if final_score >= 75:
        level = "Senior"
        decision = "Strong Fit"
    elif final_score >= 50:
        level = "Mid"
        decision = "Potential Fit"
    else:
        level = "Junior"
        decision = "Needs Improvement"

    # ===== AI Summary =====
    summary = generate_local_summary(final_score, matched[:10], missing[:10])

    # ===== Response =====
    return {
        "final_score": final_score,
        "similarity_score": round(sim_score * 100, 2),
        "matched_skills": matched[:15],
        "missing_skills": missing[:15],
        "extra_skills": extra[:15],
        "level": level,
        "decision": decision,
        "summary": summary
    }