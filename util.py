import os
from env import DOCUMENT_LOG_PATH

def get_save_path(file_id: str, profile: str, doc_type: str):
  dir_path = f'{DOCUMENT_LOG_PATH}/{file_id}'
  if not os.path.exists(dir_path):
    os.mkdir(dir_path)
  file_path = f'{dir_path}/{profile}_{doc_type}.pdf'
  return file_path