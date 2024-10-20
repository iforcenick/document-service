import re
import base64
import os
from .config import COMPANY_LOGOS

def get_profile_specific_template(profile: dict):
  template_type = f"{profile['first-name'].lower()}_{profile['last-name'].lower()}"
  if os.path.exists(f"assets/sentences/template_{template_type}.yaml"):
    return template_type
  return None

def get_profile_experience_description(profile: dict):
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
      achievement = profile[f'achievement-{position_index}']
      experience += f'{position_index}. {position_title} at {company_name} company from {company_start_date} to {company_end_date}\n'
      for line in achievement:
        experience += f'- {line}\n'
      experience += '\n'
      position_index += 1
  return experience

def get_most_relevant_template(position: str, required_skills: any):
    if re.search("full(.*?)stack", position, re.IGNORECASE):
        return "fullstack"
    if re.search("(front(.*?)end)|react|angular|UI|UX|javascript|typescript|FE|Vue|user interface", position, re.IGNORECASE):
        if re.search("react native", position, re.IGNORECASE):
            return "mobile"
        if re.search("react", position, re.IGNORECASE):
            return "react"
        if re.search("angular", position, re.IGNORECASE):
            return "angular"
        if re.search("vue", position, re.IGNORECASE):
            return "vue"
        for required_skill in required_skills:
            if required_skill["skill"] == "React":
                return "react"
            if required_skill["skill"] == "Angular":
                return "angular"
            if required_skill["skill"] == "Vue":
                return "vue"
        return "react"
    if re.search("mobile", position, re.IGNORECASE):
        return "mobile"
    return "software"

def select_skill_section_items(nodes):
    selected_skills = []
    line_length = 0
    for node in nodes:
        if node.data["level"] >= 7:
            selected_skills.append(node.skill_name)
            line_length += len(node.skill_name)
    return (selected_skills, line_length)

def gen_linkedin_default(url):
  return url[12:]
def gen_github_default(url):
  return url[8:]
def gen_website_default(url):
  return url[8:]
def gen_phone_default(phone):
  return f"+1 ({phone[0:3]}) {phone[3:6]} {phone[6:]}"

def replace_images(document, profile, logo_map):
  image_rels = []
  rels = document.part.rels
  for rel_id in rels:
    if "image" in rels[rel_id].reltype:
      image_rels.append(rels[rel_id])
  for rel_index, rel in enumerate(image_rels):
    if rel_index not in logo_map:
      continue
    section_id = logo_map[rel_index]
    logo_key  = section_id.replace('company', 'company-name-') if section_id.startswith('company') else 'university-name'
    logo_file_name = COMPANY_LOGOS[profile[logo_key]]
    logo_path = f'assets/company_logos/{logo_file_name}'
    with open(logo_path, "rb") as image_file:
      image_content = base64.b64encode(image_file.read()).decode("utf-8")
    rel.target_part._blob = base64.b64decode(image_content)

def replace_mock_images(document):
  mock_images = {
    0: '_0.png',
    1: '_1.png',
    2: '_2.png',
    3: '_3.png',
    4: '_4.png',
    5: '_5.png',
    6: '_6.png',
    7: '_7.png',
    8: '_8.png',
    9: '_9.png',
  }
  image_rels = []
  rels = document.part.rels
  for rel_id in rels:
    if "image" in rels[rel_id].reltype:
      image_rels.append(rels[rel_id])
  for rel_index, rel in enumerate(image_rels):
    if rel_index not in mock_images:
      continue
    logo_path = f'assets/company_logos/{mock_images[rel_index]}'
    with open(logo_path, "rb") as image_file:
      image_content = base64.b64encode(image_file.read()).decode("utf-8")
    rel.target_part._blob = base64.b64decode(image_content)

def get_weighted_relations(relations):
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
    return weighted_relations

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
            weighted_relations = get_weighted_relations(relations)
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
    relations = template.get("relations", [])
    exchange_keys = list(exchange.keys())
    if len(exchange_keys) == 0:
        return [{
            "content": content,
            "relations": get_weighted_relations(relations)
        }]
    _recursive_generate(content, relations, exchange_keys)
    return sentences