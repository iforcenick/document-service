from ai import generate_ai_text
import re

def extract_summary(content: str):
    section_start = content.find('### Professional Summary')
    if section_start < 0:
        raise Exception('invalid summary generated')
    content_start = content.find('\n', section_start)
    if content_start < 0:
        raise Exception('invalid summary generated')
    content_start += 1
    content_end = content.find('\n', content_start)
    summary = content[content_start:content_end].strip()
    return summary

def extract_skills(content: str):
    section_start = content.find('### Skills')
    if section_start < 0:
        raise Exception('invalid skills generated')
    content_start = content.find('\n', section_start)
    if content_start < 0:
        raise Exception('invalid skills generated')
    skill_categories = []
    matches = re.findall('\\*\\*([^\\*]+)\\*\\*:([^\\*]+)', content[content_start + 1:], flags=re.IGNORECASE)
    for match in matches:
        category_name = match[0].strip()
        skills = [ item.strip() for item in match[1].split(',') if len(item.strip()) > 0 ]
        skill_categories.append({
            "header": category_name,
            "skills": skills,
        })
    print(skill_categories)
    return skill_categories

def generate_summary(position: str, jd: str, profile: dict):
    experience = ''
    position_index = 1
    while True:
        if f'position-title-{position_index}' not in profile:
            break
        position_title = profile[f'position-title-{position_index}']
        company_name = profile[f'company-name-{position_index}']
        company_start_date = profile[f'company-start-date-{position_index}']
        company_end_date = profile[f'company-end-date-{position_index}']
        if company_end_date == '':
            company_end_date = 'present'
        experience += f'{position_title} at {company_name} company from {company_start_date} to {company_end_date}'
        position_index += 1
    prompt = f'''Given the following candidate profile and job description, generate below sections in my resume:

1. **Professional Summary**: concise paragraph summarizing the experience and skills ( shouldn't be longer than 3 sentences ).
2. **Skills**: Categorize the skills based on the job description and add at least 2 more related skills for every category ( shouldn't be more than 5 categories ).

Provide the output in the following format strictly:

### Professional Summary
[Summary text here]

### Skills
**Category**: [List of skills by category by joint ,] like "**Front-End Development**: React,Angular"


Below is the reference data.
`
Work Experience:
{experience}

Job Title:
{position}

Job Description:
{jd}
`
'''
    content = generate_ai_text(prompt, 'You are a helpful resume generator.', 1.0)
    summary = extract_summary(content)
    skill_categories = extract_skills(content)
    return ( summary, skill_categories )