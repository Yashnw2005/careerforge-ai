from app.services.pdf_extractor import extract_text_from_pdf
from app.services.skill_extractor import extract_skills
from app.services.job_matcher import calculate_match_score


def analyze_resume_against_job(
    pdf_path: str,
    job_description: str,
    required_skills: list[str],
) -> dict:
    """
    Analyze a resume PDF against a job description.
    """

    # 1. Extract resume text from PDF
    resume_text = extract_text_from_pdf(pdf_path)

    # 2. Extract skills from resume
    resume_skills = extract_skills(resume_text)

    # 3. Calculate resume-job match
    match_result = calculate_match_score(
        resume_text=resume_text,
        job_description=job_description,
        resume_skills=resume_skills,
        required_skills=required_skills,
    )

    return {
        "resume_text_length": len(resume_text),
        "resume_skills": resume_skills,
        **match_result,
    }