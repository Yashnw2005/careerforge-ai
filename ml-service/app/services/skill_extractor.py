import re


# Initial CareerForge skill dictionary.
# We will expand this substantially later.
SKILL_DATABASE = [
    "python",
    "java",
    "javascript",
    "typescript",
    "c++",
    "react",
    "node.js",
    "express",
    "fastapi",
    "django",
    "flask",
    "mongodb",
    "mysql",
    "postgresql",
    "sql",
    "git",
    "github",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "google cloud",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "natural language processing",
    "nlp",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "pandas",
    "numpy",
]


def normalize_text(text: str) -> str:
    """Normalize resume text for easier matching."""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_skills(text: str) -> list[str]:
    """Extract known technical skills from resume text."""

    normalized_text = normalize_text(text)

    found_skills = []

    for skill in SKILL_DATABASE:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, normalized_text):
            found_skills.append(skill)

    return sorted(found_skills)