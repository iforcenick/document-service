from skill.utils import normalize_skill_name
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

while True:
    temp = input()
    skills2 = get_weighted_skills(temp)
    print(skills2)
    score = similarity_nm(skills1, skills2) ** 10
    print(score)
