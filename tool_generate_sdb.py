import yaml
from ai import inject_variables_to_content, generate_ai_text
import re

prompt_template = '''Refactor the below resume sentences of software engineer to look professionally.
(write the answers only and don't change the {} template strings)

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

  sub_lines = original[start_index:end_index]
  lines_left = [ (index, line) for index, line in enumerate(sub_lines) ]
  finalized_lines = [''] * len(lines_left)
  while True:
    print('generating chunk', chunk_index, f'({len(lines_left)})')
    sub_text = [ ('- ' + line) for line in '\n'.join([ line[1] for line in lines_left]) ]
    variables = { 'sentences': sub_text }
    prompt = inject_variables_to_content(prompt_template, variables)

    new_content = generate_ai_text(prompt, temperature=1.2)
    new_lines = [ line for line in new_content.split('\n') if len(line.strip()) > 0 ]
    for i in range(len(new_lines)):
      new_line = new_lines[i]
      if new_line.startswith('- '):
        new_lines[i] = new_line[2:]
      elif new_line.startswith('**'):
        new_lines[i] = new_line[2:-2]
      elif re.match('^[\\d]+\\. ', new_line):
        space_index = new_line.index(' ')
        new_lines[i] = new_line[space_index + 1:]
    if len(new_lines) == len(lines_left):
      same_lines = []
      for index, new_line in enumerate(new_lines):
        if new_line == lines_left[index][1]:
          same_lines.append(lines_left[index])
        else:
          finalized_lines[lines_left[index][0]] = new_line
      if len(same_lines) == 0:
        break
      lines_left = same_lines

  with open(f'_sdb_chunks/chunk{chunk_index}.txt', 'w') as file:
    finalized_content = '\n'.join(finalized_lines)
    file.write(finalized_content)
  chunk_index += 1
