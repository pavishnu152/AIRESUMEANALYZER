import tempfile
import os
from PyPDF2 import PdfReader
import docx

def _save_temp(upload):
    suffix = os.path.splitext(upload.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(upload.file.read())
        return tmp.name

def extract_text_from_upload(upload):
    path = _save_temp(upload)
    ext = os.path.splitext(upload.filename.lower())[1]

    text = ""

    try:
        if ext == ".pdf":
            reader = PdfReader(path)
            for page in reader.pages:
                text += page.extract_text() or ""
        elif ext == ".docx":
            d = docx.Document(path)
            text = "\n".join([p.text for p in d.paragraphs if p.text])
        else:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
    finally:
        os.remove(path)

    return text
