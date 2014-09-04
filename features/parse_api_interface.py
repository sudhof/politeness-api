
import re
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
    dependencies = eval(d)
    parse = [dp for s in dependencies for dp in s]
    return parse



if __name__ == "__main__":

    print "\n\n"
    print get_parse("This is one sentence. And it is followed by a second.")
    print "\n\n"
    print get_parse("Hi, woops, I really appreciate your unlikely honesty.")
    print "\n\n"
    print get_parse("Please help me out here. Hi, woops, I really appreciate your unlikely honesty.")























