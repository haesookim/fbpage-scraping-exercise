from gensim.models import word2vec

model = word2vec.Word2Vec.load("Bambooword2vec.model")

model_call = model.most_similar(positive=["대숲"])

model_love = model.most_similar(positive=["연애"])

model_depression = model.most_similar(positive=["우울", "우울하다"])

model_grades = model.most_similar(positive=["학점", "성적"])

model_introspective = model.most_similar(positive=["나"])

model_election = model.most_similar(positive=["총장", "선거"])

with open("word2vec_result.txt", "w") as file:
    file.write("'대숲'과 관련된 단어\n\n")
    file.write(str(model_call))
    file.write("\n\n")

    file.write("'연애'와 관련된 단어\n\n")
    file.write(str(model_love))
    file.write("\n\n")

    file.write("'우울'과 관련된 단어\n\n")
    file.write(str(model_depression))
    file.write("\n\n")

    file.write("'학점', '성적' 과 관련된 단어\n\n")
    file.write(str(model_grades))
    file.write("\n\n")

    file.write("'나'와 관련된 단어\n\n")
    file.write(str(model_introspective))
    file.write("\n\n")

    file.write("'총장', '선거'와 관련된 단어\n\n")
    file.write(str(model_election))