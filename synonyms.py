# coding=utf-8

import pymorphy2
import random
import codecs
import pandas as pd
import numpy as np

def remove_brackets(words, open, close):
    first = -1
    last = -1
    count = 0

    open_pos = words.find(open)
    close_pos = -1
    last_open = -1

    while open_pos != -1:
        if first == -1:
            first = open_pos

        last_open = open_pos
        open_pos = words.find(open, last_open + 1)
        close_pos = words.find(close, last_open + 1)

        if close_pos < open_pos:
            last_open = close_pos
            break

        count += 1

    if last_open != -1:
        close_pos = last_open

    for _ in xrange(count):
        close_pos = words.find(close, close_pos + 1)

    last = close_pos

    if first != -1 and last != -1:
        return True, words[:first - 1] + words[last + 1:]

    return False, words

def parse_words(sentence):
    # remove examples type 1
    words = sentence.split("||")[0].lower()

    # remove references
    words = words.replace("\n", " ")
    words = words.replace(u"см.", "")
    words = words.replace(u"ср.", "")

    while True:
        result, words = remove_brackets(words, "(", ")")
        if not result:
            break

    while True:
        result, words = remove_brackets(words, "[", "]")
        if not result:
            break

    while True:
        result, words = remove_brackets(words, "<", ">")
        if not result:
            break

    # remove examples type 2
    words = words.split(".")[0]
    words = words.replace(";", ",")

    return list(set(word.strip() for word in words.split(",") if len(word.strip()) > 0))

def parse_key(key):
    while True:
        result, key = remove_brackets(key, "(", ")")
        if not result:
            break

    return key.strip()

#out = codecs.open("synonyms", "w", "utf-8", buffering=0)

synms = {}

for line in codecs.open("abr1w.txt", "r", "utf-8"):
    parts = line.split("#")
    first = parse_key(parts[0].lower())

    second =  parse_words(parts[1])

    if len(second) and len(first):
        synms[first] = second
        #out_line = ""

        #for v in second:
        #    out_line += v + ","

        #out.write(first + "#" + out_line[:-1] + "\n")
        #out.flush()

#out.close()

def process_word(word):
    word = word.replace(".", "")
    word = word.replace(",", "")
    word = word.replace("\n", "")
    word = word.replace(";", "")
    word = word.replace("?", "")
    word = word.replace("!", "")
    word = word.replace("(", "")
    word = word.replace(")", "")

    return word.strip()

data = pd.read_json('data/restoclub.reviews.json')

new_data_list = []

morph = pymorphy2.MorphAnalyzer()

# go through the data to replace word with synonyms
for inx, row in data.iterrows():
    line = row.text
    line = line.lower()
    words = line.lower().split(" ")
    changes = 0

    result_line = ""

    for word in words:
        raw_word = process_word(word)

        parsed_word = morph.parse(raw_word)
        norm_raw_word = parsed_word[0].normal_form
        tag_raw_word = parsed_word[0].tag

        # if word has synonyms then get the random one instead of it
        if norm_raw_word in synms:
            syn = random.choice(synms[norm_raw_word])

            # change the form of synonym to form of original word
            syn_parsed = morph.parse(syn)[0]
            inflected = syn_parsed.inflect(tag_raw_word.grammemes)

            if inflected:
                syn = inflected[0]

            # replace to save other symbols that could surround the word
            result_line += " " + word.replace(raw_word, syn)
            changes += 1
        else:
            result_line += " " + word

    result_line = result_line.strip()

    #print result_line

    # if something has changed, then push it to result list
    if changes:
        new_data_d = [row.href, row.name, row.ratings, result_line]
        new_data_list.append(new_data_d)

# set new generated data to data frame
new_data = pd.DataFrame(columns=data.columns, index=np.arange(0, len(new_data_list)))

for x in np.arange(0, len(new_data_list)):
    new_data.loc[x] = new_data_list[x]

# concat original data frame and new data frame, shuffle it
result = pd.concat([new_data, data]).reset_index(drop=True)
#result = result.reindex(np.random.permutation(result.index))

print result

result.to_json("data/restoclub.reviews.synonyms.json")