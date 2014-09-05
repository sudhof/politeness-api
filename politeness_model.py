
import cPickle
import numpy as np

from sklearn import svm
from scipy.sparse import csr_matrix

from features.vectorizer import FeatureVectorizer


clf = cPickle.load(open("linear-svm.p"))
vectorizer = FeatureVectorizer()

print "Loaded model"
print clf

def score_politeness(text):
    features = vectorizer.features({"text": text})
    fv = [features[f] for f in sorted(features.iterkeys())]
    X = csr_matrix(np.asarray([fv]))
    print "Predicting"
    print "Text"
    y_pred = clf.predict(X)
    l = "polite"
    if y_pred[0] == 0:
        l = "impolite"
    print l
    probs = clf.predict_proba(X)
    probs = probs[0]
    print "Class 0: ", probs[0]
    print "Class 1: ", probs[1]
    #scores = clf.decision_function(X)
    #print str(scores)
    return y_pred[0]



