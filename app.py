
import os
from flask import Flask
from flask import render_template, request

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

@app.route("/")
def hello():
    return "Hello world, it's the Politeness Classifier!"

@app.route("/get-politeness")
def text_input_form():
    return render_template("politeness-form.html")

@app.route("/score-politeness", methods=['POST'])
def send_question():
    text = request.form['text']
    print "Would score"
    print text
    score = 0.0
    return render_template('politeness-result.html', text=text, score=score)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

