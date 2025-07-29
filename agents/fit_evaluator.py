import google.generativeai as genai
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-pro")

def extract_json(text: str) -> dict:
    clean = re.sub(r"```json|```", "", text).strip()
    return json.loads(clean)

def evaluate_fit(resume_text: str, job_description: str) -> dict:
    prompt = f"""
You are a hiring assistant AI. Given a resume and a job description, evaluate:

1. Does the candidate match the position?
2. What are the strengths?
3. What improvements are needed?

Respond in JSON with keys: decision (yes/no), suggestions, summary.

Resume:
\"\"\"
{resume_text}
\"\"\"

Job Description:
\"\"\"
{job_description}
\"\"\"
"""
    response = model.generate_content(prompt)
    return extract_json(response.text)
