
import sys
import os
import cPickle
import nltk

from datasets import load_labeled_data
from features.dependencies.parser import StanfordDependencyParser

DIR = os.path.split(__file__)[0]
TOKENIZER_FILENAME = "file:%s" % os.path.join(DIR, "features", "english.pickle")
SENTENCE_TOKENIZER = nltk.data.load(TOKENIZER_FILENAME)

documents = load_labeled_data()
print "%d documents total" % len(documents)

sents = []
for i, d in enumerate(documents):

    sys.stderr.write("\r")
    sys.stderr.write("document %s" % i)
    sys.stderr.flush()

    ss = SENTENCE_TOKENIZER.tokenize(d['text'])
    ss = filter(lambda x: x, map(lambda x: x.strip(), ss))
    d['sentences'] = ss
    sents += d['sentences']


sys.stderr.write("\n")

print "%d sentences" % len(sents)

sents2parses = {}
buff = []
for s in sents:
    buff.append(s)
    if len(buff) >= 1000:
        print "Running 1000 parses"
        s2p = StanfordDependencyParser().parse(buff)
        buff = []
        sents2parses.update(s2p)

if buff:
    print "Running final parse"
    s2p = StanfordDependencyParser().parse(buff)
    sents2parses.update(s2p)


err = 0
docs2 = []
for d in documents:
    parses = []
    for s in d['sentences']:
        if s not in sents2parses:
            err += 1
        else:
            parses.append(sents2parses[s])
    if len(parses) == len(d['sentences']):
        d['parses'] = parses
        docs2.append(d)

documents = docs2
print "%d sentences not parsed-- retrieval errors" % err
print "Writing %d documents" % len(documents)

cPickle.dump(documents, open(os.path.join(DIR, "data", "training-data.p"), 'w'))


