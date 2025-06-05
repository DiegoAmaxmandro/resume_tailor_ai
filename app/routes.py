from flask import Blueprint
from app.resume_parser import  extract_text_from_pdf
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

