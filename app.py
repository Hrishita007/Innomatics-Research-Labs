from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import PyPDF2
import docx
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('data', exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}

# Default sections and areas
DEFAULT_SECTIONS = {
    'Technical': ['Software Engineering', 'Data Science', 'DevOps', 'Cybersecurity', 'AI/ML'],
    'Business': ['Marketing', 'Sales', 'Finance', 'Operations', 'Strategy'],
    'Creative': ['Design', 'Content Writing', 'Video Production', 'Photography', 'UX/UI'],
    'Healthcare': ['Nursing', 'Medical', 'Pharmacy', 'Therapy', 'Administration'],
    'Education': ['Teaching', 'Research', 'Administration', 'Curriculum', 'Training']
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_file(filepath):
    """Extract text from uploaded resume files"""
    try:
        if filepath.endswith('.pdf'):
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        elif filepath.endswith('.docx'):
            doc = docx.Document(filepath)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        elif filepath.endswith('.txt'):
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def load_data():
    """Load resume data from JSON file"""
    data_file = 'data/resumes.json'
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            return json.load(f)
    return {'resumes': [], 'sections': DEFAULT_SECTIONS}

def save_data(data):
    """Save resume data to JSON file"""
    data_file = 'data/resumes.json'
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', 
                         resumes=data['resumes'], 
                         sections=data['sections'])

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Add timestamp to avoid conflicts
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Extract text for preview
            text_content = extract_text_from_file(filepath)
            
            # Create resume entry
            resume_entry = {
                'id': len(load_data()['resumes']) + 1,
                'filename': filename,
                'original_name': file.filename,
                'upload_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'section': request.form.get('section', 'Unsorted'),
                'area': request.form.get('area', 'General'),
                'notes': request.form.get('notes', ''),
                'text_preview': text_content[:500] + '...' if len(text_content) > 500 else text_content
            }
            
            # Save to data
            data = load_data()
            data['resumes'].append(resume_entry)
            save_data(data)
            
            flash('Resume uploaded successfully!')
            return redirect(url_for('index'))
        else:
            flash('Invalid file type. Please upload PDF, DOC, DOCX, or TXT files.')
    
    data = load_data()
    return render_template('upload.html', sections=data['sections'])

@app.route('/manage_sections')
def manage_sections():
    data = load_data()
    return render_template('manage_sections.html', sections=data['sections'])

@app.route('/add_section', methods=['POST'])
def add_section():
    section_name = request.form.get('section_name')
    if section_name:
        data = load_data()
        if section_name not in data['sections']:
            data['sections'][section_name] = []
            save_data(data)
            flash(f'Section "{section_name}" added successfully!')
        else:
            flash('Section already exists!')
    return redirect(url_for('manage_sections'))

@app.route('/add_area', methods=['POST'])
def add_area():
    section_name = request.form.get('section_name')
    area_name = request.form.get('area_name')
    if section_name and area_name:
        data = load_data()
        if section_name in data['sections']:
            if area_name not in data['sections'][section_name]:
                data['sections'][section_name].append(area_name)
                save_data(data)
                flash(f'Area "{area_name}" added to section "{section_name}"!')
            else:
                flash('Area already exists in this section!')
        else:
            flash('Section does not exist!')
    return redirect(url_for('manage_sections'))

@app.route('/delete_section/<section_name>')
def delete_section(section_name):
    data = load_data()
    if section_name in data['sections']:
        del data['sections'][section_name]
        save_data(data)
        flash(f'Section "{section_name}" deleted successfully!')
    return redirect(url_for('manage_sections'))

@app.route('/delete_area/<section_name>/<area_name>')
def delete_area(section_name, area_name):
    data = load_data()
    if section_name in data['sections'] and area_name in data['sections'][section_name]:
        data['sections'][section_name].remove(area_name)
        save_data(data)
        flash(f'Area "{area_name}" deleted from section "{section_name}"!')
    return redirect(url_for('manage_sections'))

@app.route('/update_resume/<int:resume_id>', methods=['POST'])
def update_resume(resume_id):
    data = load_data()
    for resume in data['resumes']:
        if resume['id'] == resume_id:
            resume['section'] = request.form.get('section', resume['section'])
            resume['area'] = request.form.get('area', resume['area'])
            resume['notes'] = request.form.get('notes', resume['notes'])
            break
    save_data(data)
    return jsonify({'status': 'success'})

@app.route('/delete_resume/<int:resume_id>')
def delete_resume(resume_id):
    data = load_data()
    resume_to_delete = None
    for i, resume in enumerate(data['resumes']):
        if resume['id'] == resume_id:
            resume_to_delete = data['resumes'].pop(i)
            break
    
    if resume_to_delete:
        # Delete the file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], resume_to_delete['filename'])
        if os.path.exists(filepath):
            os.remove(filepath)
        save_data(data)
        flash('Resume deleted successfully!')
    
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/get_areas/<section_name>')
def get_areas(section_name):
    data = load_data()
    areas = data['sections'].get(section_name, [])
    return jsonify(areas)

@app.route('/view_resume/<int:resume_id>')
def view_resume(resume_id):
    data = load_data()
    resume = None
    for r in data['resumes']:
        if r['id'] == resume_id:
            resume = r
            break
    
    if resume:
        # Get full text content
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], resume['filename'])
        if os.path.exists(filepath):
            full_text = extract_text_from_file(filepath)
            resume['full_text'] = full_text
        
        return render_template('view_resume.html', resume=resume, sections=data['sections'])
    else:
        flash('Resume not found!')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
