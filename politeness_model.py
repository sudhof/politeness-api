
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
    y_pred = clf.predict(X)
    #scores = clf.decision_function(X)
    #print str(scores)
    return y_pred[0]



