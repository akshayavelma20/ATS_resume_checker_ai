from services.embedding_engine import get_embedding
from services.similarity_engine import similarity_score

def match_resume_jd(resume_text, jd_text):
    r_vec = get_embedding(resume_text)
    j_vec = get_embedding(jd_text)
    score = similarity_score(r_vec, j_vec)
    return score
