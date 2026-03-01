from pypdf import PdfReader
from pypdf.errors import PdfReadError, PdfStreamError

def extract_questions(file_path):
    try:
        reader = PdfReader(file_path)
    except (PdfReadError, PdfStreamError, Exception):
        print("Invalid or corrupted PDF file.")
        return []

    text = ""

    for page in reader.pages:
        try:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        except:
            continue

    if not text.strip():
        return []

    questions = []
    for part in text.split("?"):
        part = part.strip()
        if len(part) > 5:
            questions.append(part + "?")

    return questions