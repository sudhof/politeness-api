
import os
import math
from flask import Flask
from flask import render_template, request, jsonify

from politeness_model import score_politeness, check_is_request

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])



"""
@app.route("/")
def hello():
    return "Hello world, it's the Politeness Classifier!"
"""

@app.route("/")
def text_input_form():
    # Try to figure out if we're on mpi-sws or not
    # If not, tell everyone this is a debugging site
    off_mpi_flag = bool(os.environ.get("HOST", False))
    return render_template("politeness-form.html", off_mpi_flag=off_mpi_flag)


@app.route("/get-politeness")
def text_input_form2():
    return render_template("politeness-form.html")


@app.route("/score-politeness", methods=['POST'])
def score_text():
    text = request.form['text']
    probs = score_politeness(text)
    isrequest = check_is_request()
    print "is_request:",isrequest

    # Based on probs, determine label and confidence
    if probs['polite'] > 0.6:
        l = "polite"
        confidence = probs['polite']
    elif probs['impolite'] > 0.6:
        l = "impolite"
        confidence = probs['impolite']
    else:
        l = "neutral"
        confidence = 1.0 - math.fabs(probs['polite'] - 0.5)

    ##C: changing to percentages
    #confidence = "%.2f" % confidence
    confidence = "%.0f%%" % (float(confidence)*100)
    print confidence

    # Return JSON:
    return jsonify(text=text, label=l, confidence=confidence, isrequest=isrequest)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

