from flask import Flask, render_template, request
import app_init
from firebase_admin import db

pages_ref = db.reference('/pages')
ranks_ref = db.reference('/ranks')
idx_ref = db.reference('/indexes')

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/search", methods=['POST'])
def search():
    word = request.form['word-input']
    return results(word)


def task(pid, results):
    print("Fetching: ", pid)
    page_url = pages_ref.child(pid).get()
    results[page_url] = page_ids[pid]


@app.route("/results/<word>")
def results(word):

    # inserting
    page_ids = idx_ref.child(word).get()
    print("Page ids fetched", len(page_ids))
    results = {}

    # Falta paralelizar FOR
    for pid in page_ids:
        print("Fetching: ", pid)
        page_url = pages_ref.child(pid).get()
        results[page_url] = page_ids[pid]

    return render_template('results.html', results=results)


if __name__ == "__main__":
    app.run()
