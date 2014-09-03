
import nltk

def getwords(document, lasttwosents=False):
    #sents=nltk.sent_tokenize(document['text'])
    #if lasttwosents:
    #  sents=sents[-2:]
    #words=[]
    #for s in sents:
    #    words.extend(nltk.word_tokenize(s))
    words = nltk.word_tokenize(document['text'])
    return words

def getbigrams(document, lasttwosents=False):
    #sents=nltk.sent_tokenize(document['text'])
    #if lasttwosents:
    #  sents=sents[-2:]
    #words=[]
    #for s in sents:
    #    words.extend(nltk.bigrams(nltk.word_tokenize(s)))
    words = nlkt.bigrams(nltk.word_tokenize(document['text']))
    return words
