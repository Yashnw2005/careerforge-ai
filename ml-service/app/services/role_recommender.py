import json
from pathlib import Path
from typing import Any

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

def recommend_roles(
    candidate_skills: list[str],
) -> list[dict]:
    """
    Recommend career roles using the role dataset
    and weighted skill matching.
    """

    role_database = load_role_database()

    recommendations = []

    for role_name, role_data in role_database.items():

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