
import os
import math
from flask import Flask
from flask import render_template, request, jsonify

from politeness_model import score_politeness

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])



"""
@app.route("/")
def hello():
    return "Hello world, it's the Politeness Classifier!"
"""

@app.route("/")
def text_input_form():
    return render_template("politeness-form.html")


@app.route("/get-politeness")
def text_input_form2():
    return render_template("politeness-form.html")


@app.route("/score-politeness", methods=['POST'])
def score_text():
    text = request.form['text']
    probs = score_politeness(text)

    # Based on probs, determine label and confidence
    if probs['polite'] > 0.65:
        l = "polite"
        confidence = probs['polite']
    elif probs['impolite'] > 0.65:
        l = "impolite"
        confidence = probs['impolite']
    else:
        l = "neutral"
        confidence = 1.0 - math.fabs(probs['polite'] - 0.5) 

    confidence = "%.2f" % confidence

    # Return JSON:
    return jsonify(text=text, label=l, confidence=confidence)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

