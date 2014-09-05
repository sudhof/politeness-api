
import csv
import os
import cPickle
import random

DATA_DIR = "data"

##############################################################################
# For loading pickled, pre-processed documents

#TRAINING_DATA_FILENAME = "training-data.p"
TRAINING_DATA_FILENAME = "training-data-corenlp-parses.p"

def get_training_data():
    filename = os.path.join(DATA_DIR, TRAINING_DATA_FILENAME)
    return cPickle.load(open(filename, 'r'))


##############################################################################
# For loading raw documents

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
