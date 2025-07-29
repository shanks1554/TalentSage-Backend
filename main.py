from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from agents.fit_evaluator import evaluate_fit
from utils.pdf_reader import extract_text_from_pdf
from typing import Optional

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/evaluate")
async def evaluate_resume(
    resume: UploadFile = File(...),
    jd_file: Optional[UploadFile] = File(default=None),
    jd_text: Optional[str] = Form( default=None),
    position: Optional[str] = Form(default=None),
):
    resume_text = extract_text_from_pdf(await resume.read())

    # Job description logic
    if jd_file:
        jd_text = extract_text_from_pdf(await jd_file.read())
    elif not jd_text and position:
        jd_text = f"This is a job opening for the position of {position}."
    elif not jd_text:
        return {"error": "No job description or position provided."}

    result = evaluate_fit(resume_text, jd_text)
    return result
