
import cPickle
import numpy as np

from sklearn import svm
from scipy.sparse import csr_matrix

from features.vectorizer import FeatureVectorizer


clf = cPickle.load(open("politeness-svm.p"))
vectorizer = FeatureVectorizer()

print "Loaded model"
print clf

def score_politeness(text):
    features = vectorizer.features({"text": text})
    fv = [features[f] for f in sorted(features.iterkeys())]
    X = csr_matrix(np.asarray([fv]))
    #y_pred = clf.predict(X)
    probs = clf.predict_proba(X)
    probs = probs[0]
    probs = {"impolite": probs[0], "polite": probs[1]}
    return probs




