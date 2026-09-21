# 🤖 AI-Powered Resume Shortlisting Tool

An intelligent web application that automatically **ranks and shortlists resumes**
against a given job description using **Natural Language Processing (TF-IDF +
Cosine Similarity)** combined with **rule-based skill extraction**.

Recruiters can upload dozens of resumes at once (PDF, DOCX or TXT), paste a
job description, optionally specify required skills, and instantly get a
ranked, color-coded shortlist — no manual screening required.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-black)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

- 📄 **Multi-format resume parsing** — PDF, DOCX and TXT support
- 🧠 **NLP-based matching** — TF-IDF vectorization + Cosine Similarity between resume and job description
- 🎯 **Skill extraction & coverage** — detects 60+ common technical/soft skills automatically
- 📊 **Weighted scoring engine** — 70% semantic text match + 30% required-skill coverage
- ✅ **Adjustable shortlisting threshold** — set your own cut-off score (0–100%)
- 📧 **Auto-extracted contact info** — email & phone number pulled via regex
- 🎨 **Clean, responsive web UI** — built with Flask + vanilla CSS (no heavy frontend framework needed)
- 🔒 **Fully offline** — no external AI API calls, no API keys, no cost, no data leaves your machine

---

## 🖼️ How It Works

1. Recruiter pastes the **Job Description** and (optionally) a comma-separated list of **required skills**.
2. Recruiter uploads multiple resumes at once.
3. The app extracts text from every resume (PDF/DOCX/TXT).
4. Each resume is converted into a TF-IDF vector and compared against the job description using cosine similarity.
5. Detected skills in each resume are compared against the required skills list.
6. A final **Match Score** is computed:

   ```
   match_score = (text_similarity * 0.70) + (skill_coverage * 0.30)
   ```

7. Candidates scoring above the chosen threshold are marked **✅ Shortlisted**, others **❌ Rejected**.
8. Results are displayed in a sortable, color-coded table.

---

## 🛠️ Tech Stack

| Layer          | Technology                          |
|----------------|--------------------------------------|
| Backend        | Python 3, Flask                     |
| NLP / ML       | scikit-learn (TF-IDF, Cosine Similarity) |
| Resume Parsing | pdfplumber, python-docx             |
| Frontend       | HTML5, CSS3, Jinja2 templates       |

---

## 📂 Project Structure

```
resume-shortlisting-ai/
├── app.py                     # Flask application & routes
├── resume_parser.py           # Text extraction + candidate info parsing
├── matcher.py                 # TF-IDF ranking / scoring engine
├── requirements.txt           # Python dependencies
├── templates/
│   ├── index.html             # Upload / input form
│   └── results.html           # Ranked results page
├── static/
│   └── style.css              # App styling
├── sample_data/
│   └── sample_job_description.txt
├── uploads/                   # Runtime storage for uploaded resumes (gitignored)
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/resume-shortlisting-ai.git
cd resume-shortlisting-ai
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python app.py
```

### 5. Open in your browser
```
http://127.0.0.1:5000
```

---

## 🧪 Try It Out

A sample job description is included at `sample_data/sample_job_description.txt`
— paste its contents into the form, upload any resumes you have (PDF/DOCX/TXT),
set required skills like `Python, Django, SQL, Git, Docker`, and click **Analyze**.

---

## 🔮 Future Improvements

- [ ] Add support for bulk export of shortlisted candidates (CSV/Excel)
- [ ] Add authentication for multi-recruiter usage
- [ ] Integrate a transformer-based embedding model (e.g. Sentence-BERT) for deeper semantic matching
- [ ] Add a database (SQLite/PostgreSQL) to persist analysis history
- [ ] Add resume-to-JD gap report (suggested skills to add)

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙋 Author
Dua Iqbal

Made with ❤️ by [Dua Iqbal](https://github.com/duaiqbal1)

If you found this useful, please ⭐ star the repo!
