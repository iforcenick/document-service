import pymongo
from skill.utils import get_highlighted_positions, get_highlighted_blockers, get_skill_list
from tqdm import tqdm

config_path = './highlightthis_config'

client = pymongo.MongoClient(f"mongodb://root:innovation%21@127.0.0.1:27017/jobdb?authSource=admin")
db = client.jobdb
job_collection = db.jobs

skill_map = get_skill_list()
good_word_map = {}
soso_word_map = {}
bad_word_map = {}
non_block_word_map = {}
block_word_map = {}

job_count = int(job_collection.count_documents({"pageData.description": {"$not": {"$eq": None}}}))
jobs = job_collection.find({"pageData.description": {"$not": {"$eq": None}}})

for job in tqdm(jobs, desc="Analysing: ", total=job_count):
  skills = get_highlighted_positions(job["pageData"]["description"], job["position"])
  for skill in skills:
    skill_meta = skill_map[skill[1]]
    familarity = skill_meta['familarity']
    word_map = None
    if familarity >= 8:
      word_map = good_word_map
    elif familarity >= 4:
      word_map = soso_word_map
    else:
      word_map = bad_word_map
    word_map[skill[0].lower().strip()] = True

  blockers = get_highlighted_blockers(job["pageData"]["description"], job["position"])
  for blocker in blockers:
    [found, blockerType] = blocker
    word_map = None
    if blockerType == 'Remote':
      word_map = non_block_word_map
    else:
      word_map = block_word_map
    word_map[found.lower().strip()] = True

with open(f'{config_path}/good.txt', 'w') as f:
  value_text = '\n'.join(good_word_map.keys())
  f.write(value_text)

with open(f'{config_path}/soso.txt', 'w') as f:
  value_text = '\n'.join(soso_word_map.keys())
  f.write(value_text)

with open(f'{config_path}/bad.txt', 'w') as f:
  value_text = '\n'.join(bad_word_map.keys())
  f.write(value_text)

with open(f'{config_path}/non_block.txt', 'w') as f:
  value_text = '\n'.join(non_block_word_map.keys())
  f.write(value_text)

with open(f'{config_path}/block.txt', 'w') as f:
  value_text = '\n'.join(block_word_map.keys())
  f.write(value_text)