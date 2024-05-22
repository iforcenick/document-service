from skill.utils import normalize_skill_name
from job_familarity_model.word2vec import similarity_nm
from resume._sentencedb import sentence_db
from resume.sentences import generate_template_sentences

print("Input regexp of the target sentence:")

temp = input()
query_skills = [ normalize_skill_name(item) for item in temp.split(" ") ]

result = []

for sentence in sentence_db:
    new_sentences = generate_template_sentences(sentence)
    max_sentence = None
    max_similarity = 0
    quality = sentence["quality"]
    for new_sentence in new_sentences:
        relations = new_sentence["relation"]
        content = new_sentence["content"]
        vector_similarity = similarity_nm(query_skills, relations)
        if max_sentence is None or max_similarity < vector_similarity:
            max_sentence = new_sentence
            max_similarity = vector_similarity
    result.append({
        "content": max_sentence["content"],
        "vector_similarity": max_similarity,
        "quality": quality,
        "similarity": max_similarity * quality,
        "relations": max_sentence["relation"]
    })

result.sort(key=lambda x: x["similarity"], reverse=True)
for sentence in result:
    content = sentence["content"]
    relations = sentence["relations"]
    vector_similarity = sentence["vector_similarity"]
    quality = sentence["quality"]
    similarity = sentence["similarity"]
    print("")
    print(content)
    print(" ".join(relations))
    print(similarity, "=", vector_similarity, "*", quality)