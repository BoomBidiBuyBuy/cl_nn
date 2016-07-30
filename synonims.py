# coding=utf-8

import codecs

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

    return set(word.strip() for word in words.split(",") if len(word.strip()) > 0)

out = codecs.open("result.out", "w", "utf-8", buffering=0)

for line in codecs.open("abr1w.txt", "r", "utf-8"):
    parts = line.split("#")
    first = parts[0].lower()
    print first
    second =  parse_words(parts[1])

    if len(second):
        out_line = ""

        for v in second:
            out_line += v + ","

        out.write(first + "#" + out_line[:-1] + "\n")
        out.flush()

out.close()
