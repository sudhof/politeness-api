
import os

##############
# uses command-line java tool to get parses

from dependencies.parser import StanfordDependencyParser

def get_parse_commandline(text):
    parse = StanfordDependencyParser().parse([text])
    return parse.get(text, [])


##############
# uses local server to access parsing functionality
# (collapses dependency parses into one list)

from json import loads
import jsonrpc

def get_parse_jsonrpc(text):
    dependencies = getdepparse(text)
    parse = [dp for s in dependencies for dp in s]
    return parse


def getdepparse(text):
    if text == "Q": ##Silly jsonrpc bug, that closes the session when receiving Q
        text = "Q "
    server = jsonrpc.ServerProxy(jsonrpc.JsonRpc20(),jsonrpc.TransportTcpIp(addr=("127.0.0.1", 3456)))
    result = loads(server.parse(text))
    newdeps = []
    for sent in result['sentences']:
        newdepssent = []
        for t in sent['dependencies']:
            newdepssent.append(t)
        newdeps.append(newdepssent)
    return newdeps



##############
# This code accesses mpi-sws parsing server. 
# Now defunct, connecting to parser locally


"""
import requests
from werkzeug.urls import url_fix

API_URL = "http://twitter-app.mpi-sws.org/tmp_python/results.php"
PAYLOAD_TEMPLATE = "%2522$V%2522"

def get_parse(text):
    # Text should be a single sentence
    url = url_fix(API_URL + '?in=%2522' + text + '%2522')
    url = url.replace("+", "%2520")
    r = requests.get(url)
    d = r.text
    d = d[d.find("[[u"):d.find("']]")+3]
    try:
        dependencies = eval(d)
        parse = [dp for s in dependencies for dp in s]
    except:
        print "Eval'ing dependencies failed; falling back to simple split"
        parse = d[4:-3].split("', u'")
    return parse
"""

##############
# determine parsing function based on environment variables

host = os.environ.get("HOST", False)

print os.environ
print host

if host in ("localhost", "heroku"):
    # need to access commandline for parses
    get_parse = get_parse_commandline
else:
    # On mpi-sws
    get_parse = get_parse_jsonrpc



if __name__ == "__main__":

    print "\n\n"
    print get_parse("This is one sentence. And it is followed by a second.")
    print "\n\n"
    print get_parse("Hi, woops, I really appreciate your unlikely honesty.")
    print "\n\n"
    print get_parse("Please help me out here. Hi, woops, I really appreciate your unlikely honesty.")

