"""
AI-Powered Resume Shortlisting Tool
------------------------------------
A Flask web application that automatically ranks and shortlists resumes
against a given Job Description using NLP (TF-IDF + Cosine Similarity)
and rule-based skill/keyword extraction.

Author: Your Name
"""

import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, session

from resume_parser import extract_text_from_file, extract_candidate_info
from matcher import rank_resumes

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

app = Flask(__name__)
app.secret_key = "change-this-secret-key-in-production"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024  # 25 MB total upload limit

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    job_description = request.form.get("job_description", "").strip()
    min_experience = request.form.get("min_experience", "").strip()
    required_skills_raw = request.form.get("required_skills", "").strip()
    shortlist_threshold = request.form.get("threshold", "50").strip()

    if not job_description:
        flash("Job description is required.", "danger")
        return redirect(url_for("index"))

    files = request.files.getlist("resumes")
    if not files or files[0].filename == "":
        flash("Please upload at least one resume.", "danger")
        return redirect(url_for("index"))

    try:
        threshold = float(shortlist_threshold)
    except ValueError:
        threshold = 50.0

    required_skills = [
        s.strip() for s in required_skills_raw.split(",") if s.strip()
    ]

    candidates = []
    session_id = str(uuid.uuid4())[:8]
    session_folder = os.path.join(app.config["UPLOAD_FOLDER"], session_id)
    os.makedirs(session_folder, exist_ok=True)

    for file in files:
        if file and allowed_file(file.filename):
            safe_name = f"{uuid.uuid4().hex[:8]}_{file.filename}"
            filepath = os.path.join(session_folder, safe_name)
            file.save(filepath)

            text = extract_text_from_file(filepath)
            if not text.strip():
                continue

            info = extract_candidate_info(text, original_filename=file.filename)
            candidates.append(info)

    if not candidates:
        flash("Could not extract text from any uploaded resume. "
              "Please upload valid PDF, DOCX or TXT files.", "danger")
        return redirect(url_for("index"))

    ranked = rank_resumes(
        job_description=job_description,
        candidates=candidates,
        required_skills=required_skills,
    )

    for c in ranked:
        c["shortlisted"] = c["match_score"] >= threshold

    ranked.sort(key=lambda x: x["match_score"], reverse=True)

    return render_template(
        "results.html",
        candidates=ranked,
        job_description=job_description,
        threshold=threshold,
        required_skills=required_skills,
        total=len(ranked),
        shortlisted_count=sum(1 for c in ranked if c["shortlisted"]),
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
