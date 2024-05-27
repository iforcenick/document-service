import yaml
from ai import inject_variables_to_content, generate_ai_text

prompt_template = '''Rewrite each of the below resume sentence professionally using strong action words.

{{sentences}}
'''

with open('assets/sentences/_db.yaml', "r") as stream:
  raw_text = stream.read()

original = []
with open('assets/sentences/_db.yaml', "r") as stream:
  sentence_db = yaml.safe_load(stream)
  for sentence in sentence_db:
    content = sentence['content']
    original.append(content)

with open('_db_new_raw.txt', 'r') as file:
  new_content = file.read()
new_contents = [ line for line in new_content.split('\n') if len(line.strip()) > 0 ]

print(len(original))
for index, original_sentence in enumerate(original):
  print(original_sentence)
  print(new_contents[index])
  print()
  raw_text = raw_text.replace(original_sentence, new_contents[index])
with open('_db_new.yaml', 'w') as file:
  file.write(raw_text)