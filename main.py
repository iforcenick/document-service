from flask import Flask, request, send_file
from flask_cors import CORS

from env import DOCUMENT_SERVICE_PORT

import resume
import coverletter
import json
from skill.utils import get_required_skills
import tempfile

import uuid
import os

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
    skill_section_headers, skill_section_contents = resume.generate_skill_matrix(body["position"], required_skills)
    sections = []
    for index, header in enumerate(skill_section_headers):
        sections.append({ "header": header, "content": skill_section_contents[index] })
    return sections

@app.post("/resume/generate/skillmatrix/detail")
def generate_resume_detailed_skill_matrix():
    body = json.loads(request.data)
    required_skills = get_required_skills(body["jd"], body["position"])
    skill_section_headers, skill_section_contents = resume.generate_detailed_skill_matrix(body["position"], required_skills)
    sections = []
    for index, header in enumerate(skill_section_headers):
        sections.append({ "header": header, "content": skill_section_contents[index] })
    return sections




@app.post("/resume/generate/history")
def generate_resume_history():
    body = json.loads(request.data)
    required_skills = get_required_skills(body["jd"], body["position"])
    profile_index = body["profile"]
    history = resume.generate_resume_history(profile_index, body["position"], required_skills, body["jd"])
    return history

@app.post("/resume/generate/history/detail")
def generate_detailed_resume_history():
    body = json.loads(request.data)
    profile_index = body["profile"]
    required_skills = get_required_skills(body["jd"], body["position"])
    detailed_history = resume.generate_detailed_resume_history(profile_index, body["position"], required_skills, body["jd"])
    return detailed_history



@app.post("/resume/generate/file")
def generate_resume_file():
    body = json.loads(request.data)
    required_skills = get_required_skills(body["jd"], body["position"])
    resume.generate_resume_file(body["position"], required_skills, body["jd"], int(body['profile']), body["path"])
    return ""

@app.post("/resume/generate/binary")
def generate_resume_binary():
    body = json.loads(request.data)
    required_skills = get_required_skills(body["jd"], body["position"])
    temp_file_id = str(uuid.uuid4())
    temp_pdfpath = f'{TEMP_PATH}/{temp_file_id}.pdf'
    resume.generate_resume_file(body["position"], required_skills, body["jd"], int(body['profile']), temp_pdfpath)
    response = send_file(temp_pdfpath, mimetype='application/pdf')
    os.remove(temp_pdfpath)
    return response


@app.post("/coverletter/generate/file")
def generate_cover_letter_file():
    body = json.loads(request.data)
    required_skills = get_required_skills(body["jd"], body["position"])
    coverletter.generate_cover_letter_file(body['position'], required_skills, body['jd'], body['company'], int(body['profile']), body["path"])
    return ""

@app.post("/coverletter/generate/binary")
def generate_cover_letter_binary():
    body = json.loads(request.data)
    required_skills = get_required_skills(body["jd"], body["position"])
    temp_file_id = str(uuid.uuid4())
    temp_pdfpath = f'{TEMP_PATH}/{temp_file_id}.pdf'
    coverletter.generate_cover_letter_file(body['position'], required_skills, body['jd'], body['company'], int(body['profile']), temp_pdfpath)
    response = send_file(temp_pdfpath, mimetype='application/pdf')
    os.remove(temp_pdfpath)
    return response

app.run(port=DOCUMENT_SERVICE_PORT)