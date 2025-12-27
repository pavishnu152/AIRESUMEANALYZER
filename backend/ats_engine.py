# ats_engine.py
import os
import json
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

def calculate_ats_report(resume_text: str, job_description: str) -> dict:
    prompt = f"""
You are an ATS resume analyzer.

Analyze the candidate's resume against the job description and respond ONLY with a JSON object.

Resume:
{resume_text}

Job Description:
{job_description}

The JSON object MUST have exactly these keys and types:

{{
  "ats_score": <integer 0-100>,
  "match_score": <integer 0-100>,
  "skill_match": [<string>, ...],
  "skill_mismatch": [<string>, ...],
  "summary": "<2-3 sentence ATS-style summary>",
  "rewritten_resume": "<rewritten resume text>"
}}

Rules:
- Do NOT add any explanation, commentary, or text outside the JSON.
- Do NOT include markdown.
- Do NOT include trailing commas.
"""

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=900,
    )

    content = resp.choices[0].message.content or ""

    print("===== RAW MODEL OUTPUT (ANALYZE) =====")
    print(content)
    print("======================================")

    # 1) Try direct JSON
    try:
        data = json.loads(content)
        return _normalize_report(data, resume_text)
    except Exception:
        pass

    # 2) Try extracting between first '{' and last '}'
    start = content.find("{")
    end = content.rfind("}")
    if start != -1 and end != -1 and end > start:
        json_str = content[start:end+1]
        try:
            data = json.loads(json_str)
            return _normalize_report(data, resume_text)
        except Exception:
            pass

    # 3) Fallback: safe defaults so UI and /docs don't break
    return {
        "ats_score": 0,
        "match_score": 0,
        "skill_match": [],
        "skill_mismatch": [],
        "summary": "Analysis failed: could not parse model output.",
        "rewritten_resume": resume_text,
    }

def _normalize_report(data: dict, resume_text: str) -> dict:
    """Make sure all fields exist and have the right basic types."""
    if not isinstance(data, dict):
        raise ValueError("Model output is not a JSON object")

    ats_score = int(data.get("ats_score", 0))
    match_score = int(data.get("match_score", 0))

    skill_match = data.get("skill_match", [])
    if not isinstance(skill_match, list):
        skill_match = [str(skill_match)]

    skill_mismatch = data.get("skill_mismatch", [])
    if not isinstance(skill_mismatch, list):
        skill_mismatch = [str(skill_mismatch)]

    summary = str(data.get("summary", ""))
    rewritten_resume = str(data.get("rewritten_resume", resume_text))

    return {
        "ats_score": max(0, min(100, ats_score)),
        "match_score": max(0, min(100, match_score)),
        "skill_match": skill_match,
        "skill_mismatch": skill_mismatch,
        "summary": summary,
        "rewritten_resume": rewritten_resume,
    }
