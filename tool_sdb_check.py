from resume._sentencedb import get_sentence_db_from_path
from resume.utils import generate_sentences_from_template
import re
from dotenv import load_dotenv
load_dotenv()

sentence_db = get_sentence_db_from_path('_db_new.yaml')
for index, sentence_template in enumerate(sentence_db):
  print(sentence_template['content'])
  new_sentences = generate_sentences_from_template(sentence_template)
  for new_sentence in new_sentences:
    content = new_sentence['content']
    if re.search('{(.*?)}', content):
      print('Invalid!')
      exit(0)
  else:
    print('Ok')
  print()
print('All OK!')
