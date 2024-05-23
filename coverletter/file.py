# You should install LibreOffice app to enable doc2pdf feature:
# Download here: https://www.libreoffice.org/donate/dl/mac-x86_64/7.5.0/en-US/LibreOffice_7.5.0_MacOS_x86-64.dmg
# Related post:  https://apple.stackexchange.com/questions/80791/command-line-tool-to-convert-doc-and-docx-files-to-pdf
from docx import Document
import os
import uuid
import shutil
import tempfile

from resume.metadata import generate_meta_data
from env import LIBREOFFICE_PATH

from . import _gencoverletter1
from . import _gencoverletter2
from . import _gencoverletter3
from . import _gencoverletter4

# from . import _gencoverletter5

TEMP_PATH = tempfile.gettempdir()

# Extensible array as the templates increase.
coverletter_generators = [
    _gencoverletter1.generate,
    _gencoverletter2.generate,
    _gencoverletter3.generate,
    _gencoverletter4.generate,
    # _gencoverletter5.generate,
]

def _generate_cover_letter_file(position, jd, company, headline, profile, path):
  template_index = profile['cover-letter-template-index'] - 1
  document = Document(f'assets/template/coverletter_{template_index + 1}.docx')
  generate_coverletter = coverletter_generators[template_index]
  generate_coverletter(document, position, jd, company, headline, profile)

  temp_file_id = str(uuid.uuid4())
  temp_docxpath = f'{TEMP_PATH}/{temp_file_id}.docx'
  document.save(temp_docxpath)
  os.chmod(temp_docxpath, 0o777)
  if path.endswith('pdf'):
      temp_pdfpath = f'{TEMP_PATH}/{temp_file_id}.pdf'
      os.system(f'{LIBREOFFICE_PATH} --headless --convert-to pdf --outdir "{TEMP_PATH}" "{temp_docxpath}"')
      os.remove(temp_docxpath)
      shutil.move(temp_pdfpath, path)
  else:
      shutil.move(temp_docxpath, path)
  return os.path.abspath(path)

def generate_cover_letter_file(position: str, required_skills, jd: str, company: str, profile: dict, path: str) -> str:
    ( headline, _ ) = generate_meta_data(position, required_skills)
    _generate_cover_letter_file(position, jd, company, headline, profile, path)

def generate_cover_letter_file_from_jd(jd: str, profile: dict, path: str) -> str:
    _generate_cover_letter_file(None, jd, None, None, profile, path)