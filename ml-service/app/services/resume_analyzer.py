from app.services.pdf_extractor import extract_text_from_pdf
from app.services.skill_extractor import extract_skills
from app.services.job_matcher import calculate_match_score
from app.services.skill_gap import analyze_skill_gaps
from app.services.role_recommender import recommend_roles

def analyze_resume_against_job(
    pdf_path: str,
    job_description: str,
    required_skills: list[str],
) -> dict:
    """
    Run the complete CareerForge resume intelligence pipeline.
    """

    # 1. Extract resume text
    resume_text = extract_text_from_pdf(pdf_path)

    # 2. Extract candidate skills
    resume_skills = extract_skills(resume_text)

    # 3. Calculate resume-job match
    match_result = calculate_match_score(
        resume_text=resume_text,
        job_description=job_description,
        resume_skills=resume_skills,
        required_skills=required_skills,
    )

    # 4. Analyze missing skills
    skill_gap = analyze_skill_gaps(
        match_result["missing_skills"]
    )
    
    # 5. Recommend suitable career roles
    career_recommendations = recommend_roles(
       candidate_skills=resume_skills,
       candidate_profile=resume_text,
)

    return {
        "resume_text_length": len(resume_text),
        "resume_skills": resume_skills,

        "overall_match_percentage": match_result[
            "overall_match_percentage"
        ],

        "text_similarity": match_result[
            "text_similarity"
        ],

        "semantic_similarity": match_result[
            "semantic_similarity"
        ],

        "skill_match_percentage": match_result[
            "skill_match_percentage"
        ],

        "matched_skills": match_result[
            "matched_skills"
        ],

        "missing_skills": match_result[
            "missing_skills"
        ],

        "skill_gap_analysis": skill_gap,
        
        "career_recommendations": career_recommendations,
    }