import re
from datetime import datetime
from autobid.ai import generate_ai_answer, inject_variables_to_content

prompt_template = '''
My name is {{first-name}} and I am a {{headline}} with more than 10 years of experience.
Write a conversational cover letter for a job application as a {{position}} at {{company}} using the below job description as a reference.

{{jd}}
'''

def gen_linkedin_default(url):
  return url[12:]
def gen_github_default(url):
  return url[8:]
def gen_website_default(url):
  return url[8:]
def gen_phone_default(phone):
  return f"{phone[0:3]}-{phone[3:6]}-{phone[6:]}"

def _replace_data(document, position, jd, company, headline, profile, pipeline):
  def _interpolate_data(match_obj):
      nonlocal pipeline
      match = match_obj.group(1)
      if match == "FN":
          return profile['first-name']
      if match == "LN":
          return profile['last-name']
      if match == "email":
          return profile['email']
      if match == "address":
          return profile['address-line']
      if match == "city":
          return profile['city']
      if match == "state":
          return profile['state']
      if match == "zipcode":
          return profile['zip-code']
      if match == "LK":
          return pipeline['linkedin'](profile['linkedin'])
      if match == "phone":
          return pipeline['phone'](profile['phone-number'])
      if match == "today":
          today = datetime.now()
          return today.strftime('%B %-d, %Y')
      if match == "target":
          if len(company) > 0:
             return f'{company} hiring team'
          return 'hiring manager'
      if match == "headline":
          return headline
      if match == "content":
          variables = {
             "first-name": profile["first-name"],
             "headline": headline,
            "position": position,
            "company": company if company != "" else "a company",
            "jd": jd,
          }
          prompt = inject_variables_to_content(prompt_template, variables)
          print(prompt)
          return generate_ai_answer(prompt)
      return match
  
  for paragraph in document.paragraphs:
    for run in paragraph.runs:
        if re.match("{(.*?)}", run.text):
            replaced_text = re.sub("{(.*?)}", _interpolate_data, run.text)
            if replaced_text != "":
              run.text = replaced_text
            else:
                paragraph._element.getparent().remove(paragraph._element)

  txbxs = document.inline_shapes._body.xpath('//w:txbxContent')
  for txbx in txbxs:
    for tx in txbx:
      children = tx.getchildren()
      for child in children:
        if child.text and re.search("{(.*?)}", child.text):
          replaced_text = re.sub("{(.*?)}", _interpolate_data, child.text)
          child.text = replaced_text

  for table in document.tables:
      for row_index, row in enumerate(table.rows):
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        if re.match("{(.*?)}", run.text):
                            run.text = re.sub("{(.*?)}", _interpolate_data, run.text)
    
def generate(document, position, jd, company, headline, profile):
  def gen_duration(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, '%m/%d/%Y') if start_date_str != "" else None
    end_date = datetime.strptime(end_date_str, '%m/%d/%Y') if end_date_str != "" else None
    st = start_date.strftime('%b %Y') if start_date is not None else "Present"
    ed = end_date.strftime('%b %Y') if end_date is not None else "Present"
    return f'{st} - {ed}'
  pipeline = {
    "university-duration": gen_duration,
    "linkedin": gen_linkedin_default,
    "website": gen_website_default,
    "github": gen_github_default,
    "phone": gen_phone_default,
  }
  _replace_data(document, position, jd, company, headline, profile, pipeline)