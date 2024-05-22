import os
from dotenv import load_dotenv
load_dotenv()

DOCUMENT_LOG_PATH = os.getenv('DOCUMENT_LOG_PATH')
PARSE_ENGINE_URL = os.getenv('PARSE_ENGINE_URL')
DBHUB_URL = os.getenv('DBHUB_URL')
DOCUMENT_SERVICE_PORT = os.getenv('DOCUMENT_SERVICE_PORT')
LIBREOFFICE_PATH = os.getenv('LIBREOFFICE_PATH')

if not os.path.exists(DOCUMENT_LOG_PATH):
  os.mkdir(DOCUMENT_LOG_PATH)