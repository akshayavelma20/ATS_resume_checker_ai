from docx import Document

def extract_text_from_docx(file):
    document = Document(file)
    full_text = []

    for para in document.paragraphs:
        full_text.append(para.text)

    return "\n".join(full_text)
