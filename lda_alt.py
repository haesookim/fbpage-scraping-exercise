from gensim.corpora import Dictionary, MmCorpus
from konlpy.tag import Okt
from gensim import word2vec
from gensim.models import Phrases
import csv

twitter = Okt()
results = []

data_path = 'posts_data_50.csv'
parsed_path = 'parsed_bamboo.txt'
word2vec_path = 'Bambooword2vec.model'


# parsing the data to parsed_bamboo.txt
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

# making of the lda phrases analysis

# making of the dictionary for lda topic analysis
dict_made = False

dict_path = 'dictionary.dict'

if dict_made:
    dictionary = Dictionary.load(dict_path)
else:
    reviews_for_lda = word2vec.LineSentence(reviews_for_lda_filepath)
    dictionary = Dictionary(reviews_for_lda)
    dictionary.filter_extremes(no_below=10, no_above=0.4)
    dictionary.compactify()

    dictionary.save(dict_path)