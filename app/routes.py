from crypt import methods

from flask import Blueprint
from app.resume_parser import  extract_text_from_pdf
from app.job_parser import extract_text_from_txt
from app.matcher import match_score
from app.ai_rewriter import suggest_resume_improvements
import os
from flask import render_template, url_for, request, redirect
from werkzeug.utils import secure_filename



main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/parse_resume')
def parse_resume():
    #Using a sample file
    resume_path = os.path.join('data', "sample_cv.pdf")
    extract_text = extract_text_from_pdf(resume_path)
    return f"<pre>{extract_text}</pre>"

@main.route('/parse_job')
def parse_job():
    job_path = os.path.join('data', 'sample_job.txt')
    job_text = extract_text_from_txt(job_path)
    return f"<pre>{job_text}</pre>"

@main.route("/match_score")
def match_result():
    resume_path = os.path.join('data', "sample_cv.pdf")
    job_path = os.path.join('data', 'sample_job.txt')

    resume_text = extract_text_from_pdf(resume_path)
    job_text = extract_text_from_txt(job_path)

    score, matches = match_score(resume_text, job_text)

    return f"<h2> Match Score: {score}%</h2><p>Matching Keywords: {', '.join(matches)}</p>"


@main.route('/suggestions')
def get_suggestions():
    resume_path = os.path.join('data', "sample_cv.pdf")
    job_path = os.path.join('data', 'sample_job.txt')

    resume_text = extract_text_from_pdf(resume_path)
    job_text = extract_text_from_txt(job_path)

    suggestions = suggest_resume_improvements(resume_text, job_text)

    return f'<h2> Suggestions to Improve Your Resume</h2><p>{suggestions.replace('\n', '<br>')}</p>'

@main.route('/results', methods=['POST'])
def results():
    resume_file = request.files['resume']
    job_file = request.files['job']

    resume_path = os.path.join('uploads', secure_filename(resume_file.filename))
    job_path = os.path.join('uploads', secure_filename(job_file.filename))

    resume_file.save(resume_path)
    job_file.save(job_path)

    resume_text = extract_text_from_pdf(resume_path)
    job_text = extract_text_from_txt(job_path)

    score, matches = match_score(resume_text, job_text)
    suggestions = suggest_resume_improvements(resume_text, job_text)

    return f'''
    <h2>Match Score: {score}%</h2>
    <p>Matching Keywords: {', '.join(matches)}</p>
    <h3>Suggestions to Improve Your Resume</h3>
    <p>{suggestions.replace('\n', '<br>')}</p>
'''