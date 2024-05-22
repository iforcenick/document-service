import yaml

sentence_db = None

with open('assets/sentences/_db.yaml', "r") as stream:
    sentence_db = yaml.safe_load(stream)