import yaml

def get_sentence_db(profile: any):
    if profile['first-name'] == 'Omer':
        filepath = 'assets/sentences/_db2.yaml'
    else:
        filepath = 'assets/sentences/_db.yaml'
    with open(filepath, "r") as stream:
        sentence_db = yaml.safe_load(stream)
        return sentence_db
    return None