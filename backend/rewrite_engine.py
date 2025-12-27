import os
import uuid
from groq import Groq

# Read API key from environment variable
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"  # make sure this matches your Groq model name

def rewrite_resume(resume_text: str, job_description: str) -> str:
    """
    Rewrite the resume based on the job description.
    This function MUST be called directly by your FastAPI route.
    """

    # Unique id to force different prompts and help debugging
    unique_id = str(uuid.uuid4())

    prompt = f"""
You are an ATS-friendly resume rewriting assistant.

UNIQUE REQUEST ID: {unique_id}

Task:
Rewrite the candidate's resume so it matches the job description more closely.
Keep it professional, ATS-friendly, and focused on measurable impact.

Resume:
{resume_text}

Job Description:
{job_description}

Output:
Return only the rewritten resume text, no extra commentary.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.7,
        max_tokens=800,
    )

    return response.choices[0].message.content
