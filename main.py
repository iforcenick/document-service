from flask import Flask, request, send_file
from flask_cors import CORS
import tempfile
import uuid
import os
import json

from env import DOCUMENT_SERVICE_PORT
import resume
import coverletter
from social_profile import get_profile_from_name
from util import get_save_path

TEMP_PATH = tempfile.gettempdir()

app = Flask(__name__)
CORS(app)


@app.post("/resume/generate/headline")
def generate_resume_headline():
    body = json.loads(request.data)
    profile = get_profile_from_name(body['profile'])
    headline = resume.generate_headline(body["position"], body["jd"], profile)
    return {
        "headline": headline,
    }

@app.post("/resume/generate/summary")
def generate_resume_summary():
    body = json.loads(request.data)
    profile = get_profile_from_name(body['profile'])
    ( summary, skill_categories ) = resume.generate_summary(body["position"], body["jd"], profile)
    return {
        "summary": summary,
        "skill_categories": skill_categories,
    }




@app.post("/resume/generate/history")
def generate_resume_history():
    body = json.loads(request.data)
    profile = get_profile_from_name(body['profile'])
    history = resume.generate_work_history(body["position"], body["jd"], profile)
    return history




@app.post("/resume/generate/file")
def generate_resume_file():
    body = json.loads(request.data)
    profile = get_profile_from_name(body['profile'])
    file_path = get_save_path(body["fileId"], body['profile'], 'resume', body['ext'])
    resume.generate_resume_file(body["position"], body["jd"], profile, file_path)
    response = send_file(file_path, mimetype='application/pdf')
    return response

@app.post("/resume/generate/binary")
def generate_resume_binary():
    body = json.loads(request.data)
    temp_file_id = str(uuid.uuid4())
    temp_pdfpath = f'{TEMP_PATH}/{temp_file_id}.pdf'
    profile = get_profile_from_name(body['profile'])
    resume.generate_resume_file(body["position"], body["jd"], profile, temp_pdfpath)
    response = send_file(temp_pdfpath, mimetype='application/pdf')
    os.remove(temp_pdfpath)
    return response

@app.post("/resume/generate/fromjd")
def generate_resume_fromjd_binary():
    body = json.loads(request.data)
    position = resume.get_most_proper_position_from_jd(body["jd"])
    temp_file_id = str(uuid.uuid4())
    temp_pdfpath = f'{TEMP_PATH}/{temp_file_id}.pdf'
    profile = get_profile_from_name(body['profile'])
    resume.generate_resume_file(position, body["jd"], profile, temp_pdfpath)
    response = send_file(temp_pdfpath, mimetype='application/pdf')
    os.remove(temp_pdfpath)
    return response

@app.post("/resume/download")
def download_generated_resume():
    body = json.loads(request.data)
    file_path = get_save_path(body["fileId"], body['profile'], 'resume', body['ext'])
    response = send_file(file_path, mimetype='application/pdf')
    return response





@app.post("/coverletter/generate/file")
def generate_cover_letter_file():
    body = json.loads(request.data)
    profile = get_profile_from_name(body['profile'])
    file_path = get_save_path(body["fileId"], body['profile'], 'coverletter', body['ext'])
    coverletter.generate_cover_letter_file(body['position'], body['jd'], body['company'], profile, file_path)
    response = send_file(file_path, mimetype='application/pdf')
    return response

@app.post("/coverletter/generate/fromjd")
def generate_cover_letter_fromjd_binary():
    body = json.loads(request.data)
    temp_file_id = str(uuid.uuid4())
    temp_pdfpath = f'{TEMP_PATH}/{temp_file_id}.pdf'
    profile = get_profile_from_name(body['profile'])
    coverletter.generate_cover_letter_file_from_jd(body['jd'], profile, temp_pdfpath)
    response = send_file(temp_pdfpath, mimetype='application/pdf')
    os.remove(temp_pdfpath)
    return response

@app.post("/coverletter/generate/binary")
def generate_cover_letter_binary():
    body = json.loads(request.data)
    temp_file_id = str(uuid.uuid4())
    temp_pdfpath = f'{TEMP_PATH}/{temp_file_id}.pdf'
    profile = get_profile_from_name(body['profile'])
    coverletter.generate_cover_letter_file(body['position'], body['jd'], body['company'], profile, temp_pdfpath)
    response = send_file(temp_pdfpath, mimetype='application/pdf')
    os.remove(temp_pdfpath)
    return response

@app.post("/coverletter/download")
def download_generated_coverletter():
    body = json.loads(request.data)
    file_path = get_save_path(body["fileId"], body['profile'], 'coverletter', body['ext'])
    response = send_file(file_path, mimetype='application/pdf')
    return response

app.run(port=DOCUMENT_SERVICE_PORT, host='0.0.0.0')