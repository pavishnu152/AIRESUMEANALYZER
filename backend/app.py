from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="AI Resume Analyzer")


# ---------- RESPONSE MODEL ----------
class AnalyzeResponse(BaseModel):
    match_score: int
    ats_score: int
    skill_gap: List[str]
    improvements: List[str]
    summary: str


# ---------- ROUTE ----------
@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):

    # 1. Validate JD
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is empty")

    # 2. Validate file
    filename = file.filename.lower()
    if not filename.endswith((".pdf", ".docx")):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Upload PDF or DOCX only."
        )

    # 3. Read file safely
    try:
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Empty resume file")
    except Exception:
        raise HTTPException(status_code=500, detail="File read failed")

    # 4. TEMP STABLE RESPONSE (replace with AI later)
    return AnalyzeResponse(
        match_score=80,
        ats_score=85,
        skill_gap=["Docker", "System Design"],
        improvements=[
            "Add measurable impact to projects",
            "Improve keyword alignment with JD"
        ],
        summary="Good resume. Needs stronger ATS optimization."
    )
