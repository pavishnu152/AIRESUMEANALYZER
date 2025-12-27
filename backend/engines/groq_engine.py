import os
import json
from groq import Groq
from typing import Dict, Any

# --- Groq Client Initialization ---
# The client is initialized globally so it's accessible by all functions in this module.
# It automatically looks for the GROQ_API_KEY environment variable.
try:
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )
    # Define the model to use once
    GROQ_MODEL = "llama-3.1-8b-instant"
except Exception as e:
    # Handle the case where the client could not be initialized (e.g., missing API key)
    print(f"Error initializing Groq client: {e}")
    # Setting client to None to allow error handling inside the functions
    client = None
    GROQ_MODEL = None

# --- Core Analysis Function ---

def analyze_with_ai(resume_text: str, job_description: str) -> Dict[str, Any]:
    """
    Analyzes a resume against a job description using the Groq API.
    Returns a dictionary of analysis results (or an error dictionary).
    """
    if not client or not GROQ_MODEL:
        return {"error": "AI service not available. Check GROQ_API_KEY."}

    prompt = f"""
    You are an expert Resume Analyst. Your task is to compare a RESUME with a JOB DESCRIPTION.
    
    1. **Score:** Assign an overall match percentage score (0-100%).
    2. **Missing Skills:** Identify 3-5 critical skills mentioned in the JOB DESCRIPTION that are MISSING or weakly mentioned in the RESUME.
    3. **Actionable Suggestions:** Provide 3-5 concise, specific bullet points on how the RESUME should be modified to better match the JOB DESCRIPTION.
    4. **Keyword Match:** Extract 5-10 specific keywords from the JOB DESCRIPTION that the RESUME should include.

    **RESUME:**
    ---
    {resume_text}
    ---
    
    **JOB DESCRIPTION:**
    ---
    {job_description}
    ---

    Your output MUST be a single JSON object that conforms to the following schema:
    {{
        "match_score": integer,
        "missing_skills": list of strings,
        "actionable_suggestions": list of strings,
        "keyword_match": list of strings
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You are a Resume Analyst who returns only a single, valid JSON object."},
                {"role": "user", "content": prompt}
            ],
            # Use JSON mode for reliable structured output
            response_format={"type": "json_object"},
            temperature=0.2,
        )
        # The content of the response should be a JSON string
        return json.loads(response.choices[0].message.content)
    
    except Exception as e:
        print(f"Error during AI analysis: {e}")
        return {"error": f"Failed to get analysis from AI: {str(e)}"}

# --- Resume Rewrite Function ---

def rewrite_with_ai(resume_text: str) -> Dict[str, str]:
    """
    Rewrites a section of a resume for improved impact.
    Returns a dictionary containing the rewritten text (or an error dictionary).
    """
    if not client or not GROQ_MODEL:
        return {"error": "AI service not available. Check GROQ_API_KEY."}

    prompt = f"""
    You are an expert Resume Editor. Your task is to rewrite the provided resume text to be more powerful, action-oriented, and results-focused.
    
    * Start sentences with strong action verbs.
    * Quantify achievements with numbers where appropriate (e.g., "Increased sales by 15%").
    * Remove weak or passive language.
    * Maintain the original meaning and context.
    
    **ORIGINAL RESUME TEXT:**
    ---
    {resume_text}
    ---
    
    Provide only the rewritten text, and ensure the output is a single string.
    """

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You are a professional resume writer who provides only the rewritten text."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        # Return the rewritten text as a single string inside a dict
        return {"rewritten_text": response.choices[0].message.content}
        
    except Exception as e:
        print(f"Error during AI rewrite: {e}")
        return {"error": f"Failed to rewrite text with AI: {str(e)}"}