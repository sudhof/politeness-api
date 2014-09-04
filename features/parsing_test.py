



from dependencies.parser import StanfordDependencyParser
from parse_api_interface import get_parse
from politeness_strategies import getPolitenessFeaturesFromParse

docs = [
    "can you not understand my question?",
    "are you stupid??",
    "Could you would you please is it any trouble?",
    "Yooo man can someone out there help me here?",
    "This is a sentence.",
    "Do you know who can help me?"
]

text2parse = StanfordDependencyParser().parse(docs)
parse1 = [text2parse[t] for t in docs]

parse2 = []
for d in docs:
    parse2.append(get_parse(d))

for t, p1, p2 in zip(docs, parse1, parse2):
    print t
    d = {
        "sentences": [t],
        "parses": [p1], 
        "words": t.split()
    }
    f1 = getPolitenessFeaturesFromParse(d)
    d['parses'] = [p2]
    f2 = getPolitenessFeaturesFromParse(d)

    ks = f1.keys()
    for k in ks:
        if f1[k] == 1:
            print "Good! ", k
        if f1[k] != f2[k]:
            print "\nERR: ", k

    """
    p1 = set(p1)
    p2 = set(p2)
    c = p1 & p2
    if len(c) !=  len(p1) or len(c) != len(p2):
        print "\nERRR"
        print filter(lambda x: x not in p2, list(p1))
        print filter(lambda x: x not in p1, list(p2))
    """

