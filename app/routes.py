from flask import Blueprint
from app.resume_parser import  extract_text_from_pdf
from app.job_parser import extract_text_from_txt
from app.matcher import match_score
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return 'Flask is working!'

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



