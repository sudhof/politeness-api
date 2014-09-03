
import os
import cPickle
import string

from bow_features import getwords, getbigrams
# No dependency parsing for now
#from politeness_strategies import getPolitenessFeaturesFromParse

DIR = os.path.split(__file__)[0]


class FeatureVectorizer:

    # Currently just unigram, bigram features

    def __init__(self, documents=False, minwords=20, minbigrams=20, minparse=20, minparserel=20, minwordloc=20):
        # If we get documents on initialization, we seed the features
        # otherwise, we expect featwords and featbigrams to be pickled nearby
        
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
        feature_dict = {}
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
            words = getwords(document)
            for w in set(words):
                wordcounts.setdefault(w, 0)
                wordcounts[w] += 1                
            bigrams=getbigrams(document)
            for w in set(bigrams):
                bigramcounts.setdefault(w,0)
                bigramcounts[w] += 1
        self.featwords = [w for w in wordcounts if wordcounts[w] > minwords]
        self.featbigrams = [w for w in bigramcounts if bigramcounts[w] > minbigrams and w[0] not in punctuation and w[1] not in punctuation]
        # Save results
        cPickle.dump(self.featwords, open(os.path.join(DIR, "featwords.p"), 'w'))
        cPickle.dump(self.featbigrams, open(os.path.join(DIR, "featbigrams.p"), 'w'))


