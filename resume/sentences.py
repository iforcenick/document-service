from skill.utils import normalize_skill_name, get_required_skill_groups
from skill.skill_tree import get_skill_tree
from .utils import get_most_relevant_template, expand_weighted_skills_into_full_list
from ._template import get_template_data
from ._sentencedb import sentence_db
from job_familarity_model.word2vec import similarity_nm
import re
import time
from datetime import datetime
import random

def generate_sentences_from_template(template):
    exchange = template.get("exchange", {})
    sentences = []

    replacement = []

    def do_replacement(match_obj):
        nonlocal replacement
        value = replacement[0]
        replacement.pop(0)
        return value

    def _recursive_generate(content, relations, exchange_keys):
        nonlocal exchange, replacement, sentences
        if len(exchange_keys) == 0:
            weighted_relations = []
            for relation in relations:
                if type(relation) == list:
                    weighted_relations.append({
                        "skill_name": relation[0],
                        "weight": float(relation[1]),
                    })
                else:
                    weighted_relations.append({
                        "skill_name": relation,
                        "weight": 1,
                    })
            sentences.append({
                "content": content,
                "relations": weighted_relations
            })
            return
        front_key = exchange_keys[0]
        keys_left = exchange_keys[1:]

        replacements = exchange[front_key]
        for rep in replacements:
            replacement = rep[0][:]
            replaced = re.sub("{" + front_key + "}", do_replacement, content)
            relation_ext = relations[:]
            relation_ext.extend(list(filter(lambda x: x is not None, rep[1])))
            _recursive_generate(replaced, relation_ext, keys_left)
    content = template["content"]
    relations = template["relations"]
    _recursive_generate(content, relations, list(exchange.keys()))
    return sentences
    
def generate_detailed_resume_history(profile: dict, position: str, required_skills, jd: str) -> str:
    (root, nodes) = get_skill_tree()
    template_type = get_most_relevant_template(position, required_skills)
    try:
        template = get_template_data(template_type)
    except:
        return None

    # copy full template data
    history = template["history"]
    final_history = []
    for item in history:
        final_history.append({
            "position": item["position"],
            "sentences": [ sentence.copy() for sentence in item["sentences"] ]
        })
    if len(required_skills) == 0:
        return final_history
    
    # Initialize sentence db usage
    sentence_usage = [ False ] * len(sentence_db)


    skill_category_info = {
        "frontend": { "score": 0.03, "skills": [], "weighted_skills": [], "scale": 1 },
        "backend":  { "score": 0.02, "skills": [], "weighted_skills": [], "scale": 1 },
        "dev":      { "score": 0.01, "skills": [], "weighted_skills": [], "scale": 0.3 },
        "cloud":    { "score": 0, "skills": [], "weighted_skills": [], "scale": 1 },
        "database": { "score": 0, "skills": [], "weighted_skills": [], "scale": 1 },
        "mobile":   { "score": 0, "skills": [], "weighted_skills": [], "scale": 1 },
        "blockchain":   { "score": 0, "skills": [], "weighted_skills": [], "scale": 1.3 }
    }
    # Generate skill section
    skill_groups = get_required_skill_groups(jd, position)
    all_skill_occurences = [ item["skillName"] for sub_list in skill_groups for item in sub_list ]

    # Generate a weighted skill array with all skills in it.
    all_weighted_skills = []
    for required_skill in required_skills:
        occurence_count = len([ skill_name for skill_name in all_skill_occurences if skill_name == required_skill["skill"] ])
        all_weighted_skills.append({
            "skill_name": required_skill["skill"],
            "weight": occurence_count * required_skill['affect']
        })
    all_expanded = expand_weighted_skills_into_full_list(all_weighted_skills)

    # Group CLEARLY CATEGORIZED required skills by category into skill_category_info
    for required_skill in required_skills:
        category = required_skill['category']
        if type(category) == list:
            continue
        skill_category_info[category]["skills"].append(required_skill["skill"])
        occurence_count = len([ skill_name for skill_name in all_skill_occurences if skill_name == required_skill["skill"] ])
        skill_category_info[category]["weighted_skills"].append({
            "skill_name": required_skill["skill"],
            "weight": occurence_count * required_skill['affect']
        })

    # Temporarily measure the importance of every category ( with obvious skills ) to put weight for UNOBVIOUS CATEGORIZED skills
    for category in skill_category_info:
        score = 0
        if len(skill_category_info[category]["skills"]) > 0:
            category_expanded = expand_weighted_skills_into_full_list(skill_category_info[category]["weighted_skills"])
            score = similarity_nm(all_expanded, category_expanded) ** 10
        skill_category_info[category]["score"] = score * skill_category_info[category]["scale"]
        print("temporary category importance: ", category, score)
    
    # Group UNCLEAR CATEGORIZED required skills into skill_category_info with pre-measured weight
    for required_skill in required_skills:
        categories = required_skill['category']
        if type(categories) != list:
            continue
        category_weight_sum = sum([ skill_category_info[category]["score"] for category in categories ])
        for category in categories:
            skill_category_info[category]["skills"].append(required_skill["skill"])
            occurence_count = len([ skill_name for skill_name in all_skill_occurences if skill_name == required_skill["skill"] ])
            current_category_weight = skill_category_info[category]["score"]
            if current_category_weight == 0 and category_weight_sum > 0:
                continue
            portion = 0
            if category_weight_sum > 0:
                portion = current_category_weight / category_weight_sum
            else:
                portion = 1.0 / len(categories)
            skill_category_info[category]["weighted_skills"].append({
                "skill_name": required_skill["skill"],
                "weight": occurence_count * portion * required_skill['affect']
            })
    
    # Finally measure the importance of every category with all skills involved
    #  by calculating the similarity between total occurence list and the required skills certain category
    for category in skill_category_info:
        score = 0
        # if len(skill_category_info[category]["skills"]) > 0:
        #     category_expanded = expand_weighted_skills_into_full_list(skill_category_info[category]["weighted_skills"])
        #     score = similarity_nm(all_expanded, category_expanded) ** 10
        score = sum([ weighted_skill['weight'] for weighted_skill in skill_category_info[category]["weighted_skills"] ])
        skill_category_info[category]["score"] = score * skill_category_info[category]["scale"]
        print("final category importance: ", category, score)
    
    # Remove the DEV category as we don't need that essentially.
    del skill_category_info["dev"]

    skill_categories = [ (skill_category_info[item]["score"], item) for item in skill_category_info ]

    current_category_progress = [0] * len(skill_categories)
    # Get total exchangable sentence count
    total_sentence_count = 0
    for group in history:
        for sentence in group['sentences']:
            if "exchangable" in sentence and sentence['exchangable'] is True:
                total_sentence_count += 1
    total_category_score = sum([ cat[0] for cat in skill_categories ])
    
    # Group skills by category and add weight to every skill using the importance level
    categorized_weighted_skill_names = []
    for category in skill_categories:
        categorized_weighted_skill_names = [ skill_category_info[category[1]]["weighted_skills"] for category in skill_categories ]
        
    selected_categories = []
    for group_index, group in enumerate(final_history):
        sentences = group['sentences']
        end_date_str = profile[f'company-end-date-{group_index + 1}']
        limit_year = datetime.strptime(end_date_str, '%m/%d/%Y').year if end_date_str != "" else 2100
        for (sentence_index, sentence) in enumerate(sentences):
            # Select exchangable slots
            if "exchangable" not in sentence or sentence["exchangable"] is False:
                continue

            # Determine in which category should select the sentence
            current_category_index = 0
            max_remain = 0
            remain_metadata = []
            while True:
                remain_metadata = []
                for index, category in enumerate(skill_categories):

                    # Get last sequent sentence count for the same category
                    # For decremental calculation
                    sequent_count = 0
                    selected_categories_len = len(selected_categories)
                    for last in range(selected_categories_len):
                        if selected_categories[selected_categories_len - last - 1] != index:
                            break
                        sequent_count += 1
                    
                    # Get progress of the current category
                    progress = current_category_progress[index] / total_sentence_count * total_category_score
                    remain = (category[0] - progress) * (0.8 ** sequent_count)
                    remain_metadata.append({
                        "category": category[1],
                        "value": remain
                    })
                    if max_remain < remain:
                        current_category_index = index
                        max_remain = remain
                if max_remain > 0:
                    break
                current_category_progress = [0] * len(skill_categories)

            current_category_progress[current_category_index] += 1
            selected_categories.append(current_category_index)

            for index, category in enumerate(skill_categories):
                progress = current_category_progress[index] / total_sentence_count * total_category_score
                print(category[1], progress)
            
            best_candidate_sentence = {
                "similarity": 0,
                "index": 0
            }

            # Add non-related category skills as the additional factor of sentence selection process
            target_skill_group = [ weighted_skill.copy() for weighted_skill in categorized_weighted_skill_names[current_category_index]]
            for weighted_skill in target_skill_group:
                weighted_skill['weight'] *= 3
            for category_index, other_weighted_skill_names in enumerate(categorized_weighted_skill_names):
                if category_index == current_category_index:
                    continue
                for weighted_skill_name in other_weighted_skill_names:
                    target_skill_group.append(weighted_skill_name)
            # Generated expanded skill list for target(remaining) skill group
            expanded_target_skills = expand_weighted_skills_into_full_list(target_skill_group)

            for index, sentence_template in enumerate(sentence_db):
                if sentence_usage[index] is True:
                    continue
                new_sentence_quality = sentence_template["quality"]
                new_sentences = generate_sentences_from_template(sentence_template)
                for new_sentence in new_sentences:
                    weighted_relations = new_sentence["relations"]
                    for weighted_relation in weighted_relations:
                        relation = weighted_relation['skill_name']
                        if relation not in nodes:
                            continue
                        if nodes[relation].data["release"] > limit_year:
                            break
                    else:
                        expanded_relations = expand_weighted_skills_into_full_list(weighted_relations, True)
                        # Calculate similarity between relational skills and target skills
                        vector_similarity = similarity_nm(expanded_target_skills, expanded_relations) ** 2
                        # Consider manual sentence quality
                        similarity = vector_similarity * new_sentence_quality
                        if best_candidate_sentence["similarity"] < similarity:
                            best_candidate_sentence = {
                                "similarity": similarity,
                                "vector_similarity": float(vector_similarity),
                                "sentence_quality": new_sentence_quality,
                                "among": target_skill_group,
                                "relations": weighted_relations,
                                "content": new_sentence["content"],
                                "index": index
                            }

            best_sentence_index = best_candidate_sentence["index"]
            sentence_usage[best_sentence_index] = True

            for weighted_skill in categorized_weighted_skill_names[current_category_index]:
                for relation in best_candidate_sentence["relations"]:
                    if normalize_skill_name(relation['skill_name']) == normalize_skill_name(weighted_skill['skill_name']):
                        weighted_skill['weight'] /= 2
                        break
            sentences[sentence_index] = {
                "content": best_candidate_sentence["content"],
                "metadata": best_candidate_sentence,
                "remain": remain_metadata
            }
    
    return final_history

def generate_resume_history(profile: dict, position: str, required_skills, jd: str) -> list:
    detailed_history = generate_detailed_resume_history(profile, position, required_skills, jd)
    history = []
    for group in detailed_history:
        sentences = [ sentence["content"] for sentence in group["sentences"] ]
        history.append({
            "position": group['position'],
            "sentences": sentences,
        })
    return history