import yaml
import random

DB_COUNT = 2

def get_sentence_db(profile: any):
    random.seed(f"{profile['first-name']} {profile['last-name']}")
    selected_db_index = random.randint(1, DB_COUNT)
    filepath = f'assets/sentences/_db{selected_db_index}.yaml'
    print('selected sdb', selected_db_index)
    with open(filepath, "r") as stream:
        sentence_db = yaml.safe_load(stream)
        return sentence_db
    return None