"""
adapted parameter estimation sample script
"""

from __future__ import print_function

import os
import numpy as np

from scipy.sparse import csr_matrix
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC

from features.vectorizer import FeatureVectorizer
from datasets import get_training_data

########################################################################

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

########################################################################

documents = get_training_data()
print("%d documents" % len(documents))
X, y = documents2feature_vectors(documents)

Xtest, ytest = X[-500:], y[-500:]
X, y = X[:-500], y[:-500]

# Split the dataset 50-50
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.5, random_state=0)

print("%d training, %d testing" % (len(X_train), len(X_test)))

X_train, X_test = csr_matrix(X_train), csr_matrix(X_test)


########################################################################

# Set the parameters by cross-validation
tuned_parameters = [
                {'kernel': ['poly'], 'gamma': [1e-3, 1e-4], 'degree': [2,3],  
                     'C': [1, 10, 100, 1000]},                     
                {'kernel': ['linear'], 'C': [0.02, 1, 10, 100]},
                {'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                     'C': [1, 10, 100, 1000]}
]

scores = ['f1']

########################################################################

for score in scores:
    print("# Tuning hyper-parameters for %s" % score)
    print()

    clf = GridSearchCV(SVC(C=1), tuned_parameters, cv=5, scoring=score)
    clf.fit(X_train, y_train)

    print("Best parameters set found on development set:")
    print()
    print(clf.best_estimator_)
    print()
    print("Grid scores on development set:")
    print()
    for params, mean_score, scores in clf.grid_scores_:
        print("%0.3f (+/-%0.03f) for %r"
              % (mean_score, scores.std() / 2, params))
    print()

    print("Detailed classification report:")
    print()
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.")
    print()
    y_true, y_pred = y_test, clf.predict(X_test)
    print(classification_report(y_true, y_pred))
    print()

