import yaml

matrix = None
with open('assets/skill/skill_occurence.yaml', 'r') as file:
  matrix = yaml.safe_load(file)