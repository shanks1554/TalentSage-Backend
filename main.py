from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from agents.fit_evaluator import evaluate_fit
from utils.pdf_reader import extract_text_from_pdf
from typing import Union

app = FastAPI()

# Allow frontend requests (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Health check endpoint
@app.get("/ping")
async def ping():
    return JSONResponse(content={"status": "ok"})

# ✅ Resume evaluation endpoint
@app.post("/evaluate")
async def evaluate_resume(
    resume: UploadFile = File(...),
    position: Union[str, None] = Form(default=None),
):
    resume_text = extract_text_from_pdf(await resume.read())

    jd_text = (
        f"This is a job opening for the position of {position}. The ideal candidate should have relevant skills, experience, and qualifications."
        if position else
        "This is a generic job description. The candidate should have suitable qualifications and skills."
    )

    result = evaluate_fit(resume_text, jd_text)
    return result
