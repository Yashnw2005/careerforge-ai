import json
from pathlib import Path

from app.services.role_recommender import recommend_roles


DATASET_FILE = (
    Path(__file__).resolve().parent
    / "datasets"
    / "role_validation.json"
)


def load_validation_dataset() -> list[dict]:
    """Load the independent validation dataset."""
    with open(
        DATASET_FILE,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def evaluate_validation_set() -> None:
    """
    Evaluate role recommendations on the
    independent validation dataset.
    """
    dataset = load_validation_dataset()

    total_candidates = len(dataset)

    top_1_correct = 0
    top_3_correct = 0

    reciprocal_ranks = []
    preferred_role_ranks = []

    print("\nCareerForge Role Recommendation Validation")
    print("=" * 75)

    for candidate in dataset:

        recommendations = recommend_roles(
            candidate_skills=candidate["skills"],
            candidate_profile=candidate["profile"],
        )

        expected_roles = candidate["expected_roles"]

        preferred_role = max(
            expected_roles,
            key=expected_roles.get,
        )

        predicted_roles = [
            recommendation["role"]
            for recommendation in recommendations
        ]

        # --------------------------------------------------
        # Top-1 evaluation
        # --------------------------------------------------

        top_1_prediction = predicted_roles[0]

        top_1_match = (
            top_1_prediction == preferred_role
        )

        if top_1_match:
            top_1_correct += 1

        # --------------------------------------------------
        # Top-3 evaluation
        # --------------------------------------------------

        top_3_match = any(
            role in expected_roles
            for role in predicted_roles[:3]
        )

        if top_3_match:
            top_3_correct += 1

        # --------------------------------------------------
        # MRR
        # --------------------------------------------------

        reciprocal_rank = 0.0

        for rank, role in enumerate(
            predicted_roles,
            start=1,
        ):
            if role in expected_roles:
                reciprocal_rank = 1 / rank
                break

        reciprocal_ranks.append(
            reciprocal_rank
        )

        # --------------------------------------------------
        # Preferred-role rank
        # --------------------------------------------------

        preferred_rank = None

        for rank, role in enumerate(
            predicted_roles,
            start=1,
        ):
            if role == preferred_role:
                preferred_rank = rank
                break

        if preferred_rank is not None:
            preferred_role_ranks.append(
                preferred_rank
            )

        # --------------------------------------------------
        # Candidate output
        # --------------------------------------------------

        print(
            f"\n{candidate['candidate_id']}"
        )

        expected_display = ", ".join(
            f"{role} (priority {priority})"
            for role, priority
            in expected_roles.items()
        )

        print(
            f"Expected roles: "
            f"{expected_display}"
        )

        print(
            f"Preferred role: "
            f"{preferred_role}"
        )

        print("\nPredicted ranking:")

        for rank, recommendation in enumerate(
            recommendations,
            start=1,
        ):
            print(
                f"  {rank}. "
                f"{recommendation['role']} "
                f"— "
                f"{recommendation['match_percentage']:.2f}% "
                f"(skills: "
                f"{recommendation['skill_match_percentage']:.2f}%, "
                f"semantic: "
                f"{recommendation['semantic_match_percentage']:.2f}%)"
            )

        print(
            f"\nTop-1: "
            f"{'PASS' if top_1_match else 'FAIL'}"
        )

        print(
            f"Top-3: "
            f"{'PASS' if top_3_match else 'FAIL'}"
        )

        print(
            f"Preferred role rank: "
            f"{preferred_rank}"
            if preferred_rank is not None
            else "Preferred role rank: N/A"
        )

    # ------------------------------------------------------
    # Aggregate metrics
    # ------------------------------------------------------

    top_1_accuracy = (
        top_1_correct / total_candidates
    ) * 100

    top_3_recall = (
        top_3_correct / total_candidates
    ) * 100

    mean_reciprocal_rank = (
        sum(reciprocal_ranks)
        / total_candidates
    )

    average_preferred_rank = (
        sum(preferred_role_ranks)
        / len(preferred_role_ranks)
        if preferred_role_ranks
        else 0
    )

    # ------------------------------------------------------
    # Final report
    # ------------------------------------------------------

    print("\n" + "=" * 75)
    print("Validation Summary")
    print("=" * 75)

    print(
        f"Candidates evaluated: "
        f"{total_candidates}"
    )

    print(
        f"Top-1 Accuracy: "
        f"{top_1_accuracy:.2f}%"
    )

    print(
        f"Top-3 Recall: "
        f"{top_3_recall:.2f}%"
    )

    print(
        f"Mean Reciprocal Rank (MRR): "
        f"{mean_reciprocal_rank:.4f}"
    )

    print(
        f"Average Preferred Role Rank: "
        f"{average_preferred_rank:.2f}"
    )


if __name__ == "__main__":
    evaluate_validation_set()