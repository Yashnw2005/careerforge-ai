import json
from pathlib import Path
from typing import Any
from app.services.semantic_matcher import calculate_semantic_similarity

DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "role_skills.json"
)


def load_role_database() -> dict[str, dict[str, Any]]:
    """
    Load career role definitions from the JSON dataset.
    """

    with open(
        DATA_FILE,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)
    

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

def calculate_role_semantic_match(
    candidate_profile: str,
    role_description: str,
) -> float:
    """
    Calculate semantic similarity between the candidate
    profile and a career role description.
    """

    return calculate_semantic_similarity(
        candidate_profile,
        role_description,
    )
    
def recommend_roles(
    candidate_skills: list[str],
    candidate_profile: str = "",
) -> list[dict]:
    """
    Recommend career roles using weighted skill matching
    and semantic similarity.
    """

    role_database = load_role_database()

    recommendations = []

    for role_name, role_data in role_database.items():

        # Weighted skill matching
        match = calculate_role_match(
            candidate_skills=candidate_skills,
            role_skills=role_data["skills"],
        )

        # Semantic matching
        semantic_similarity = 0.0

        if candidate_profile.strip():
            semantic_similarity = calculate_role_semantic_match(
                candidate_profile,
                role_data["description"],
            )

        semantic_match_percentage = round(
            semantic_similarity * 100,
            2,
        )

        # Combine the two signals
        skill_score = match["match_percentage"]

        if candidate_profile.strip():
            final_score = (
                (skill_score * 0.70)
                + (semantic_match_percentage * 0.30)
            )
        else:
            final_score = skill_score

        recommendations.append(
            {
                "role": role_name,
                "category": role_data["category"],
                "match_percentage": round(
                    final_score,
                    2,
                ),
                "skill_match_percentage": skill_score,
                "semantic_match_percentage": (
                    semantic_match_percentage
                ),
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