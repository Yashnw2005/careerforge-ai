from typing import Literal


SkillPriority = Literal["high", "medium", "low"]


# Skill metadata used to generate explainable
# career-learning recommendations.
SKILL_METADATA = {
    "python": {
        "priority": "high",
        "category": "programming",
        "reason": (
            "Python is widely used in software development, "
            "data science, and AI."
        ),
        "prerequisites": [],
        "learning_topics": [
            "Python fundamentals",
            "Object-oriented programming",
            "APIs and backend development",
        ],
    },
    "docker": {
        "priority": "high",
        "category": "devops",
        "reason": (
            "Docker is commonly required for "
            "containerized application development."
        ),
        "prerequisites": [],
        "learning_topics": [
            "Images and containers",
            "Dockerfiles",
            "Docker Compose",
        ],
    },
    "kubernetes": {
        "priority": "high",
        "category": "devops",
        "reason": (
            "Kubernetes is required for container "
            "orchestration and scalable deployments."
        ),
        "prerequisites": [
            "docker",
        ],
        "learning_topics": [
            "Pods",
            "Deployments",
            "Services",
            "ConfigMaps and Secrets",
            "Helm",
        ],
    },
    "aws": {
        "priority": "high",
        "category": "cloud",
        "reason": (
            "AWS skills are frequently required for "
            "cloud-based application deployment."
        ),
        "prerequisites": [
            "docker",
        ],
        "learning_topics": [
            "EC2",
            "S3",
            "IAM",
            "VPC fundamentals",
        ],
    },
    "sql": {
        "priority": "medium",
        "category": "database",
        "reason": (
            "SQL is important for querying and "
            "managing relational databases."
        ),
        "prerequisites": [],
        "learning_topics": [
            "SELECT queries",
            "JOIN operations",
            "Aggregation",
            "Database design",
        ],
    },
    "react": {
        "priority": "medium",
        "category": "frontend",
        "reason": (
            "React is widely used for modern "
            "web application interfaces."
        ),
        "prerequisites": [
            "javascript",
        ],
        "learning_topics": [
            "Components",
            "Props and state",
            "Hooks",
            "API integration",
        ],
    },
}


def analyze_skill_gaps(
    missing_skills: list[str],
) -> list[dict]:
    """
    Analyze missing skills and generate
    learning recommendations.
    """

    recommendations = []

    for skill in missing_skills:
        normalized_skill = skill.lower().strip()

        metadata = SKILL_METADATA.get(
            normalized_skill
        )

        if metadata:
            recommendations.append(
                {
                    "skill": normalized_skill,
                    "priority": metadata["priority"],
                    "category": metadata["category"],
                    "reason": metadata["reason"],
                    "prerequisites": metadata[
                        "prerequisites"
                    ],
                    "learning_topics": metadata[
                        "learning_topics"
                    ],
                }
            )
        else:
            recommendations.append(
                {
                    "skill": normalized_skill,
                    "priority": "medium",
                    "category": "general",
                    "reason": (
                        "This skill is listed as required "
                        "by the target role."
                    ),
                    "prerequisites": [],
                    "learning_topics": [
                        f"{normalized_skill} fundamentals",
                        (
                            f"Practical "
                            f"{normalized_skill} projects"
                        ),
                    ],
                }
            )

    priority_order = {
        "high": 0,
        "medium": 1,
        "low": 2,
    }

    recommendations.sort(
        key=lambda item: priority_order[
            item["priority"]
        ]
    )

    return recommendations