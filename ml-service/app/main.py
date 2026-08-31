from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import tempfile
import os

from app.services.skill_extractor import extract_skills
from app.services.pdf_extractor import extract_text_from_pdf


app = FastAPI(
    title="CareerForge AI ML Service",
    description="AI and Data Science engine for CareerForge AI",
    version="1.0.0",
)


class SkillExtractionRequest(BaseModel):
    text: str


@app.get("/")
def root():
    return {
        "success": True,
        "message": "CareerForge AI ML service is running",
    }


@app.get("/health")
def health():
    return {
        "success": True,
        "service": "ml-service",
        "status": "healthy",
    }


@app.post("/api/extract-skills")
def extract_resume_skills(request: SkillExtractionRequest):
    skills = extract_skills(request.text)

    return {
        "success": True,
        "skills": skills,
        "count": len(skills),
    }

@app.post("/api/analyze-resume")
async def analyze_resume(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        return {
            "success": False,
            "message": "Only PDF files are supported.",
        }

    file_content = await file.read()

    temporary_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf",
    )

    try:
        temporary_file.write(file_content)
        temporary_file.close()

        extracted_text = extract_text_from_pdf(
            temporary_file.name
        )

        skills = extract_skills(extracted_text)

        return {
            "success": True,
            "filename": file.filename,
            "text_length": len(extracted_text),
            "skills": skills,
            "skill_count": len(skills),
        }

    finally:
        os.unlink(temporary_file.name)