import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.3-70b-versatile"

def ai_improvement(resume_text: str, job_description: str) -> str:
    prompt = f"""
You are an ATS expert.

Resume content (unique):
{resume_text}

Job description (unique):
{job_description}

Give clear improvement suggestions:
- missing skills
- keyword fixes
- formatting advice
"""

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=500
    )

    return resp.choices[0].message.content
