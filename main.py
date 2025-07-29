from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from agents.fit_evaluator import evaluate_fit
from utils.pdf_reader import extract_text_from_pdf
from typing import Union

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
    position: Union[str, None] = Form(default=None),
):
    # Extract text from resume
    resume_text = extract_text_from_pdf(await resume.read())

    # If position is provided, use it to generate a simple JD
    if position:
        jd_text = f"This is a job opening for the position of {position}. The ideal candidate should have relevant skills, experience, and qualifications."
    else:
        jd_text = "This is a generic job description. The candidate should have suitable qualifications and skills."

    # Evaluate resume fit
    result = evaluate_fit(resume_text, jd_text)
    return result
