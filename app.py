import streamlit as st
import pandas as pd
import sqlite3
import fitz
import docx2txt
import spacy
import tempfile
from sentence_transformers import SentenceTransformer, util
import re

# ------------------ Page Config ------------------
st.set_page_config(page_title="Automated Resume Relevance Check System",
                   page_icon="📄", layout="wide")

nlp = spacy.load("en_core_web_sm")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# ------------------ Database ------------------
conn = sqlite3.connect("database.db", check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS evaluations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resume_name TEXT,
                job_name TEXT,
                role_title TEXT,
                score REAL,
                verdict TEXT,
                missing_items TEXT,
                suggestions TEXT
             )''')
conn.commit()

# ------------------ CSS Styling ------------------
st.markdown("""
    <style>
    body { background-color: #f4f8fb; font-family: 'Segoe UI', sans-serif; }
    .main { background-color: #f4f8fb; }
    h1, h2, h3 { color: #00695c; font-weight: 700; letter-spacing: 1px;}
    .st-emotion-cache-1v0mbdj { background: #fff; border-radius: 12px; box-shadow: 0 2px 12px #e0e0e0; }
    .stFileUploader>div>div>input { border-radius: 8px; border:1px solid #bdbdbd; padding:7px; }
    .stButton>button {
        border-radius: 10px; background-color: #00695c; color:white; font-weight:bold; box-shadow:1px 2px 5px #b2dfdb;
        transition: background 0.2s;
    }
    .stButton>button:hover { background-color: #00897b; }
    .stDataFrame, .streamlit-expanderHeader {
        background-color: #ffffff; border-radius: 12px; box-shadow: 0px 2px 12px #b2dfdb;
    }
    .high {color:white; background-color:#43a047; padding:3px 10px; border-radius:5px; font-weight:bold;}
    .medium {color:black; background-color:#fff176; padding:3px 10px; border-radius:5px; font-weight:bold;}
    .low {color:white; background-color:#e53935; padding:3px 10px; border-radius:5px; font-weight:bold;}
    .st-emotion-cache-1v0mbdj { padding: 2rem 2rem 1rem 2rem; }
    .st-emotion-cache-1v0mbdj .stMarkdown { margin-bottom: 0.5rem; }
    .st-emotion-cache-1v0mbdj .stDataFrame { margin-top: 1.5rem; }
    .st-emotion-cache-1v0mbdj .stDownloadButton { margin-top: 1.5rem; }
    </style>
""", unsafe_allow_html=True)

# ------------------ Utility Functions ------------------
def extract_text(file):
    text = ""
    if file.name.endswith(".pdf"):
        pdf = fitz.open(stream=file.read(), filetype="pdf")
        for page in pdf:
            text += page.get_text()
    elif file.name.endswith(".docx"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(file.read())
            text = docx2txt.process(tmp.name)
    elif file.name.endswith(".txt"):
        text = file.read().decode("utf-8")
    text = "\n".join([line.strip() for line in text.splitlines() if 0 < len(line.strip()) < 100])
    return text

def preprocess(text):
    doc = nlp(text.lower())
    tokens = [t.lemma_ for t in doc if not t.is_stop and not t.is_punct]
    return " ".join(tokens)

def parse_jd(jd_text):
    role_title = re.search(r"(?:Role|Position|Job Title)\s*:\s*(.*)", jd_text, re.IGNORECASE)
    must_skills = re.findall(r"(?:Must[- ]Have Skills|Required Skills)\s*:\s*(.*)", jd_text, re.IGNORECASE)
    good_skills = re.findall(r"(?:Good[- ]to[- ]Have Skills|Preferred Skills)\s*:\s*(.*)", jd_text, re.IGNORECASE)
    qualifications = re.findall(r"(?:Qualifications|Education)\s*:\s*(.*)", jd_text, re.IGNORECASE)

    return {
        "role_title": role_title.group(1) if role_title else "N/A",
        "must_skills": must_skills[0].split(",") if must_skills else [],
        "good_skills": good_skills[0].split(",") if good_skills else [],
        "qualifications": qualifications[0].split(",") if qualifications else []
    }

def hard_match(resume_text, jd_skills):
    missing = []
    match_count = 0
    for skill in jd_skills:
        skill = skill.strip().lower()
        if skill and skill in resume_text:
            match_count += 1
        else:
            missing.append(skill)
    score = match_count / max(len(jd_skills), 1)
    return score, missing

def semantic_match(resume_text, jd_text):
    resume_emb = embedder.encode([resume_text], convert_to_tensor=True)
    jd_emb = embedder.encode([jd_text], convert_to_tensor=True)
    return util.cos_sim(resume_emb, jd_emb).item()

def get_final_score(hard_score, semantic_score):
    final_score = (0.4 * hard_score) + (0.6 * semantic_score)
    verdict = "High" if final_score > 0.75 else "Medium" if final_score > 0.5 else "Low"
    return round(final_score * 100, 2), verdict

def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def color_verdict(val):
    if val == "High": return 'background-color: #4CAF50; color:white; font-weight:bold'
    elif val == "Medium": return 'background-color: #FFEB3B; color:black; font-weight:bold'
    else: return 'background-color: #F44336; color:white; font-weight:bold'

# ------------------ UI ------------------
st.markdown(
    """
    <div style="display:flex;align-items:center;gap:16px;">
        <img src="https://img.icons8.com/ios-filled/100/00695c/resume.png" width="60"/>
        <div>
            <h1 style="margin-bottom:0;">Automated Resume Relevance Check</h1>
            <p style="color:#00695c;font-size:1.1rem;margin-top:0;">Professional dashboard for placement teams & recruiters</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

with st.container():
    st.markdown("#### 1. Upload Job Description & Resumes")
    col1, col2 = st.columns(2)
    with col1:
        job_file = st.file_uploader(
            "Upload Job Description (PDF/DOCX/TXT)",
            type=["pdf", "docx", "txt"],
            help="Upload the job description file here."
        )
    with col2:
        resume_files = st.file_uploader(
            "Upload Resumes (PDF/DOCX)",
            type=["pdf", "docx"],
            accept_multiple_files=True,
            help="Upload one or more candidate resumes."
        )

if job_file and resume_files:
    st.markdown("#### 2. Results & Insights")
    jd_text = extract_text(job_file)
    jd_text_proc = preprocess(jd_text)
    jd_info = parse_jd(jd_text)

    st.markdown(
        f"""
        <div style="background:#e0f2f1;padding:1rem 1.5rem;border-radius:10px;margin-bottom:1rem;">
            <b>Role:</b> {jd_info['role_title']}<br>
            <b>Must-have skills:</b> {', '.join(jd_info['must_skills'])}<br>
            <b>Good-to-have skills:</b> {', '.join(jd_info['good_skills'])}
        </div>
        """, unsafe_allow_html=True
    )

    results = []
    for resume in resume_files:
        resume_text = extract_text(resume)
        resume_text_proc = preprocess(resume_text)

        hard_score, missing_items = hard_match(resume_text_proc, jd_info["must_skills"] + jd_info["good_skills"])
        semantic_score = semantic_match(resume_text_proc, jd_text_proc)
        final_score, verdict = get_final_score(hard_score, semantic_score)
        suggestions = "Add missing skills: " + ", ".join(missing_items) if missing_items else "No major gaps."

        c.execute("""
        INSERT INTO evaluations (resume_name, job_name, role_title, score, verdict, missing_items, suggestions)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
                  (resume.name, job_file.name, jd_info["role_title"], final_score, verdict,
                   ", ".join(missing_items), suggestions))
        conn.commit()

        results.append({
            "Resume": resume.name,
            "Score": final_score,
            "Verdict": verdict,
            "Missing Items": ", ".join(missing_items),
            "Suggestions": suggestions
        })

    st.markdown("##### Evaluation Results")
    df_results = pd.DataFrame(results)
    st.dataframe(df_results.style.applymap(color_verdict, subset=['Verdict']), use_container_width=True)

# ------------------ Stored Evaluations ------------------
st.markdown("---")
st.markdown("## 🗂 Stored Evaluations")
with st.expander("🔎 Filters & Download CSV", expanded=True):
    filter_job = st.text_input("Filter by Job Name / Role Title")
    min_score, max_score = st.slider("Score Range", 0, 100, (0, 100))
    filter_verdict = st.multiselect("Verdict", ["High","Medium","Low"], default=["High","Medium","Low"])
    filter_missing_skill = st.text_input("Filter by Missing Skill")

query = "SELECT resume_name, job_name, role_title, score, verdict, missing_items, suggestions FROM evaluations WHERE 1=1"
params = []
if filter_job:
    query += " AND (job_name LIKE ? OR role_title LIKE ?)"
    params += [f"%{filter_job}%", f"%{filter_job}%"]

stored_df = pd.read_sql_query(query, conn, params=params)
stored_df = stored_df[stored_df['score'].between(min_score, max_score)]
stored_df = stored_df[stored_df['verdict'].isin(filter_verdict)]
if filter_missing_skill:
    stored_df = stored_df[stored_df['missing_items'].str.contains(filter_missing_skill, case=False, na=False)]

st.dataframe(stored_df.style.applymap(color_verdict, subset=['verdict']), use_container_width=True)

csv = convert_df_to_csv(stored_df)
st.download_button("⬇️ Download Filtered Results as CSV", csv, "filtered_evaluations.csv", "text/csv")
