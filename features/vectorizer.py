
import os
import cPickle
import string
import nltk

from bow_features import getwords, getbigrams
from politeness_strategies import getPolitenessFeaturesFromParse

##C: added for is_request
from politeness_strategies import getdeptag, getleft, getleftpos, getright, getrightpos

##C: switching to local coreNLP server
from parse_api_interface import get_parse

DIR = os.path.split(__file__)[0]
TOKENIZER_FILENAME = "file:%s" % os.path.join(DIR, "english.pickle")
SENTENCE_TOKENIZER = nltk.data.load(TOKENIZER_FILENAME)

##C: added for is_request
polar_set=set(["is", "are", "was", "were", "am", "have", "has", "had", "can", "could", "shall", "should", "will", "would", "may", "might", "must", "do", "does", "did", "ought", "need", "dare", "if", "when", "which", "who", "whom", "how"])
initial_polar = lambda p: (getleftpos(p)==1 and getleft(p) in polar_set) or (getrightpos(p)==1 and getright(p) in polar_set)
aux_polar = lambda p: getdeptag(p)=="aux" and getright(p) in polar_set



class FeatureVectorizer:

    # Currently just unigram, bigram features

    def __init__(self, documents=False, minwords=20, minbigrams=20, minparse=20, minparserel=20, minwordloc=20):
        # If we get documents on initialization, we seed the features
        # otherwise, we expect featwords and featbigrams to be pickled nearby
        self.tmpd={} #saving parse in order to do the is_request check without reparsing
        
        if os.path.exists(os.path.join(DIR, "featwords.p")):
            self.featwords = cPickle.load(open(os.path.join(DIR, "featwords.p")))
            self.featbigrams = cPickle.load(open(os.path.join(DIR, "featbigrams.p")))
        else:            
            self._compute_words_and_bigrams(documents, minwords, minbigrams)
        """
        if documents:
            self._compute_words_and_bigrams(documents, minwords, minbigrams)
        else:
            self.featwords = cPickle.load(open(os.path.join(DIR, "featwords.p")))
            self.featbigrams = cPickle.load(open(os.path.join(DIR, "featbigrams.p")))
        """
        print "Features: %d unigram, %d bigrams" % (len(self.featwords), len(self.featbigrams))


    def features(self, d):
        if 'sentences' not in d:
            d['sentences'] = SENTENCE_TOKENIZER.tokenize(d['text'])
        if 'parses' not in d:
            d['parses'] = map(lambda x: get_parse(x), d['sentences'])
            self.tmpd=d # saving parse in order to do the is_request check without reparsing
        d['words'] = getwords(d)
        feature_dict = {}
        feature_dict.update(self._get_word_features(d))
        feature_dict.update(getPolitenessFeaturesFromParse(d))
        return feature_dict

    def _get_word_features(self, d):
        feature_dict = {}
        if 'words' in d:
            words = set(d['words'])
        else:
            words = set(getwords(d))
        for w in self.featwords:
            if w in words:
                feature_dict["UNIGRAM_"+w] = 1
            else:
                feature_dict["UNIGRAM_"+w] = 0
        words = set(getbigrams(d))
        for w in self.featbigrams:
            if w in words:
                feature_dict["BIGRAM_"+str(w)] = 1
            else:
                feature_dict["BIGRAM_"+str(w)] = 0
        return feature_dict

    def _compute_words_and_bigrams(self, documents, minwords, minbigrams):
        punctuation = string.punctuation
        punctuation = punctuation.replace("?","").replace("!","")
        wordcounts = {}
        bigramcounts = {}
        # Count words and bigrams
        for c, document in enumerate(documents):
            document['sentences'] = SENTENCE_TOKENIZER.tokenize(document['text'])
            words = getwords(document)
            for w in set(words):
                wordcounts.setdefault(w, 0)
                wordcounts[w] += 1                
            bigrams = getbigrams(document)
            for w in set(bigrams):
                bigramcounts.setdefault(w,0)
                bigramcounts[w] += 1
        self.featwords = [w for w in wordcounts if wordcounts[w] > minwords]
        self.featbigrams = [w for w in bigramcounts if bigramcounts[w] > minbigrams and w[0] not in punctuation and w[1] not in punctuation]
        # Save results
        cPickle.dump(self.featwords, open(os.path.join(DIR, "featwords.p"), 'w'))
        cPickle.dump(self.featbigrams, open(os.path.join(DIR, "featbigrams.p"), 'w'))

    ##C: added for is_request
    def _select2(self,parse, unittest):
        for l in parse:
            try:
                testres=unittest(l)
                if testres:
                    return True
            except Exception, e:
                print e,l
                testres=False
        return False

    ##C: added for is_request
    def is_request(self):
        if 'parses' in self.tmpd: ##use the already computed parse
            d = self.tmpd
        else:
            print "This is ran on an empty FeatureVectorizer instance (no processed document)"
            return False
        if "?" in d['text']:
            return True
        if 'sentences' not in d:
            d['sentences'] = SENTENCE_TOKENIZER.tokenize(d['text'])
        if 'parses' not in d:
            d['parses'] = map(lambda x: get_parse(x), d['sentences'])
        for parse in d['parses']:
            if self._select2(parse,initial_polar) or self._select2(parse,aux_polar):
                return True
        return False





if __name__ == "__main__":

    docs = [
        "are you stupid?? can you not understand my question?",
        "Could you would you please is it any trouble?",
        "I'm so sorry but I'm having trouble understanding. Could you maybe revise? Thank you so much!"
    ]

    docs = map(lambda x: {"text": x}, docs)

    vectorizer = FeatureVectorizer()
    for d in docs:

        print "\n===================="
        print d['text']
        f = vectorizer.features(d)
        print "%d features" % len(f)




