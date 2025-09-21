
````markdown
# 📄 Resume Management & Analysis Suite  

A complete system for **resume handling, management, and AI-powered analysis**.  
This project combines two complementary applications:  

- **🗂️ Flask Resume Sorter** → Upload, organize, and manage resumes.  
- **🤖  Resume Analysis** → AI-powered resume-job description matching and scoring.  

Both apps run locally and are designed to work together as a **Resume Management & Analysis Suite**.  

---

## 🚀 Applications Overview  

### 🔹 Flask Resume Sorter  
**Status:** ✅ Running  
**Port:** `5000`  
**URL:** [http://127.0.0.1:5000](http://127.0.0.1:5000)  

**Features:**  
- Upload resumes (**PDF, DOCX, TXT**)  
- Categorization by **sections & technical domains**  
- Search and filter functionality  
- Resume text extraction & preview  
- Edit resume metadata (title, tags, notes)  
- Download resumes with details  
- AI-powered resume analysis  
- Resume–Job Description (JD) matching  
- Semantic similarity scoring (0–100)  
- Verdict system → **High / Medium / Low fit**  
- Missing skills detection  
- Resume improvement suggestions  
- CSV export for results  

---

## 📋 What You Can Do  

### ✅ With Flask Resume Sorter  
- Upload & manage resumes in different formats  
- Organize by categories like *Software Engineering, Data Science, etc.*  
- Add personal notes to resumes  
- Search and filter efficiently  
- Edit and download resumes anytime  


---

## 🛠️ Installation & Setup  

### 1️⃣ Clone the repository  
```bash
git clone <your-repo-link>
cd <repo-name>
````

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

Visit → [http://127.0.0.1:5000](http://127.0.0.1:5000)



## 📦 Requirements

```txt
Flask==2.3.3
Werkzeug==2.3.7
PyPDF2==3.0.1
python-docx==0.8.11
streamlit==1.35.0
pandas
scikit-learn
spacy
```

---

## 📂 Project Structure

```
├── app.py                   # Flask application entry point   
├── requirements.txt         # Dependencies list  
├── templates/               # HTML templates for Flask  
│   ├── base.html  
│   ├── index.html  
│   ├── upload.html  
│   ├── manage_sections.html  
│   └── view_resume.html  
├── uploads/                 # Uploaded resumes (auto-created)  
├── data/                    # Processed data storage (auto-created)  
```


---


