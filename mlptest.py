import os
import glob
import json
import csv

dic_file = "dictionary.json"
data_file = "data.json"

word_dic = {"_MAX": 0}


def text_to_ids(text):
    text = text.strip()
    words = text.split(" ")
    result = []

    for w in words:
        w = w.strip()
        if w == "": continue
        if not w in word_dic:
            wid = word_dic[w] = word_dic["_MAX"]
            word_dic["_MAX"] += 1
            print(wid, w)
        else:
            wid = word_dic[w]
        result.append(wid)
    return result


def row_to_ids(fname):
    for line in fname:
        return text_to_ids(line)

    """with open(fname) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            lines = row[0].split("\n")

            for line in lines:
                text_to_ids(line)"""


def register_dic(fname):
    with open(fname) as file:
        read_file = csv.reader(file, delimiter=',')

        for row in read_file:
            lines = row[0].split("\n")
            row_to_ids(lines)


def count_row_freq(fname):
    cnt = [0 for n in range(word_dic["_MAX"])]
    with open(fname) as file:
        read_file = csv.reader(file, delimiter=',')

        for row in read_file:
            lines = row[0].split("\n").strip()
            ids = row_to_ids(lines)
            for wid in ids:
                cnt[wid] += 1
    return cnt


# unfinished function definition, not sure if needed for uncategorized data
def count_freq(limit = 0):
    X = []
    Y = []
    max_words = word_dic["_MAX"]
    cat_names =[]


if os.path.exists(dic_file):
    word_dic = json.load(open(dic_file))
else:
    register_dic('posts_data_50.csv')
    json.dump(word_dic, open(dic_file, 'w'))
