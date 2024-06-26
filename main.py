from flask import Flask, request, send_file
from flask_cors import CORS
import tempfile
import uuid
import os
import json

from env import DOCUMENT_SERVICE_PORT
import resume
import coverletter
from skill.utils import get_required_skills
from social_profile import get_profile_from_name
from util import get_save_path

TEMP_PATH = tempfile.gettempdir()

app = Flask(__name__)
CORS(app)


@app.post("/resume/generate/metadata")
def generate_resume_metadata():
    body = json.loads(request.data)
    required_skills = get_required_skills(body["jd"], body["position"])
    headline, summary = resume.generate_meta_data(body["position"], required_skills)
    return {
        "headline": headline,
        "summary": summary,
    }

@app.post("/resume/generate/skillmatrix")
def generate_resume_skill_matrix():
    body = json.loads(request.data)
    required_skills = get_required_skills(body["jd"], body["position"])
    profile = get_profile_from_name(body['profile'])
    skill_section_headers, skill_section_contents = resume.generate_skill_matrix(profile, body["position"], required_skills)
    sections = []
    for index, header in enumerate(skill_section_headers):
        sections.append({ "header": header, "content": skill_section_contents[index] })
    return sections

@app.post("/resume/generate/skillmatrix/detail")
def generate_resume_detailed_skill_matrix():
    body = json.loads(request.data)
    required_skills = get_required_skills(body["jd"], body["position"])
    profile = get_profile_from_name(body['profile'])
    skill_section_headers, skill_section_contents = resume.generate_detailed_skill_matrix(profile, body["position"], required_skills)
    sections = []
    for index, header in enumerate(skill_section_headers):
        sections.append({ "header": header, "content": skill_section_contents[index] })
    return sections




@app.post("/resume/generate/history")
def generate_resume_history():
    body = json.loads(request.data)
    required_skills = get_required_skills(body["jd"], body["position"])
    profile = get_profile_from_name(body['profile'])
    history = resume.generate_resume_history(profile, body["position"], required_skills, body["jd"])
    return history

@app.post("/resume/generate/history/detail")
def generate_detailed_resume_history():
    body = json.loads(request.data)
    required_skills = get_required_skills(body["jd"], body["position"])
    profile = get_profile_from_name(body['profile'])
    detailed_history = resume.generate_detailed_resume_history(profile, body["position"], required_skills, body["jd"])
    return detailed_history




@app.post("/resume/generate/file")
def generate_resume_file():
    body = json.loads(request.data)
    required_skills = get_required_skills(body["jd"], body["position"])
    profile = get_profile_from_name(body['profile'])
    file_path = get_save_path(body["fileId"], body['profile'], 'resume', body['ext'])
    resume.generate_resume_file(body["position"], required_skills, body["jd"], profile, file_path)
    response = send_file(file_path, mimetype='application/pdf')
    return response

@app.post("/resume/generate/binary")
def generate_resume_binary():
    body = json.loads(request.data)
    required_skills = get_required_skills(body["jd"], body["position"])
    temp_file_id = str(uuid.uuid4())
    temp_pdfpath = f'{TEMP_PATH}/{temp_file_id}.pdf'
    profile = get_profile_from_name(body['profile'])
    resume.generate_resume_file(body["position"], required_skills, body["jd"], profile, temp_pdfpath)
    response = send_file(temp_pdfpath, mimetype='application/pdf')
    os.remove(temp_pdfpath)
    return response

@app.post("/resume/generate/fromjd")
def generate_resume_fromjd_binary():
    body = json.loads(request.data)
    position = resume.metadata.get_most_proper_position_from_jd(body["jd"])
    required_skills = get_required_skills(body["jd"], position)
    temp_file_id = str(uuid.uuid4())
    temp_pdfpath = f'{TEMP_PATH}/{temp_file_id}.pdf'
    profile = get_profile_from_name(body['profile'])
    resume.generate_resume_file(position, required_skills, body["jd"], profile, temp_pdfpath)
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
    required_skills = get_required_skills(body["jd"], body["position"])
    profile = get_profile_from_name(body['profile'])
    file_path = get_save_path(body["fileId"], body['profile'], 'coverletter', body['ext'])
    coverletter.generate_cover_letter_file(body['position'], required_skills, body['jd'], body['company'], profile, file_path)
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
    required_skills = get_required_skills(body["jd"], body["position"])
    temp_file_id = str(uuid.uuid4())
    temp_pdfpath = f'{TEMP_PATH}/{temp_file_id}.pdf'
    profile = get_profile_from_name(body['profile'])
    coverletter.generate_cover_letter_file(body['position'], required_skills, body['jd'], body['company'], profile, temp_pdfpath)
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