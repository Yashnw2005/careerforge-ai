from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_text_similarity(
    resume_text: str,
    job_description: str,
) -> float:
    """
    Calculate similarity between a resume and job description
    using TF-IDF and cosine similarity.
    """

    documents = [resume_text, job_description]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

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
        skill.lower()
        for skill in resume_skills
    }

    required_skill_set = {
        skill.lower()
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
    Calculate the overall candidate-job match.
    """

    text_similarity = calculate_text_similarity(
        resume_text,
        job_description,
    )

    skill_analysis = calculate_skill_match(
        resume_skills,
        required_skills,
    )

    text_score = text_similarity * 100
    skill_score = skill_analysis[
        "skill_match_percentage"
    ]

    overall_score = (
        (text_score * 0.4)
        + (skill_score * 0.6)
    )

    return {
        "overall_match_percentage": round(
            overall_score,
            2,
        ),
        "text_similarity": round(
            text_similarity,
            4,
        ),
        "skill_match_percentage": skill_score,
        "matched_skills": skill_analysis[
            "matched_skills"
        ],
        "missing_skills": skill_analysis[
            "missing_skills"
        ],
    }