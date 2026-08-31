from typing import Any


# Initial role-skill knowledge base.
# We will expand and refine this later using real job-market data.
ROLE_DATABASE: dict[str, dict[str, Any]] = {
    "Full Stack Developer": {
        "category": "Software Development",
        "skills": [
            "javascript",
            "typescript",
            "react",
            "node.js",
            "express",
            "mongodb",
            "sql",
            "git",
            "github",
            "docker",
        ],
    },

    "Backend Developer": {
        "category": "Software Development",
        "skills": [
            "python",
            "java",
            "node.js",
            "express",
            "fastapi",
            "django",
            "mongodb",
            "mysql",
            "postgresql",
            "sql",
            "git",
            "docker",
        ],
    },

    "Frontend Developer": {
        "category": "Software Development",
        "skills": [
            "javascript",
            "typescript",
            "react",
            "git",
            "github",
        ],
    },

    "DevOps Engineer": {
        "category": "Cloud & DevOps",
        "skills": [
            "linux",
            "git",
            "github",
            "docker",
            "kubernetes",
            "aws",
            "azure",
            "google cloud",
        ],
    },

    "Cloud Engineer": {
        "category": "Cloud & DevOps",
        "skills": [
            "linux",
            "docker",
            "kubernetes",
            "aws",
            "azure",
            "google cloud",
            "git",
        ],
    },

    "Machine Learning Engineer": {
        "category": "Artificial Intelligence",
        "skills": [
            "python",
            "machine learning",
            "scikit-learn",
            "pandas",
            "numpy",
            "tensorflow",
            "pytorch",
            "git",
            "docker",
        ],
    },

    "Data Scientist": {
        "category": "Data Science",
        "skills": [
            "python",
            "sql",
            "machine learning",
            "pandas",
            "numpy",
            "scikit-learn",
            "statistics",
            "data visualization",
        ],
    },

    "AI Engineer": {
        "category": "Artificial Intelligence",
        "skills": [
            "python",
            "machine learning",
            "deep learning",
            "natural language processing",
            "pytorch",
            "tensorflow",
            "docker",
            "git",
        ],
    },
}


def calculate_role_match(
    candidate_skills: list[str],
    role_skills: list[str],
) -> dict:
    """
    Calculate how well a candidate's skills match a career role.
    """

    candidate_skill_set = {
        skill.lower().strip()
        for skill in candidate_skills
    }

    role_skill_set = {
        skill.lower().strip()
        for skill in role_skills
    }

    matched_skills = sorted(
        candidate_skill_set & role_skill_set
    )

    missing_skills = sorted(
        role_skill_set - candidate_skill_set
    )

    if role_skill_set:
        match_percentage = (
            len(matched_skills)
            / len(role_skill_set)
        ) * 100
    else:
        match_percentage = 0

    return {
        "match_percentage": round(
            match_percentage,
            2,
        ),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
    }


def recommend_roles(
    candidate_skills: list[str],
) -> list[dict]:
    """
    Recommend career roles based on candidate skills.
    """

    recommendations = []

    for role_name, role_data in ROLE_DATABASE.items():

        match = calculate_role_match(
            candidate_skills=candidate_skills,
            role_skills=role_data["skills"],
        )

        recommendations.append(
            {
                "role": role_name,
                "category": role_data["category"],
                "match_percentage": match[
                    "match_percentage"
                ],
                "matched_skills": match[
                    "matched_skills"
                ],
                "missing_skills": match[
                    "missing_skills"
                ],
            }
        )

    recommendations.sort(
        key=lambda role: role["match_percentage"],
        reverse=True,
    )

    return recommendations