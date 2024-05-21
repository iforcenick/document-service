from langchain.embeddings import OpenAIEmbeddings
from skill.utils import normalize_skill_name
import os
from skill.utils import get_skill_list

from gensim.models.keyedvectors import KeyedVectors

print("Reading skill yaml data ...")
skill_names = []
skills = []
try:
    skill_data = get_skill_list()
    for key in skill_data:
        value = skill_data[key]
        if "embedding" in value:
            skills.append(value["embedding"])
            skill_names.append(normalize_skill_name(key))
except: pass

embeddings = OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'))

print("Calculating vectors using OpenAI ...")
vectors = embeddings.embed_documents(skills)

if len(vectors) == 0:
    exit()

print("Creating KeyedVectors ...")
vector_dim = len(vectors[0])
print("Embedding dim: ", vector_dim)
word_vect = KeyedVectors(vector_dim)
word_vect.add_vectors(skill_names, vectors)
word_vect.save_word2vec_format('./job_familarity_model/Model/openai_powered_embedding.bin', binary=True)
