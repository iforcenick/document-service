import re
import base64
from .config import RESUME_TEMPLATE_PATH

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

def expand_weighted_skills_into_full_list(weighted_skills):
    if len(weighted_skills) == 0:
        return []
    min_weight = min([ weighted_skill['weight'] for weighted_skill in weighted_skills ])

    expand_scale = None

    if min_weight >= 1:
        expand_scale = 2
    elif min_weight >= 0.5:
        expand_scale = 1.0 / min_weight * 2
    else:
        expand_scale = 1.0 / min_weight
    expand_scale *= 3

    expanded = []
    for weighted_skill in weighted_skills:
        weight = weighted_skill['weight'] * expand_scale
        count = round(weight)
        expanded.extend([weighted_skill['skill_name']] * count)
    return expanded

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
    logo_key = logo_map[rel_index]
    logo_path = f'assets/company_logos/{profile[logo_key]}'
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
    logo_path = f'{RESUME_TEMPLATE_PATH}/company_logos/{mock_images[rel_index]}'
    with open(logo_path, "rb") as image_file:
      image_content = base64.b64encode(image_file.read()).decode("utf-8")
    rel.target_part._blob = base64.b64decode(image_content)