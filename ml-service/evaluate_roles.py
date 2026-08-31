import json
from pathlib import Path

from app.services.role_recommender import recommend_roles


DATASET_FILE = (
    Path(__file__).resolve().parent
    / "datasets"
    / "role_evaluation.json"
)


def load_evaluation_dataset() -> list[dict]:
    """Load the curated role evaluation dataset."""

    with open(
        DATASET_FILE,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def evaluate_role_recommendations() -> None:
    """Evaluate role recommendations against expected roles."""

    dataset = load_evaluation_dataset()

    total_candidates = len(dataset)
    top_1_correct = 0
    top_3_correct = 0

    print("\nCareerForge Role Recommendation Evaluation")
    print("=" * 60)

    for candidate in dataset:
        recommendations = recommend_roles(
            candidate["skills"]
        )

        predicted_roles = [
            recommendation["role"]
            for recommendation in recommendations
        ]

        expected_roles = candidate["expected_roles"]

        top_1_prediction = predicted_roles[0]

        top_1_match = (
            top_1_prediction in expected_roles
        )

        top_3_match = any(
            role in expected_roles
            for role in predicted_roles[:3]
        )

        if top_1_match:
            top_1_correct += 1

        if top_3_match:
            top_3_correct += 1

        print(
            f"\n{candidate['candidate_id']}"
        )

        print(
            f"Expected roles: {', '.join(expected_roles)}"
        )

        print(
            f"Predicted top role: {top_1_prediction}"
        )

        print(
            f"Top-1: {'PASS' if top_1_match else 'FAIL'}"
        )

        print(
            f"Top-3: {'PASS' if top_3_match else 'FAIL'}"
        )

    top_1_accuracy = (
        top_1_correct / total_candidates
    ) * 100

    top_3_recall = (
        top_3_correct / total_candidates
    ) * 100

    print("\n" + "=" * 60)
    print("Evaluation Summary")
    print("=" * 60)

    print(
        f"Candidates evaluated: {total_candidates}"
    )

    print(
        f"Top-1 Accuracy: {top_1_accuracy:.2f}%"
    )

    print(
        f"Top-3 Recall: {top_3_recall:.2f}%"
    )


if __name__ == "__main__":
    evaluate_role_recommendations()