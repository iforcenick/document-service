import pymongo

client = pymongo.MongoClient("localhost", 27017)
db = client.jobdb
job_collection = db.jobs
annotation_collection = db.annotations

bid_question_collection = db.bid_questions

def get_job_id_from_url(url: str):
  pass