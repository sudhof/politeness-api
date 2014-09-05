
import cPickle

from politeness_model import score_politeness


documents = cPickle.load(open("testing-data.p", 'r'))
right, total = 0, 0
for d in documents:
    total += 1
    probs = score_politeness(d['text'])
    pred_l = "polite" if probs['polite'] > probs['impolite'] else "impolite"
    true_l = "polite" if d['score'] > 0.0 else "impolite"
    if pred_l == true_l:
        right += 1


print "%d right decisions out of %d total" % (right, total)
print "%.1f%% Accuracy" % (100.0*float(right)/float(total))



