from openai import OpenAI
import re
from env import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def inject_variables_to_content(content: str, variables):
  matches = re.findall('{{(.*?)}}', content)
  for match in matches:
    variable = variables[match]
    if type(variable) == list:
      variable = '\n'.join(variable)
    content = content.replace('{{' + match + '}}', variable)
  return content

def generate_ai_text(prompt: str, temperature=0.8):
  chat_completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
    temperature=temperature
  )
  try:
    message = chat_completion.choices[0].message.content
    return message
  except:
    return None