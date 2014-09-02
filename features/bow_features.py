
import string
import nltk

def getwords(document, lasttwosents=False):
    sents=nltk.sent_tokenize(document['text'])
    if lasttwosents:
      sents=sents[-2:]
    words=[]
    for s in sents:
        words.extend(nltk.word_tokenize(s))
    return words

def getbigrams(document, lasttwosents=False):
    sents=nltk.sent_tokenize(document['text'])
    if lasttwosents:
      sents=sents[-2:]
    words=[]
    for s in sents:
        words.extend(nltk.bigrams(nltk.word_tokenize(s)))
    return words


class FeatureVectorizer:

      def __init__(self, documents, minwords=20, minbigrams=20, minparse=20, minparserel=20, minwordloc=20):
            punctuation=string.punctuation
            punctuation=punctuation.replace("?","").replace("!","")
            wordcounts={}
            for c, document in enumerate(documents):
                words=getwords(document)
                for w in set(words):
                    wordcounts[w]=wordcounts.setdefault(w,0)+1
            bigramcounts={}
            for c, document in enumerate(documents):
                bigrams=getbigrams(document)
                for w in set(bigrams):
                    bigramcounts[w]=bigramcounts.setdefault(w,0)+1
            wordloccountrel={}
            for c, document in enumerate(documents):
                labels=getwordpositionrel(document)
                for l in set(labels):
                  wordloccountrel[l]=wordloccountrel.setdefault(l,0)+1
            self.featwords=[w for w in wordcounts if wordcounts[w]>minwords]
            del wordcounts
            self.featbigrams=[w for w in bigramcounts if bigramcounts[w]>minbigrams and w[0] not in punctuation and w[1] not in punctuation]   
            del bigramcounts


      def getfeatures(self, documents, last2sentences=False): ## documents to classify
            features={}
            for d in documents:
                  id=d["id"]
                  tmpfeatdict={}
                  words=getwords(d,last2sentences)
                  for w in self.featwords:
                        if w in words:
                              tmpfeatdict["UNIGRAM_"+w]=1
                        else:
                              tmpfeatdict["UNIGRAM_"+w]=0
                  words2=getbigrams(d,last2sentences)
                  for w in self.featbigrams:
                        if w in words2:
                            tmpfeatdict["BIGRAM_"+str(w)]=1
                        else:
                            tmpfeatdict["BIGRAM_"+str(w)]=0

