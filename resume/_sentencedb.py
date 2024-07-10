import yaml
import random
import os

DB_COUNT = 2

def get_sentence_db(profile: dict):
    name_basis = f"{profile['first-name'].lower()}_{profile['last-name'].lower()}"
    db_path = None
    specific_profile_db_path = f"assets/sentences/db_{name_basis}.yaml"
    if os.path.exists(specific_profile_db_path):
        db_path = specific_profile_db_path
    else:
        random.seed(name_basis)
        selected_db_index = random.randint(1, DB_COUNT)
        db_path = f'assets/sentences/db_{selected_db_index}.yaml'
        print('selected sdb', selected_db_index)
    with open(db_path, "r") as stream:
        sentence_db = yaml.safe_load(stream)
        return sentence_db
    return None