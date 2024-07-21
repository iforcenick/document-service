import yaml

DB_COUNT = 2

def get_sentence_db_from_path(db_path: str):
    with open(db_path, "r") as stream:
        sentence_db = yaml.safe_load(stream)
        return sentence_db

def get_sentence_db(profile: dict):
    name_basis = f"{profile['first-name'].lower()}_{profile['last-name'].lower()}"
    db_path = f"assets/sentences/db_{name_basis}.yaml"
    return get_sentence_db_from_path(db_path)