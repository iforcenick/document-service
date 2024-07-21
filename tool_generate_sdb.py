import yaml
from ai import inject_variables_to_content, generate_ai_text
import re

prompt_template = '''Refactor the below resume sentences of software engineer to look professionally.
(write the answers only)

{{sentences}}
'''
CHUNK_COUNT = 10

with open('_db.yaml', "r") as stream:
  raw_text = stream.read()

original = []
with open('_db.yaml', "r") as stream:
  sentence_db = yaml.safe_load(stream)
  for sentence in sentence_db:
    content = sentence['content']
    original.append(content)


chunk_index = 0

for i in range(0, len(original), CHUNK_COUNT):
  start_index = i
  end_index = min(i + CHUNK_COUNT, len(original))
  line_count = end_index - start_index

  sub_lines = original[start_index:end_index]
  sub_text = [ ('- ' + line) for line in '\n'.join(sub_lines) ]
  variables = {
    'sentences': sub_text
  }
  prompt = inject_variables_to_content(prompt_template, variables)

  normalized_content = ''
  while True:
    print('generating chunk', chunk_index)
    new_content = generate_ai_text(prompt, temperature=1.2)
    new_lines = [ line for line in new_content.split('\n') if len(line.strip()) > 0 ]
    for i in range(len(new_lines)):
      new_line = new_lines[i]
      if new_line.startswith('- '):
        new_lines[i] = new_line[2:]
      elif re.match('^[\\d]+\\. ', new_line):
        space_index = new_line.index(' ')
        new_lines[i] = new_line[space_index + 1:]
    if len(new_lines) == line_count:
      normalized_content = '\n'.join(new_lines)
      break

  with open(f'_sdb_chunks/chunk{chunk_index}.txt', 'w') as file:
    file.write(normalized_content)
  chunk_index += 1
