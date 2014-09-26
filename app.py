
import os
import datetime
import math
from flask import Flask
from flask import render_template, request, jsonify

from politeness_model import score_politeness, check_is_request

#from db_utils import add_reclassification, print_all_reclassifications
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])


#############################################
## SQLite reclassification db code

HOST = os.environ.get("HOST", False)
DB_FILENAME = "sqlite:///" + os.environ.get("SQLITE_FILENAME", ":memory:")
app.config['SQLALCHEMY_DATABASE_URI'] = DB_FILENAME
db = SQLAlchemy(app)

if HOST == "heroku":
    print "On heroku, creating DB"
    db.create_all()


class Reclassification(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    label = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, text, label):
        self.text = text
        self.label = label

    def __repr__(self):
        return "<Reclassification(id=%d, text='%s', label='%s', created_at='%s')>" % (
                                self.id, self.text, self.label, str(self.created_at))


def print_all_reclassifications():
    print "\n\n"
    print "-- reclassifications --"
    recs = Reclassification.query.all()
    for rec in recs:
        print "\t", rec

def add_reclassification(text, label):
    rec = Reclassification(text, label)
    db.session.add(rec)
    db.session.commit()


#############################################



@app.route("/")
def text_input_form():
    # Try to figure out if we're on mpi-sws or not
    # If not, tell everyone this is a debugging site
    off_mpi_flag = bool(os.environ.get("HOST", False))
    return render_template("politeness-form.html", off_mpi_flag=off_mpi_flag)


@app.route("/get-politeness")
def text_input_form2():
    return render_template("politeness-form.html")


@app.route("/submit-reclassification", methods=['POST'])
def submit_reclassification():
    text = request.form['text']
    label = request.form['label']
    add_reclassification(text, label)
    print_all_reclassifications()
    return jsonify(success=True)


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

