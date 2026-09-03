from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.services.semantic_matcher import calculate_semantic_similarity


def calculate_text_similarity(
    resume_text: str,
    job_description: str,
) -> float:
    """
    Calculate similarity between a resume and job description
    using TF-IDF and cosine similarity.
    """

    documents = [
        resume_text,
        job_description,
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(
        documents
    )

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2],
    )[0][0]

    return round(float(similarity), 4)


def calculate_skill_match(
    resume_skills: list[str],
    required_skills: list[str],
) -> dict:
    """
    Compare candidate skills with required job skills.
    """

    resume_skill_set = {
        skill.lower().strip()
        for skill in resume_skills
    }

    required_skill_set = {
        skill.lower().strip()
        for skill in required_skills
    }

    matched_skills = sorted(
        resume_skill_set & required_skill_set
    )

    missing_skills = sorted(
        required_skill_set - resume_skill_set
    )

    if required_skill_set:
        skill_match_percentage = (
            len(matched_skills)
            / len(required_skill_set)
        ) * 100
    else:
        skill_match_percentage = 0

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_match_percentage": round(
            skill_match_percentage,
            2,
        ),
    }


def calculate_match_score(
    resume_text: str,
    job_description: str,
    resume_skills: list[str],
    required_skills: list[str],
) -> dict:
    """
    Calculate the overall candidate-job match
    using skill, TF-IDF, and semantic similarity.
    """

    # 1. TF-IDF similarity
    text_similarity = calculate_text_similarity(
        resume_text,
        job_description,
    )

    # 2. Explicit skill matching
    skill_analysis = calculate_skill_match(
        resume_skills,
        required_skills,
    )

    # 3. Semantic similarity
    semantic_similarity = calculate_semantic_similarity(
        resume_text,
        job_description,
    )

    text_score = text_similarity * 100
    semantic_score = semantic_similarity * 100
    skill_score = skill_analysis[
        "skill_match_percentage"
    ]

    # Initial explainable weighting
    overall_score = (
        (skill_score * 0.50)
        + (semantic_score * 0.30)
        + (text_score * 0.20)
    )

    return {
        "overall_match_percentage": round(
            overall_score,
            2,
        ),
        "text_similarity": text_similarity,
        "semantic_similarity": semantic_similarity,
        "skill_match_percentage": skill_score,
        "matched_skills": skill_analysis[
            "matched_skills"
        ],
        "missing_skills": skill_analysis[
            "missing_skills"
        ],
    }