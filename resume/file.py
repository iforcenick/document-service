# You should install LibreOffice app to enable doc2pdf feature:
# Download here: https://www.libreoffice.org/donate/dl/mac-x86_64/7.5.0/en-US/LibreOffice_7.5.0_MacOS_x86-64.dmg
# Related post:  https://apple.stackexchange.com/questions/80791/command-line-tool-to-convert-doc-and-docx-files-to-pdf

from docx import Document
import os
import uuid
import shutil
import tempfile

from env import LIBREOFFICE_PATH

from .skillmatrix import generate_skill_matrix
from .sentences import generate_resume_history
from .metadata import generate_meta_data

from . import _genresume1
from . import _genresume2
from . import _genresume3
from . import _genresume4
from . import _genresume5

# Extensible array as the templates increase.
resume_generators = [
    _genresume1.generate,
    _genresume2.generate,
    _genresume3.generate,
    _genresume4.generate,
    _genresume5.generate,
]

TEMP_PATH = tempfile.gettempdir()

def _generate_resume_file(headline, summary, history, skill_section_headers, skill_section_contents, profile, path):
    template_index = profile['resume-template-index'] - 1
    document = Document(f'assets/template/resume_{template_index + 1}.docx')
    generate_resume = resume_generators[template_index]
    generate_resume(document, headline, summary, history, skill_section_headers, skill_section_contents, profile)

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

def generate_resume_file(position: str, required_skills, jd: str, profile: dict, path: str) -> str:
    history = generate_resume_history(profile, position, required_skills, jd)
    ( skill_section_headers, skill_section_contents ) = generate_skill_matrix(position, required_skills)
    ( headline, _ ) = generate_meta_data(position, required_skills)
    _generate_resume_file(headline, profile['summary'], history, skill_section_headers, skill_section_contents, profile, path)
