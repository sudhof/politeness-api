
import os
import re
from collections import defaultdict

DIR = os.path.split(__file__)[0]
nlp = False

hedges = [
  "think", "thought", "thinking", "almost",
  "apparent", "apparently", "appear", "appeared", "appears", "approximately", "around",
  "assume", "assumed", "certain amount", "certain extent", "certain level", "claim",
  "claimed", "doubt", "doubtful", "essentially", "estimate",
  "estimated", "feel", "felt", "frequently", "from our perspective", "generally", "guess",
  "in general", "in most cases", "in most instances", "in our view", "indicate", "indicated",
  "largely", "likely", "mainly", "may", "maybe", "might", "mostly", "often", "on the whole",
  "ought", "perhaps", "plausible", "plausibly", "possible", "possibly", "postulate",
  "postulated", "presumable", "probable", "probably", "relatively", "roughly", "seems",
  "should", "sometimes", "somewhat", "suggest", "suggested", "suppose", "suspect", "tend to",
  "tends to", "typical", "typically", "uncertain", "uncertainly", "unclear", "unclearly",
  "unlikely", "usually", "broadly", "tended to", "presumably", "suggests",
  "from this perspective", "from my perspective", "in my view", "in this view", "in our opinion",
  "in my opinion", "to my knowledge", "fairly", "quite", "rather", "argue", "argues", "argued",
  "claims", "feels", "indicates", "supposed", "supposes", "suspects", "postulates"
]

negativewords = open(os.path.join(DIR, "liu-negative-words.txt"), 'r').read().splitlines()
negativewords = map(lambda x: x.strip(), negativewords)
negativewords = set(negativewords)

positivewords = open(os.path.join(DIR, "liu-positive-words.txt"), 'r').read().splitlines()
positivewords = map(lambda x: x.strip(), positivewords)
positivewords = set(positivewords)

getdeptag = lambda p: p.split("(")[0]
getleft = lambda p: re.findall(r"([-\w]+)-(\d+)",p)[0][0].lower()
getleftpos = lambda p: int(re.findall(r"([-\w]+)-(\d+)",p)[0][1])
getright = lambda p: re.findall(r"([-\w]+)-(\d+)",p)[1][0].lower()
getrightpos = lambda p: int(re.findall(r"([-\w]+)-(\d+)",p)[1][1])

def removenumbers(parse_element):
  return re.sub(r"\-(\d+)","",parse_element)

def getrel(document):
  return [removenumbers(w.lower()) for w in document['parse']]

please = lambda p: len(set([getleft(p),getright(p)]).intersection(["please"]))>0 and 1 not in [getleftpos(p),getrightpos(p)]
please.__name__ = "Please"

pleasestart = lambda p: (getleftpos(p)==1 and getleft(p)=="please") or (getrightpos(p)==1 and getright(p)=="please")
pleasestart.__name__ = "Please start"

hashedges = lambda p:   getdeptag(p)=="nsubj" and  getleft(p) in hedges
hashedges.__name__ = "Hedges"

deference = lambda p: (getleftpos(p)==1 and getleft(p) in ["great","good","nice","good","interesting","cool","excellent","awesome"]) or (getrightpos(p)==1 and getright(p) in ["great","good","nice","good","interesting","cool","excellent","awesome"]) 
deference.__name__ = "Deference"

gratitude = lambda p: getleft(p).startswith("thank") or getright(p).startswith("thank") or "(appreciate, i)" in removenumbers(p).lower()
gratitude.__name__ = "Gratitude"

apologize = lambda p: getleft(p) in ["sorry","woops","oops"] or getright(p) in ["sorry","woops","oops"] or removenumbers(p).lower()=="dobj(excuse, me)" or removenumbers(p).lower()=="nsubj(apologize, i)" or removenumbers(p).lower()=="dobj(forgive, me)"
apologize.__name__ = "Apologizing"

groupidentity = lambda p: len(set([getleft(p),getright(p)]).intersection(["we","our","us","ourselves"]))>0
groupidentity.__name__ = "1st person pl."

firstperson = lambda p: 1 not in [getleftpos(p),getrightpos(p)] and len(set([getleft(p),getright(p)]).intersection(["i","my","mine","myself"]))>0
firstperson.__name__ = "1st person"

secondperson_start = lambda p: (getleftpos(p)==1 and getleft(p) in ["you","your","yours","yourself"]) or (getrightpos(p)==1 and getright(p) in ["you","your","yours","yourself"]) 
secondperson_start.__name__ = "2nd person start"

firstperson_start = lambda p: (getleftpos(p)==1 and getleft(p) in ["i","my","mine","myself"]) or (getrightpos(p)==1 and getright(p) in ["i","my","mine","myself"]) 
firstperson_start.__name__ = "1st person start"

hello = lambda p: (getleftpos(p)==1 and getleft(p) in ["hi","hello","hey"]) or (getrightpos(p)==1 and getright(p) in ["hi","hello","hey"]) 
hello.__name__ = "Indirect (greeting)"

really = lambda p: (getright(p)=="fact" and getdeptag(p)=="prep_in") or removenumbers(p) in ["det(point, the)","det(reality, the)","det(truth, the)"] or len(set([getleft(p),getright(p)]).intersection(["really","actually","honestly","surely"]))>0  
really.__name__ = "Factuality"

why = lambda p: (getleftpos(p) in [1,2] and getleft(p) in ["what","why","who","how"]) or (getrightpos(p) in [1,2] and getright(p) in ["what","why","who","how"])
why.__name__ = "Direct question"

conj = lambda p: (getleftpos(p) in [1] and getleft(p) in ["so","then","and","but","or"]) or (getrightpos(p) in [1] and getright(p) in ["so","then","and","but","or"])
conj.__name__ = "Direct start"

btw = lambda p: getdeptag(p)=="prep_by" and getright(p)=="way" and getrightpos(p)==3
btw.__name__ = "Indirect (btw)"

secondperson = lambda p: 1 not in [getleftpos(p),getrightpos(p)] and len(set([getleft(p),getright(p)]).intersection(["you","your","yours","yourself"]))>0
secondperson.__name__ = "2nd person"


def getparse(document):
  return document['parse']

def select(document, processfun, unittest):
    for l in processfun(document):
        try:
            testres=unittest(l)
            if testres:
                return True
        except Exception, e:
            print e,l
            testres=False
    return False



funset = [
    please, pleasestart, btw, 
    hashedges, really, deference, 
    gratitude, apologize, groupidentity, 
    firstperson, secondperson, secondperson_start,
    firstperson_start, hello, why, conj
]


def getPolitenessFeaturesFromParse(parse, verbose=False):
  """
  parse looks like this--
    {
      "sentences": ["sentence 1", "sentence 2"],
      "parses": [
        ["(dep 1)", "(dep 2)"],
        ["(dep 1)", "(dep 2)"],
      ],
      "words": [
        [toks, one],
        [toks, two]
      ]
    }

  """
  parse_string_list = parse['parses']
  # parse_string_list looks like: [[u'root(ROOT-0, help-2)', u'discourse(help-2, Please-1)', u'dobj(help-2, me-3)', u'prt(help-2, out-4)', u'tmod(help-2, here-5)'], [u'root(ROOT-0, Hi-1)', u'appos(Hi-1, woops-3)', u'nsubj(appreciate-7, I-5)', u'advmod(appreciate-7, really-6)', u'dep(Hi-1, appreciate-7)', u'poss(honesty-10, your-8)', u'amod(honesty-10, unlikely-9)', u'dobj(appreciate-7, honesty-10)']]
  featurelist_dict = defaultdict(list)
  if len(parse['sentences']) == 0:
    # Make sure we still output something.
    all_politeness_features = ['feature_politeness_==1st_person==', 'feature_politeness_==1st_person_pl.==', 'feature_politeness_==1st_person_start==', 'feature_politeness_==2nd_person==', 'feature_politeness_==2nd_person_start==', 'feature_politeness_==Apologizing==', 'feature_politeness_==Deference==', 'feature_politeness_==Direct_question==', 'feature_politeness_==Direct_start==', 'feature_politeness_==Factuality==', 'feature_politeness_==Gratitude==', 'feature_politeness_==Hedges==', 'feature_politeness_==INDICATIVE==', 'feature_politeness_==Indirect_(btw)==', 'feature_politeness_==Indirect_(greeting)==', 'feature_politeness_==Please==', 'feature_politeness_==Please_start==', 'feature_politeness_==SUBJONCTIVE==', 'feature_politeness_=HASHEDGE=','feature_politeness_=HASPOSITIVE=','feature_politeness_=HASNEGATIVE=']
    result = {}
    for f in all_politeness_features:
      result[f] = 0
    return result
  wordslower = map(lambda x: x.lower(), parse['words'])
  for sentence_id in xrange(len(parse['sentences'])):
    # Fake dictionary with parse and text
    d = {}
    d['parse'] = parse_string_list[sentence_id]
    d['text'] = parse['sentences'][sentence_id]
    if verbose:
      print '\t\t', sentence_id, d['text']
      print '\t\t', sentence_id, d['parse']

    for fun in funset:
      featurelist_dict["=="+fun.__name__.replace(" ","_")+"=="].append(int(select(d,getparse,fun)))
    featurelist_dict["==SUBJONCTIVE=="].append(int("could you" in d['text'].lower() or "would you" in d['text'].lower()))
    featurelist_dict["==INDICATIVE=="].append(int("can you" in d['text'].lower() or "will you" in d['text'].lower()))
    featurelist_dict["=HASHEDGE="].append((len(set(d['text'].lower().split()).intersection(hedges))>0))
    featurelist_dict["=HASPOSITIVE="].append(int(len(positivewords.intersection(wordslower))>0))
    featurelist_dict["=HASNEGATIVE="].append(int(len(negativewords.intersection(wordslower))>0))
  # Aggregate all binary features by OR/MAX. Alternatively, one could also sum them up.
  aggregated_features = {}
  for k,v in featurelist_dict.items():
    aggregated_features['feature_politeness_'+k] = max(v)
  return aggregated_features



if __name__ == '__main__':
  
  import re
  from bow_features import getwords
  from parse_api_interface import get_parse

  text = 'Hi, woops, I really appreciate your unlikely honesty.'
  
  parse = get_parse(text)
  print parse

  document = {
    "sentences": [text],
    "parses": [parse],
    "words": getwords({'sentences': [text]})
  }

  print document

  f = getPolitenessFeaturesFromParse(document)

  print sorted(f.keys())

