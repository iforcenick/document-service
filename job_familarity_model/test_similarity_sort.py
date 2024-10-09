from skill.utils import normalize_skill_name, get_skill_list
from job_familarity_model.word2vec import similarity_nm
import re

def get_weighted_skills(weight_string):
    matches = re.findall('\\s*(.*?) x([0-9\\.]+)', weight_string, flags=re.IGNORECASE)
    if matches is None:
        print('Invalid input')
        return None
    all_weighted_skills = []
    for match in matches:
        all_weighted_skills.append({
            "skill_name": normalize_skill_name(match[0]),
            "weight": float(match[1])
        })
    return all_weighted_skills

temp = input()
skills1 = get_weighted_skills(temp)
print(skills1)

similarities = []

all_skills = get_skill_list()
for skill in all_skills:
    skills2 = [{
        "skill_name": normalize_skill_name(skill),
        "weight": 1,
    }]
    score = similarity_nm(skills1, skills2) ** 10
    similarities.append(( skill, score ))
similarities.sort(key=lambda x: x[1], reverse=True)
for item in similarities:
    print(item[0], item[1])