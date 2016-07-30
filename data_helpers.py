# coding=utf-8

import string
import numpy as np
import pandas as pd
import datetime
from keras.utils.np_utils import to_categorical


def load_ag_data():
    train = pd.read_csv('orig_data/ag_news_csv/train.csv', header=None)
    print len(train)
    train = train.dropna()

    x_train = train[1] + train[2]
    x_train = np.array(x_train)

    y_train = train[0] - 1
    y_train = to_categorical(y_train)

    test = pd.read_csv('orig_data/ag_news_csv/test.csv', header=None)
    x_test = test[1] + test[2]
    x_test = np.array(x_test)

    y_test = test[0] - 1
    y_test = to_categorical(y_test)

    return (x_train, y_train), (x_test, y_test)


def mini_batch_generator(x, y, vocab, vocab_size, vocab_check, maxlen, batch_size=128):

    for i in xrange(0, len(x), batch_size):
        x_sample = x[i:i + batch_size]
        y_sample = y[i:i + batch_size]

        input_data = encode_data(x_sample, maxlen, vocab, vocab_size, vocab_check)

        yield (input_data, y_sample)

def encode_data(x, maxlen, vocab, vocab_size, check):
    #Iterate over the loaded data and create a matrix of size maxlen x vocabsize
    #In this case that will be 1014x69. This is then placed in a 3D matrix of size
    #data_samples x maxlen x vocab_size. Each character is encoded into a one-hot
    #array. Chars not in the vocab are encoded into an all zero vector.

    input_data = np.zeros((len(x), maxlen, vocab_size))

    for sentence_pos, sentence in enumerate(x):
        char_pos = 0
        sent_array = np.zeros((maxlen, vocab_size))
        chars = list(sentence.lower().replace(' ', ''))[:maxlen]

        for char in chars:
            char_array = np.zeros(vocab_size, dtype=np.int)

            if char in check:
                char_array[vocab[char]] = 1

            sent_array[char_pos, :] = char_array
            char_pos += 1

        input_data[sentence_pos, :, :] = sent_array

    return input_data

def shuffle_matrix(x, y):
    stacked = np.hstack((np.matrix(x).T, y))
    np.random.shuffle(stacked)
    xi = np.array(stacked[:, 0]).flatten()
    yi = np.array(stacked[:, 1:])

    return xi, yi

def create_vocab_set():
    alphabet = (list(string.ascii_lowercase) + list(string.digits) +
                list(string.punctuation) + ['\n'])

    vocab = {letter: inx for inx, letter in enumerate(alphabet)}

    return vocab, len(alphabet), set(alphabet)

#(xt, yt), (x_test, y_test) = load_ag_data()
#vocab, vocab_size, check = create_vocab_set()

#test_data = encode_data2(x_test, 1014, vocab, vocab_size, check)

#print test_data[0][:10]
