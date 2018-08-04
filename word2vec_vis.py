import pandas as pd
from konlpy.tag import Okt
from gensim.models import word2vec
import csv
from sklearn.manifold import TSNE
import pickle

twitter = Okt()
results = []

data_path = 'posts_data_50.csv'
parsed_path = 'parsed_bamboo.txt'
word2vec_path = 'bamboo_w2v.model'
tsne_path = 'bamboo_tsne.pkl'


def clean_posts(post):
    lines = post[0].split("\n")
    for line in lines:
        temp_list = twitter.pos(line, norm=True, stem=True)
        r = []
        for word in temp_list:
            if not word[1] in ["Josa", "Eomi", "Punctuation"]:
                r.append(word[0])
        rl = (" ".join(r)).strip()
    return rl


with open(data_path, 'w') as f:
    data = csv.reader(f, delimiter=',')
    for row in data:
        results.append(clean_posts(row))


with open(parsed_path, 'w', encoding='utf-8') as fp:
    fp.write("\n".join(results))

data = word2vec.LineSentence(parsed_path)
model = word2vec.Word2Vec(data, size=100, window=10, hs=1, min_count=2, sg=1)
model.save(word2vec_path)
print("model made")

vector_file = word2vec.load(word2vec_path)

vector_file.init_sims()

num_words = 2000
word_embeddings = pd.DataFrame(vector_file.syn0norm[:num_words, :], index=vector_file.index2word[:num_words])
word_embeddings.head()


# create tsne visualization method
tsne = TSNE(random_state=0)
tsne_points = tsne.fit_transform(word_embeddings.values)
with open(tsne_path, 'wb') as f:
    pickle.dump(tsne_points, f)

tsne_df = pd.DataFrame(tsne_points, index=word_embeddings.index, columns=['x_coord', 'y_coord'])
tsne_df['word'] = tsne_df.index
