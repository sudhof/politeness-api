
import csv
import os
import cPickle
import numpy as np
import random

from sklearn import svm
from scipy.sparse import csr_matrix
from sklearn.metrics import classification_report

from features.vectorizer import FeatureVectorizer
from datasets import get_training_data

# Training a simple SVM
# anything < 0.0 is not polite
# anything > 0.0 is polite
# only features- unigrams and bigrams


DATA_DIR = "data"
MODEL_PATH = "linear-svm.p"

def documents2feature_vectors(documents):
    vectorizer = FeatureVectorizer(documents=documents)
    fks = False
    X, y = [], []
    for d in documents:
        fs = vectorizer.features(d)
        if not fks:
            fks = sorted(fs.keys())
        fv = [fs[f] for f in fks]
        # If politeness score > 0.0, 
        # the doc is polite AKA 1
        l = 0
        if d['score'] > 0.0:
            l = 1
        X.append(fv)
        y.append(l)
    X = np.asarray(X)
    y = np.asarray(y)
    return X, y


documents = get_training_data()
print "%d documents" % len(documents)

X, y = documents2feature_vectors(documents)

Xtest, ytest = X[-500:], y[-500:]
X, y = X[:-500], y[:-500]
cPickle.dump({"X": Xtest, "y": ytest}, open("sparse-testing.p", 'w'))

print "%d training, %d testing" % (len(X), len(Xtest))

X, Xtest = csr_matrix(X), csr_matrix(Xtest)

print "Fitting"

#clf = svm.SVC(C=100.0, kernel='linear')
clf = svm.SVC(C=100, cache_size=200, class_weight=None, coef0=0.0, degree=3,
  gamma=0.001, kernel='rbf', max_iter=-1, probability=True,
  random_state=None, shrinking=True, tol=0.001, verbose=False)
clf.fit(X, y)

print "Pickling"
cPickle.dump(clf, open(MODEL_PATH, 'w'))

print "Evaluating"
y_pred = clf.predict(Xtest)
print(classification_report(ytest, y_pred))


