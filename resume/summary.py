from .utils import get_profile_specific_template, generate_sentences_from_template
from ._template import get_template_data
from job_familarity_model.word2vec import similarity_nm
from skill.utils import get_required_skill_groups

def generate_detailed_summary(position: str, jd: str, profile: dict):
    template_name = get_profile_specific_template(profile)
    if template_name is None:
        return None
    template = get_template_data(template_name)
    summary_template = template['summary']
    possibles = generate_sentences_from_template(summary_template)

    skill_groups = get_required_skill_groups(jd, position)
    target_skill_group = [ {"skill_name": item["skillName"], "weight": 1} for sub_list in skill_groups for item in sub_list ]

    best_candidate_simmary = {
        "similarity": 0,
        "index": 0
    }

    for possible in possibles:
        weighted_relations = possible["relations"]
        # Calculate similarity between relational skills and target skills
        similarity = similarity_nm(target_skill_group, weighted_relations) ** 2
        if best_candidate_simmary["similarity"] <= similarity:
            best_candidate_simmary = {
                "similarity": similarity,
                "vector_similarity": float(similarity),
                "among": target_skill_group,
                "relations": weighted_relations,
                "content": possible["content"],
            }
      
    return best_candidate_simmary

def generate_summary(position: str, jd: str, profile: dict):
    detailed_summary = generate_detailed_summary(position, jd, profile)
    return detailed_summary['content']