# coding=utf-8

import pandas as pd
import string

#------------------------------------#

def to_class(m):
    def func(x):
        if x < m:
            return 0

        return 1

    return func

#------------------------------------#

def get_alphabet():
    return set(list(u"абвгдеёжзийклмнопрстуфчцчшщъыьэюя") + list(string.digits) +\
        list(string.punctuation) +['\n'])

alpha = get_alphabet()

data = pd.read_json('restoclub.reviews.json')

split_index = int(len(data) * 0.8)

train_data = data[:split_index]
test_data = data[split_index:]

print len(train_data) + len(test_data) == len(data)

"""
text_data = data.text.apply(lambda x: x.lower().replace(' ', ''))


length = 0
for row in text_data:
    chars = list(row)
    chars = filter(lambda x: x in alpha, chars)
    sent = u''.join(chars)
    pass

print (length + 0.1) / len(text_data)

total = data.ratings.apply(lambda x: x['total'])

mean = total.mean()

class_total = total.apply(to_class(mean))
"""