import yaml
from ai import inject_variables_to_content, generate_ai_text

prompt_template = '''Generate the resume sentences that has the same meaning as each of the below resume sentence professionally.

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


original_text = [ ('- ' + line) for line in '\n'.join(original) ]
variables = {
  'sentences': original_text
}
prompt = inject_variables_to_content(prompt_template, variables)
new_content = generate_ai_text(prompt, temperature=1.0)
print(new_content)
with open('_db_new_raw.txt', 'w') as file:
  file.write(new_content)
