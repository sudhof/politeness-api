

import os
import nltk


def getwords(document):
    words = []
    for s in document['sentences']:
        words.extend(nltk.word_tokenize(s))
    return words


def getbigrams(document, lasttwosents=False):
    words = []
    for s in document['sentences']:
        words.extend(nltk.bigrams(nltk.word_tokenize(s)))
    return words

