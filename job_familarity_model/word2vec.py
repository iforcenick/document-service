from gensim.models.keyedvectors import KeyedVectors
from skill.utils import normalize_skill_name
from numpy import dot
from gensim import matutils

print("Loading Word2Vec model...")
word_vect = KeyedVectors.load_word2vec_format("./job_familarity_model/Model/openai_powered_embedding.bin", binary=True)
print("Model loaded.")

def similarity_nm(skills1, skills2):
    if len(skills1) == 0 or len(skills2) == 0:
        return 0
    keys1 = [ normalize_skill_name(item["skill_name"]) for item in skills1 ]
    keys2 = [ normalize_skill_name(item["skill_name"]) for item in skills2 ]
    weights1 = [ item["weight"] for item in skills1 ]
    weights2 = [ item["weight"] for item in skills2 ]
    mean1 = word_vect.get_mean_vector(keys1, weights=weights1, pre_normalize=False)
    mean2 = word_vect.get_mean_vector(keys2, weights=weights2, pre_normalize=False)
    return dot(matutils.unitvec(mean1), matutils.unitvec(mean2))

def similarity_n1(skills, point):
    return similarity_nm(skills, [point])