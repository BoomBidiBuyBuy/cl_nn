# coding=utf-8

import codecs

def remove_brackets(words, open, close, pos = 0):
    open_pos = words.find(open)

    if open_pos != -1:
        next_pos = words.find(open, open_pos + 1)

        if next_pos != -1:
            return remove_brackets(words, open, close, next_pos + 1)


    return -1, -1

def parse_words(sentence):
    # remove examples type 1
    words = sentence.split("||")[0].lower()

    # remove references
    words = words.replace(u"см.", "")
    words = words.replace(u"ср.", "")

    remove_brackets(words, "(", ")")
    remove_brackets(words, "[", "]")
    remove_brackets(words, "<", ">")

    while words.find('[') != -1:
        if words.find(']') != -1:
            words = words[:words.find('[') - 1] + words[words.find(']') + 1:]
        else:
            words = ""

    while words.find('(') != -1:
        if words.find(')') != -1:
            words = words[:words.find('(') - 1] + words[words.find(')') + 1:]
        else:
            words = ""

    while words.find('<') != -1:
        if words.find('>') != -1:
            words = words[:words.find('<') - 1] + words[words.find('>') + 1:]
        else:
            words = ""

    # remove examples type 2
    words = words.split(".")[0]
    words = words.replace(";", ",")

    return set(word.strip() for word in words.split(",") if len(word.strip()) > 0)


remove_brackets("<<av> a>", "<", ">")

#out = codecs.open("result.out", "w", "utf-8", buffering=0)
"""
for line in codecs.open("abr1w.txt", "r", "utf-8"):
    parts = line.split("#")
    first = parts[0].lower()
    print first
    second =  parse_words(parts[1])

    if len(second):
        out_line = ""

        for v in second:
            out_line += v + ","
"""
        #out.write(first + "#" + out_line[:-1])
        #out.flush()

#out.close()
