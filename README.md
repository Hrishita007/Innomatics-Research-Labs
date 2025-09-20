# Innomatics-Research-Labs

Workflow
Job Requirement Upload - Placement team uploads job description (JD).
Resume Upload - Students upload resumes while applying.
Resume Parsing
Extract raw text from PDF/DOCX.
Standardize formats (remove headers/footers, normalize sections).
JD Parsing
Extract role title, must-have skills, good-to-have skills, qualifications.
Relevance Analysis
Step 1: Hard Match – keyword & skill check (exact and fuzzy matches).
Step 2: Semantic Match – embedding similarity between resume and JD using LLMs.
Step 3: Scoring & Verdict – Weighted scoring formula for final score.
Output Generation
Relevance Score (0–100).
Missing Skills/Projects/Certifications.
Verdict (High / Medium / Low suitability).
Suggestions for student improvement.
Storage & Access
Results stored in the database.
The placement team can search/filter resumes by job role, score, and location.
Web Application
Placement team dashboard: upload JD, see shortlisted resumes.
