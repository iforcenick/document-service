import yaml
import os

with open('_db.yaml', "r") as stream:
  raw_text = stream.read()

original = []
with open('_db.yaml', "r") as stream:
  sentence_db = yaml.safe_load(stream)
  for sentence in sentence_db:
    content = sentence['content']
    original.append(content)

new_contents = []
chunk_index = 0
while True:
  chunk_file_name = f'_sdb_chunks/chunk{chunk_index}.txt'
  if not os.path.exists(chunk_file_name):
    break
  with open(chunk_file_name, 'r') as file:
    new_content = file.read()
    new_contents.extend(new_content.split('\n'))
  chunk_index += 1

print('sentence count:', len(new_contents))

for index, original_sentence in enumerate(original):
  generated_line = new_contents[index]
  print(original_sentence)
  print(generated_line)
  print()
  raw_text = raw_text.replace(original_sentence, generated_line)
with open('_db_new.yaml', 'w') as file:
  file.write(raw_text)