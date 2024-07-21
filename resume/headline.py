from job_familarity_model.word2vec import similarity_n1
from skill.utils import get_required_skill_groups
from .utils import get_profile_specific_template
from ._template import get_template_data

def generate_headline(position: str, jd: str, profile: dict):
    template_name = get_profile_specific_template(profile)
    if template_name is None:
        return None
    template = get_template_data(template_name)
    return template['headline']

def get_most_proper_position_from_jd(jd):
    skill_groups = get_required_skill_groups(jd, '')
    all_skill_occurences = [ item["skillName"] for sub_list in skill_groups for item in sub_list ]
    candidates = [
        ('architecture', 'Senior Software Engineer'),
        ('frontend', 'Senior Front End Engineer'),
        ('backend', 'Senior Full Stack Engineer'),
        ('mobile', 'Senior Mobile Developer'),
    ]
    if len(all_skill_occurences) == 0:
        return candidates[0][1]
    weighted_skills = [ {"skill_name": item, "weight": 1} for item in all_skill_occurences ]
    max_centrality = 0
    max_position = None
    for candidate in candidates:
        centrality = similarity_n1(weighted_skills, {"skill_name": candidate[0], "weight": 1})
        print(candidate[1], centrality)
        if centrality > max_centrality:
            max_position = candidate[1]
            max_centrality = centrality
    return max_position