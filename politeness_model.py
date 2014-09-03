
import cPickle
import numpy as np

from sklearn import svm
from scipy.sparse import csr_matrix

from features.vectorizer import FeatureVectorizer


clf = cPickle.load(open("linear-svm.p"))
vectorizer = FeatureVectorizer()


def score_politeness(text):
    features = vectorizer.features({"text": text})
    fv = [features[f] for f in sorted(features.iterkeys())]
    X = csr_matrix(np.asarray([fv]))
    y_pred = clf.predict(X)
    return y_pred[0]



