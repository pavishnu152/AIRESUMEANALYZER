# api.py
import io
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

import pdfplumber
from docx import Document

from rewrite_engine import rewrite_resume
from ats_engine import calculate_ats_report

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # you can restrict later to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------- CONFIG: max resume characters sent to Groq ---------

MAX_RESUME_CHARS = 15000  # adjust if needed

def shorten_resume(resume_text: str) -> str:
    """Limit resume text so Groq does not throw length errors."""
    if len(resume_text) <= MAX_RESUME_CHARS:
        return resume_text
    return resume_text[:MAX_RESUME_CHARS]

# --------- HELPER: extract text from uploaded file (PDF / DOCX / TXT) ---------

async def extract_resume_text(file: UploadFile) -> str:
    """
    Extract text based on file type:
    - .pdf  -> pdfplumber
    - .docx -> python-docx
    - other -> simple decode
    """
    content_bytes = await file.read()
    filename = (file.filename or "").lower()

    # DOCX
    if filename.endswith(".docx"):
        try:
            doc_file = io.BytesIO(content_bytes)
            doc = Document(doc_file)
            text = "\n".join(p.text for p in doc.paragraphs)
            return text
        except Exception:
            return content_bytes.decode(errors="ignore")

    # PDF
    if filename.endswith(".pdf"):
        try:
            pdf_file = io.BytesIO(content_bytes)
            text = ""
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            return text
        except Exception:
            return content_bytes.decode(errors="ignore")

    # TXT or unknown → assume text
    return content_bytes.decode(errors="ignore")

# --------- ROOT ---------

@app.get("/")
def root():
    return {"message": "AI Resume Analyzer backend running"}

# --------- ANALYZE: file + JD -> ATS, skills, summary, rewritten resume ---------

@app.post("/analyze")
async def analyze_endpoint(
    file: UploadFile = File(...),
    job_description: str = Form(...),
):
    resume_text = await extract_resume_text(file)
    resume_text = shorten_resume(resume_text)

    print("========== ANALYZE DEBUG ==========")
    print("FILENAME:", file.filename)
    print("RESUME LENGTH (AFTER CUT):", len(resume_text))
    print("JD LENGTH:", len(job_description))
    print("===================================")

    report = calculate_ats_report(resume_text, job_description)
    # report should be a dict with:
    # ats_score, match_score, skill_match, skill_mismatch, summary, rewritten_resume

    return {
        "filename": file.filename,
        "resume_text": resume_text,
        **report,
    }

# --------- REWRITE: file + JD -> rewritten resume only ---------

@app.post("/rewrite")
async def rewrite_endpoint(
    file: UploadFile = File(...),
    job_description: str = Form(...),
):
    resume_text = await extract_resume_text(file)
    resume_text = shorten_resume(resume_text)

    print("========== REWRITE DEBUG ==========")
    print("FILENAME:", file.filename)
    print("RESUME LENGTH (AFTER CUT):", len(resume_text))
    print("JD LENGTH:", len(job_description))
    print("===================================")

    rewritten = rewrite_resume(resume_text, job_description)

    return {
        "filename": file.filename,
        "rewritten_resume": rewritten,
    }
