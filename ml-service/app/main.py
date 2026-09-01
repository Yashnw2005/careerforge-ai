from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
import tempfile
import os

from app.services.skill_extractor import extract_skills
from app.services.pdf_extractor import extract_text_from_pdf
from app.services.job_matcher import calculate_match_score
from app.services.resume_analyzer import analyze_resume_against_job
from app.services.skill_gap import analyze_skill_gaps
from app.services.semantic_matcher import calculate_semantic_similarity
from app.services.role_recommender import recommend_roles

app = FastAPI(
    title="CareerForge AI ML Service",
    description="AI and Data Science engine for CareerForge AI",
    version="1.0.0",
)


class SkillExtractionRequest(BaseModel):
    text: str
    

class JobMatchRequest(BaseModel):
    resume_text: str
    job_description: str
    resume_skills: list[str]
    required_skills: list[str]

class SemanticMatchRequest(BaseModel):
    resume_text: str
    job_description: str
    
class RoleRecommendationRequest(BaseModel):
    candidate_skills: list[str]
    candidate_profile: str = ""
    
    
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
        
@app.post("/api/match-job")
def match_job(request: JobMatchRequest):
    result = calculate_match_score(
        resume_text=request.resume_text,
        job_description=request.job_description,
        resume_skills=request.resume_skills,
        required_skills=request.required_skills,
    )

    return {
        "success": True,
        **result,
    }
    
@app.post("/api/analyze-resume-job")
async def analyze_resume_job(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    required_skills: str = Form(...),
):
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

        skills = [
            skill.strip()
            for skill in required_skills.split(",")
            if skill.strip()
        ]

        result = analyze_resume_against_job(
            pdf_path=temporary_file.name,
            job_description=job_description,
            required_skills=skills,
        )

        return {
            "success": True,
            "filename": file.filename,
            "job_required_skills": skills,
            **result,
        }

    finally:
        os.unlink(temporary_file.name)

@app.post("/api/analyze-skill-gap")
def analyze_skill_gap(skills: list[str]):
    recommendations = analyze_skill_gaps(skills)

    return {
        "success": True,
        "skill_gaps": recommendations,
    }
    
@app.post("/api/semantic-match")
def semantic_match(request: SemanticMatchRequest):
    similarity = calculate_semantic_similarity(
        resume_text=request.resume_text,
        job_description=request.job_description,
    )

    return {
        "success": True,
        "semantic_similarity": similarity,
        "semantic_match_percentage": round(
            similarity * 100,
            2,
        ),
    }

@app.post("/api/recommend-roles")
def recommend_career_roles(
    request: RoleRecommendationRequest,
):
    recommendations = recommend_roles(
        candidate_skills=request.candidate_skills,
        candidate_profile=request.candidate_profile,
    )

    return {
        "success": True,
        "recommendations": recommendations,
    }
    
 