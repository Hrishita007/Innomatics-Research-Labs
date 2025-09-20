
# 📄 Resume Management & Analysis Suite

This project combines **two applications** for end-to-end resume handling:

* **Flask Resume Sorter** → Upload, categorize, and manage resumes.
* **Streamlit Resume Analysis** → AI-powered resume-job description matching and scoring.

Both apps are fully functional and run locally.

---

## 🚀 Applications Overview

### 🔹 Flask Resume Sorter Application

**Status:** ✅ Running
**Port:** `5000`
**URL:** [http://127.0.0.1:5000](http://127.0.0.1:5000)

**Features:**

* Resume upload and management
* Categorization by sections and technical areas
* Search and filter functionality
* Text extraction and preview
* Edit resume metadata
* Download functionality

---

### 🔹 Streamlit Resume Analysis Application

**Status:** ✅ Running
**Port:** `8501`
**URL:** [http://127.0.0.1:8501](http://127.0.0.1:8501)

**Features:**

* AI-powered resume analysis
* Job description matching
* Semantic similarity analysis
* Resume scoring system (0–100)
* Verdict system: **High / Medium / Low**
* Missing skills identification
* Database storage & CSV export

---

## 📋 What You Can Do

### ✅ Flask Resume Sorter

* Upload resumes in **PDF, DOCX, or TXT** format
* Organize by **technical sections** (e.g., Software Engineering, Data Science, etc.)
* Add notes & categorize by specific areas
* Search & filter resumes easily
* View and edit resume details

### ✅ Streamlit Resume Analysis

* Upload a **job description** and multiple resumes
* Get **AI-powered relevance scores**
* See detailed missing skills analysis
* Receive **resume improvement suggestions**
* Export results to **CSV** for further analysis

---

## 🛠️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone <your-repo-link>
cd <repo-name>
```

### 2️⃣ Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Flask app

```bash
python app.py
```

Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

### 5️⃣ Run the Streamlit app

```bash
streamlit run app.py
```

Visit: [http://127.0.0.1:8501](http://127.0.0.1:8501)

---

## 📦 Requirements

```txt
Flask==2.3.3
PyPDF2==3.0.1
python-docx==0.8.11
Werkzeug==2.3.7
```

---

## 📂 Project Structure

```
├── app.py                # Main Python file (Flask entry point)
├── requirements.txt       # Project dependencies
├── templates/             # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── upload.html
│   ├── manage_sections.html
│   └── view_resume.html
├── uploads/               # Resume uploads (auto-created)
├── data/                  # Processed data storage (auto-created)
```

---

## 🎯 Usage Recommendation

* Use the **Flask app** to manage and organize your resume collection.
* Use the **Streamlit app** to analyze resumes against **job descriptions** for AI-driven insights.

Both apps complement each other, providing a complete **Resume Management & Analysis Suite**.

---

