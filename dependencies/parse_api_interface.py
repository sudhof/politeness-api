

import requests
from werkzeug.urls import url_fix

API_URL = "http://twitter-app.mpi-sws.org/tmp_python/results.php"

PAYLOAD_TEMPLATE = "%2522$V%2522"

def get_parse(text):
    # Should sentence tokenize here
    sents = [text]
    parses = []
    for s in sents:
        #payload = {"in": PAYLOAD_TEMPLATE.replace("$V", s)}
        #r = requests.get(API_URL, params=payload)
        url = url_fix(API_URL + '?in=%2522' + s + '%2522')
        url = url.replace("+", "%2520")
        r = requests.get(url)
        d = r.text
        d = d[d.find("[[u"):d.find("']]")]
        parses.append(d)
    return parses



if __name__ == "__main__":


    print get_parse("This is a sentence")























