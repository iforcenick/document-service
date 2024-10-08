from urllib import request, parse
import json
from env import PARSE_ENGINE_URL

def normalize_skill_name(skill_name):
    return skill_name.lower().replace(" ", "").replace("-", "").replace("*", "").replace("/", "").replace(".", "").strip()

def get_required_skills(jd: str, position: str = ""):
    wrapped_jd = f"<p>{position}<br/>{position}</p>{jd}"
    request_body = parse.urlencode({"jd": wrapped_jd}).encode()
    req = request.Request(f'{PARSE_ENGINE_URL}/skill/measure', data=request_body) # this will make the method "POST"
    response = request.urlopen(req)
    return json.loads(response.read())

def get_required_skill_groups(jd: str, position: str = ""):
    wrapped_jd = f"<p>{position}<br/>{position}<br/>{position}<br/>{position}</p>{jd}"
    request_body = parse.urlencode({"jd": wrapped_jd}).encode()
    req = request.Request(f'{PARSE_ENGINE_URL}/skill/measure/groups', data=request_body) # this will make the method "POST"
    response = request.urlopen(req)
    return json.loads(response.read())


def get_skill_list():
    req = request.Request(f'{PARSE_ENGINE_URL}/skill/list', method="GET") # this will make the method "POST"
    response = request.urlopen(req)
    return json.loads(response.read())

def get_highlighted_positions(jd: str, position: str = ""):
  wrapped_jd = f"<p>{position}<br/>{position}</p>{jd}".encode('ascii', 'ignore').decode('utf-8')
  request_body = parse.urlencode({"jd": wrapped_jd}).encode()
  req = request.Request(f'{PARSE_ENGINE_URL}/skill/highlights/tagged', data=request_body) # this will make the method "POST"
  response = request.urlopen(req)
  occurences = json.loads(response.read())
  highlights = []
  for occ in occurences:
    highlight = wrapped_jd[occ[0]:occ[1]]
    highlights.append([highlight, occ[2]])
  return highlights

def get_highlighted_blockers(jd: str, position: str = ""):
  wrapped_jd = f"<p>{position}<br/>{position}</p>{jd}".encode('ascii', 'ignore').decode('utf-8')
  request_body = parse.urlencode({"jd": wrapped_jd}).encode()
  req = request.Request(f'{PARSE_ENGINE_URL}/blocker/highlights/tagged', data=request_body) # this will make the method "POST"
  response = request.urlopen(req)
  occurences = json.loads(response.read())
  highlights = []
  for occ in occurences:
    highlight = wrapped_jd[occ[0]:occ[1]]
    highlights.append([highlight, occ[2]])
  return highlights

def get_allowed_nodes(root_skill_name, banned_skill_names, nodes):
    def _iterate_children(root_node, banned_nodes) -> list:
        allowed_nodes = [ root_node ]
        for child_skill in root_node.children:
            child_skill_name = normalize_skill_name(child_skill.skill_name)
            if child_skill_name in banned_skill_names:
                continue
            allowed_nodes.extend(_iterate_children(nodes[child_skill_name], banned_nodes))
        return allowed_nodes
    return _iterate_children(nodes[root_skill_name], [ nodes[skill_name] for skill_name in banned_skill_names ])