from skill.utils import normalize_skill_name
from .word2vec import word_vect

while True:
    temp = input()
    skills1 = [ normalize_skill_name(item) for item in temp.split(" ") ]
    temp = input()
    skills2 = [ normalize_skill_name(item) for item in temp.split(" ") ]
    print(word_vect.n_similarity(skills1, skills2) ** 2)
