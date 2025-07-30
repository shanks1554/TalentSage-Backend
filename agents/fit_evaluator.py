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
You are a hiring assistant AI. Given a resume and a job description, evaluate the candidate on the following:

1. Does the candidate match the position?
2. What are the strengths?
3. What improvements are needed?

Please avoid vague suggestions, placeholder values like "X%" or "Y%", or hypothetical examples such as "for example...".
Only provide actionable feedback based on the actual content.

Respond only in valid JSON with the following keys:
- decision: "yes" or "no"
- suggestions: a list of concise improvement points
- summary: a short summary of the evaluation

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
