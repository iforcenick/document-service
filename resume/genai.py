from ai import generate_ai_text, inject_variables_to_content
import re
from .utils import get_profile_experience_description
import yaml

def get_bullet_counts(resume_template_index: int):
    with open('./assets/docx/metadata.yaml', 'r') as stream:
        bullets_data = yaml.safe_load(stream)
        return bullets_data[resume_template_index - 1]

def extract_summary(content: str):
    matches = re.findall('### Professional Summary([\\s\\S]*?)\n###', content)
    if matches is None:
        raise Exception('summary not found')
    return matches[0].strip()

def extract_skills(content: str):
    matches = re.findall('### Skills([\\s\\S]*?)$', content)
    if matches is None:
        raise Exception('skills not found')
    
    skill_categories = []
    matches = re.findall('\\*\\*([^\\*]+)\\*\\*:([^\\*]+)', matches[0].strip(), flags=re.IGNORECASE)
    for match in matches:
        category_name = match[0].strip()
        skills = [ item.strip() for item in match[1].split(',') if len(item.strip()) > 0 ]
        skill_categories.append({
            "header": category_name,
            "skills": skills,
        })
    return skill_categories

def extract_work_history(content: str):
    matches = re.findall('### Work Experience([\\s\\S]*?)\n###', content)
    if matches is None:
        raise Exception('summary not found')
    experience = matches[0].strip()
    matches = re.findall('\\*\\*([^\\*]+)\\*\\*[\\s]*\n\\*\\*Period\\*\\*([^\\*]+)\n\\*\\*Role\\*\\*([^\\*]+)\n\\*\\*Job Descriptions\\*\\*[\\s]*\n([^\\*]+)(?=\\*\\*|$)', experience)
    history = []
    for match in matches:
        history.append({
            "position": match[2].strip(),
            "sentences": [ line.strip() for line in match[3].strip().split('- ') if line.strip() != "" ]
        })
    return history


def generate_summary(position: str, jd: str, profile: dict):
    experience = get_profile_experience_description(profile)
    variables = {
        "experience": experience,
        "position": position,
        "jd": jd,
    }
    with open('./resume/prompt/summary.txt') as stream:
        prompt_template = stream.read()
        prompt = inject_variables_to_content(prompt_template, variables)

    content = generate_ai_text(prompt, 'You are a helpful resume generator.', 1.0)
    summary = extract_summary(content)
    skill_categories = extract_skills(content)
    return ( summary, skill_categories )

def generate_work_history(position: str, jd: str, profile: dict):
    experience = get_profile_experience_description(profile)
    bullet_counts = get_bullet_counts(profile['resume-template-index'])
    print(bullet_counts)
    bullet_counts_str = ", ".join([ str(item) for item in bullet_counts ])
    variables = {
        "experience": experience,
        "bullet_counts": bullet_counts_str,
        "position": position,
        "jd": jd,
    }
    with open('./resume/prompt/work_history.txt') as stream:
        prompt_template = stream.read()
        prompt = inject_variables_to_content(prompt_template, variables)

    print(prompt)
    content = generate_ai_text(prompt, 'You are a helpful resume generator.', 1.0)
    work_history = extract_work_history(content)
    return work_history

def generate_all(position: str, jd: str, profile: dict):
    experience = get_profile_experience_description(profile)
    bullet_counts = get_bullet_counts(profile['resume-template-index'])
    bullet_counts_str = ", ".join([ str(item) for item in bullet_counts ])
    variables = {
        "experience": experience,
        "bullet_counts": bullet_counts_str,
        "position": position,
        "jd": jd,
    }
    with open('./resume/prompt/all.txt') as stream:
        prompt_template = stream.read()
        prompt = inject_variables_to_content(prompt_template, variables)

    content = generate_ai_text(prompt, 'You are a helpful resume generator.', 1.0)
    summary = extract_summary(content)
    skill_categories = extract_skills(content)
    work_history = extract_work_history(content)
    return ( summary, skill_categories, work_history )
