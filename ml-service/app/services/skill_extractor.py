import re


# Canonical CareerForge skill dictionary.
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
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "pandas",
    "numpy",
]


# Common aliases mapped to canonical CareerForge skills.
SKILL_ALIASES = {
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "nlp": "natural language processing",
    "reactjs": "react",
    "react.js": "react",
    "nodejs": "node.js",
    "node js": "node.js",
    "scikit learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "gcp": "google cloud",
}


def normalize_text(text: str) -> str:
    """
    Normalize resume text for easier matching.
    """

    text = text.lower()
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_skills(text: str) -> list[str]:
    """
    Extract known technical skills from resume text.

    Detected aliases are normalized to canonical
    CareerForge skill names.
    """

    normalized_text = normalize_text(text)

    found_skills = set()

    # Match canonical skills.
    for skill in SKILL_DATABASE:
        pattern = (
            r"(?<!\w)"
            + re.escape(skill)
            + r"(?!\w)"
        )

        if re.search(pattern, normalized_text):
            found_skills.add(skill)

    # Match aliases and convert them to canonical names.
    for alias, canonical_skill in SKILL_ALIASES.items():
        pattern = (
            r"(?<!\w)"
            + re.escape(alias)
            + r"(?!\w)"
        )

        if re.search(pattern, normalized_text):
            found_skills.add(canonical_skill)

    return sorted(found_skills)