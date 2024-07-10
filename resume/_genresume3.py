import re
from datetime import datetime
from .utils import gen_linkedin_default, gen_github_default, gen_website_default, gen_phone_default, replace_images, replace_mock_images

def _replace_data(document, headline, summary, history, skill_section_headers, skill_section_contents, profile, pipeline):
  sentence_slot_index = 0
  position_slot_index = 0
  company_slot_index = 0
  duration_slot_index = 0
  category_slot_index = 0
  skill_slot_index = 0

  all_sentences = []
  for company_item in history:
     all_sentences.extend(company_item['sentences'])

  def _interpolate_data(match_obj):
      nonlocal sentence_slot_index, position_slot_index, company_slot_index, duration_slot_index, category_slot_index, skill_slot_index, pipeline
      match = match_obj.group(1)
      if match == "name":
          return f"{profile['first-name']} {profile['last-name']}"
      if match == "email":
          return profile['email']
      if match == "location":
          return f"{profile['city']}, {profile['state-abbr']}"
      if match == "LK":
          return pipeline['linkedin'](profile['linkedin'])
      if match == "phone":
          return pipeline['phone'](profile['phone-number'])
      if match == "website":
          return pipeline['website'](profile['website'])
      if match == "GH":
          return pipeline['github'](profile['github'])
      if match == "headline":
          return headline
      if match == "summary":
          return summary
      if match == "position":
          position_slot_index += 1
          sentence_slot_index = 0
          # return history[position_slot_index - 1]['position']
          return profile[f"position-title-{position_slot_index}"]
      if match == "company":
          company_slot_index += 1
          return profile[f"company-name-{company_slot_index}"]
      if match == "duration":
          duration_slot_index += 1
          start_date_str = profile[f"company-start-date-{duration_slot_index}"]
          end_date_str = profile[f"company-end-date-{duration_slot_index}"]
          return pipeline['duration'](start_date_str, end_date_str)
      if match == "university-name":
          return profile['university-name']
      if match == "university-degree":
          return profile['university-degree']
      if match == "university-major":
          return profile['university-major']
      if match == "university-duration":
          start_date_str = profile['university-start-date']
          end_date_str = profile['university-end-date']
          return pipeline['university-duration'](start_date_str, end_date_str)
      if match == "sentence":
          current_sentence = all_sentences[sentence_slot_index]
          sentence_slot_index += 1
          return current_sentence
      if match == "category":
          category_slot_index += 1
          return skill_section_headers[category_slot_index - 1]
      if match == "skill":
          skill_slot_index += 1
          return " • ".join(skill_section_contents[skill_slot_index - 1])
      return match
  
  for paragraph in document.paragraphs:
    for run in paragraph.runs:
      if re.match("{(.*?)}", run.text):
        replaced_text = re.sub("{(.*?)}", _interpolate_data, run.text)
        if replaced_text != "":
          run.text = replaced_text
        else:
          paragraph._element.getparent().remove(paragraph._element)
  for table in document.tables:
    for row_index, row in enumerate(table.rows):
      if row_index >= len(skill_section_headers):
        row._element.getparent().remove(row._element)
      else:
        for cell in row.cells:
          for paragraph in cell.paragraphs:
            for run in paragraph.runs:
              if re.match("{(.*?)}", run.text):
                run.text = re.sub("{(.*?)}", _interpolate_data, run.text)
  # replace_mock_images(document)
    
def generate(document, headline, summary, history, skill_section_headers, skill_section_contents, profile):
  def gen_duration(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, '%m/%d/%Y') if start_date_str != "" else None
    end_date = datetime.strptime(end_date_str, '%m/%d/%Y') if end_date_str != "" else None
    st = start_date.strftime('%Y.%-m') if start_date is not None else "Present"
    ed = end_date.strftime('%Y.%-m') if end_date is not None else "Present"
    return f'{st} - {ed}'
  def gen_edu_duration(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, '%m/%d/%Y') if start_date_str != "" else None
    end_date = datetime.strptime(end_date_str, '%m/%d/%Y') if end_date_str != "" else None
    st = start_date.strftime('%Y')
    ed = end_date.strftime('%Y')
    return f'{st} - {ed}'
  pipeline = {
    "duration": gen_duration,
    "university-duration": gen_edu_duration,
    "linkedin": gen_linkedin_default,
    "website": gen_website_default,
    "github": gen_github_default,
    "phone": gen_phone_default,
  }
  _replace_data(document, headline, summary, history, skill_section_headers, skill_section_contents, profile, pipeline)