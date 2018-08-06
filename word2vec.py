import csv
from konlpy.tag import Okt
from gensim.models import word2vec

twitter = Okt()
results = []

with open('posts_data_50.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    for row in csv_reader:

        lines = row[0].split("\n")

        for line in lines:
            temp_list = twitter.pos(line, norm=True, stem=True)
            r = []
            for word in temp_list:
                if not word[1] in ["Josa", "Eomi", "Punctuation"]:
                    r.append(word[0])
            rl = (" ".join(r)).strip()
            results.append(rl)

bamboo_file = "bamboo_1.wakati"

with open(bamboo_file, 'w', encoding='utf-8') as fp:
    fp.write("\n".join(results))

data = word2vec.LineSentence(bamboo_file)
model = word2vec.Word2Vec(data, size=200, window=10, hs=1, min_count=2, sg=1)
model.save("Bambooword2vec_1.model")
print("done")
