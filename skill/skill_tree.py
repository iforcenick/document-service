from .utils import normalize_skill_name, get_skill_list
from functools import reduce

import time

root_cache = None
nodes_cache = []
last_tree_built_time = 0

class SkillNode:
    def __init__(self, skill_name="", data=None, parents=[], children=[]) -> None:
        self.data = data
        self.skill_name = skill_name
        self.parents = parents.copy()
        self.children = children.copy()


def _compile_skill_tree():
    skills = get_skill_list()
    root = SkillNode()
    nodes = {}
    normalized = {}
    
    def compile_skill_item(skill_name):
        normalized_skill_name = normalize_skill_name(skill_name)
        skill_data = skills[skill_name]
        if normalized_skill_name in nodes:
            return nodes[normalized_skill_name]
        
        node = SkillNode(skill_name, skill_data)
        nodes[normalized_skill_name] = node
        if skill_data["parent"] is None:
            root.children.append(node)
            node.parents.append(root)
        elif type(skill_data["parent"]) == str:
            parent_node = compile_skill_item(normalized[skill_data["parent"]])
            node.parents.append(parent_node)
            parent_node.children.append(node)
        else:
            for parent_name in skill_data["parent"]:
                parent_node = compile_skill_item(normalized[parent_name])
                node.parents.append(parent_node)
                parent_node.children.append(node)
        return node
    
    for skill_name in skills:
        normalized[normalize_skill_name(skill_name)] = skill_name
    
    for skill_name in skills:
        compile_skill_item(skill_name)
    return (root, nodes)

def get_skill_tree():
    global root_cache, nodes_cache, last_tree_built_time

    current_timestamp = time.time()
    if root_cache is None or current_timestamp - last_tree_built_time > 10:
        (root_cache, nodes_cache) = _compile_skill_tree()
        last_tree_built_time = current_timestamp
    return (root_cache, nodes_cache)
