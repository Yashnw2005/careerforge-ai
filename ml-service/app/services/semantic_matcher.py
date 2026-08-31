from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load the embedding model once when the service starts.
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_semantic_similarity(
    resume_text: str,
    job_description: str,
) -> float:
    """
    Calculate semantic similarity between a resume
    and a job description using sentence embeddings.
    """

    embeddings = model.encode(
        [resume_text, job_description]
    )

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]],
    )[0][0]

    return round(float(similarity), 4)