from skill.utils import normalize_skill_name
from resume.utils import expand_weighted_skills_into_full_list
from job_familarity_model.word2vec import similarity_nm
from .word2vec import word_vect
import re

def get_expanded_skills(weight_string):
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
    all_expanded = expand_weighted_skills_into_full_list(all_weighted_skills)
    return all_expanded

temp = input()
skills1 = get_expanded_skills(temp)
print(skills1)

while True:
    temp = input()
    skills2 = get_expanded_skills(temp)
    print(skills2)
    score = similarity_nm(skills1, skills2) ** 10
    print(score)
