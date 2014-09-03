
import csv
import os
import cPickle
import numpy as np
import random

from sklearn import svm
from scipy.sparse import csr_matrix
from sklearn.metrics import classification_report

from features.vectorizer import FeatureVectorizer

# Training a simple SVM
# anything < 0.0 is not polite
# anything > 0.0 is polite
# only features- unigrams and bigrams


DATA_DIR = "data"
MODEL_PATH = "linear-svm.p"


def load_labeled_data():
    files = ["stack-exchange.annotated.csv", "wikipedia.annotated.csv"]
    documents = []
    err = 0
    for f in files:
        reader = csv.DictReader(open(os.path.join(DATA_DIR, f), "rU"))
        for row in reader:
            try:
                documents.append({"text": row['Request'], "score": float(row['Normalized Score'])})
            except:
                err += 1
    print "Couldn't load %d documents due to CSV error" % err
    documents = keep_extreme_quartiles(documents)
    return documents


def keep_extreme_quartiles(documents):
    # Only the bottom quartile is impolite,
    # the top quartile polite.
    # Toss the rest
    documents.sort(key=lambda x: x['score'])
    l = len(documents)
    impolite = documents[:l/4]
    polite = documents[-l/4:]
    documents = impolite + polite
    random.shuffle(documents)
    return documents


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


documents = load_labeled_data()
print "%d documents" % len(documents)

X, y = documents2feature_vectors(documents)

Xtest, ytest = X[-500:], y[-500:]
X, y = X[:-500], y[:-500]

print "%d training, %d testing" % (len(X), len(Xtest))

X, Xtest = csr_matrix(X), csr_matrix(Xtest)

print "Fitting"

clf = svm.SVC(C=100.0, kernel='linear')
clf.fit(X, y)

print "Pickling"
cPickle.dump(clf, open(MODEL_PATH, 'w'))

print "Evaluating"
y_pred = clf.predict(Xtest)
print(classification_report(ytest, y_pred))












