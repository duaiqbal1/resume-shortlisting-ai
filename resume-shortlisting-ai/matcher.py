"""
matcher.py
----------
Core matching engine that scores each resume against a job description.

Scoring is a weighted combination of:
  1. TF-IDF + Cosine Similarity between resume text and job description (70%)
  2. Required-skill coverage: how many of the explicitly required skills
     appear in the resume (30%)

This keeps the tool fully offline / free (no external AI API needed),
while still giving genuinely useful, explainable ranking.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def _text_similarity_scores(job_description: str, resume_texts: list) -> list:
    """Return cosine similarity (0-100) of each resume against the JD."""
    corpus = [job_description] + resume_texts
    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    tfidf_matrix = vectorizer.fit_transform(corpus)

    jd_vector = tfidf_matrix[0:1]
    resume_vectors = tfidf_matrix[1:]

    similarities = cosine_similarity(jd_vector, resume_vectors)[0]
    return [round(float(score) * 100, 2) for score in similarities]


def _skill_coverage(required_skills: list, candidate_skills: list) -> tuple:
    """Return (coverage_percent, matched_skills, missing_skills)."""
    if not required_skills:
        return 100.0, [], []

    candidate_skills_lower = {s.lower() for s in candidate_skills}
    required_lower = [s.lower() for s in required_skills]

    matched = [s for s in required_skills if s.lower() in candidate_skills_lower]
    missing = [s for s in required_skills if s.lower() not in candidate_skills_lower]

    coverage = (len(matched) / len(required_lower)) * 100
    return round(coverage, 2), matched, missing


def rank_resumes(job_description: str, candidates: list, required_skills: list) -> list:
    """
    candidates: list of dicts from resume_parser.extract_candidate_info
    Returns the same list with added keys:
        - text_similarity (float)
        - skill_coverage (float)
        - matched_skills (list)
        - missing_skills (list)
        - match_score (float)  -- final weighted score 0-100
    """
    resume_texts = [c["raw_text"] for c in candidates]
    similarity_scores = _text_similarity_scores(job_description, resume_texts)

    TEXT_WEIGHT = 0.70
    SKILL_WEIGHT = 0.30

    for candidate, sim_score in zip(candidates, similarity_scores):
        coverage, matched, missing = _skill_coverage(
            required_skills, candidate["skills"]
        )

        final_score = (sim_score * TEXT_WEIGHT) + (coverage * SKILL_WEIGHT)

        candidate["text_similarity"] = sim_score
        candidate["skill_coverage"] = coverage
        candidate["matched_skills"] = matched
        candidate["missing_skills"] = missing
        candidate["match_score"] = round(final_score, 2)

        # raw_text is large; drop it before sending to the template
        candidate.pop("raw_text", None)

    return candidates
