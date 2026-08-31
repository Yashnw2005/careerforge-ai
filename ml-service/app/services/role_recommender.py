from typing import Any


# Initial role-skill knowledge base.
# We will expand and refine this later using real job-market data.
ROLE_DATABASE: dict[str, dict[str, Any]] = {
    "Full Stack Developer": {
        "category": "Software Development",
        "skills": {
            "javascript": 3,
            "typescript": 2,
            "react": 3,
            "node.js": 3,
            "express": 2,
            "mongodb": 2,
            "sql": 2,
            "git": 1,
            "github": 1,
            "docker": 1,
        },
    },

    "Backend Developer": {
        "category": "Software Development",
        "skills": {
            "python": 3,
            "java": 3,
            "node.js": 3,
            "express": 2,
            "fastapi": 2,
            "django": 2,
            "mongodb": 2,
            "mysql": 2,
            "postgresql": 2,
            "sql": 3,
            "git": 1,
            "docker": 1,
        },
    },

    "Frontend Developer": {
        "category": "Software Development",
        "skills": {
            "javascript": 3,
            "typescript": 3,
            "react": 3,
            "git": 1,
            "github": 1,
        },
    },

    "DevOps Engineer": {
        "category": "Cloud & DevOps",
        "skills": {
            "linux": 3,
            "docker": 3,
            "kubernetes": 3,
            "aws": 3,
            "azure": 2,
            "google cloud": 2,
            "git": 1,
            "github": 1,
        },
    },

    "Cloud Engineer": {
        "category": "Cloud & DevOps",
        "skills": {
            "linux": 3,
            "aws": 3,
            "azure": 3,
            "google cloud": 3,
            "docker": 2,
            "kubernetes": 2,
            "git": 1,
        },
    },

    "Machine Learning Engineer": {
        "category": "Artificial Intelligence",
        "skills": {
            "python": 3,
            "machine learning": 3,
            "scikit-learn": 3,
            "pandas": 2,
            "numpy": 2,
            "tensorflow": 2,
            "pytorch": 2,
            "git": 1,
            "docker": 1,
        },
    },

    "Data Scientist": {
        "category": "Data Science",
        "skills": {
            "python": 3,
            "sql": 3,
            "machine learning": 3,
            "pandas": 3,
            "numpy": 2,
            "scikit-learn": 2,
            "statistics": 3,
            "data visualization": 2,
        },
    },

    "AI Engineer": {
        "category": "Artificial Intelligence",
        "skills": {
            "python": 3,
            "machine learning": 3,
            "deep learning": 3,
            "natural language processing": 3,
            "pytorch": 3,
            "tensorflow": 2,
            "docker": 1,
            "git": 1,
        },
    },
}


def calculate_role_match(
    candidate_skills: list[str],
    role_skills: dict[str, int],
) -> dict:
    """
    Calculate a weighted candidate-role match.

    Higher-weight skills contribute more to the score.
    """

    candidate_skill_set = {
        skill.lower().strip()
        for skill in candidate_skills
    }

    matched_skills = sorted(
        skill
        for skill in role_skills
        if skill in candidate_skill_set
    )

    missing_skills = sorted(
        skill
        for skill in role_skills
        if skill not in candidate_skill_set
    )

    total_weight = sum(role_skills.values())

    matched_weight = sum(
        role_skills[skill]
        for skill in matched_skills
    )

    if total_weight:
        match_percentage = (
            matched_weight / total_weight
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
        "matched_weight": matched_weight,
        "total_weight": total_weight,
    }

def recommend_roles(
    candidate_skills: list[str],
) -> list[dict]:
    """
    Recommend career roles using weighted skill matching.
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