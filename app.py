from flask import Flask, render_template, request

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/")
def home():
  return render_template('index.html')

@app.route("/search", methods=['POST'])
def search():
  word = request.form['word-input']
  return results(word)

@app.route("/results/<word>")
def results(word):
  list_results = [word, word, word]
  return render_template('results.html', list_results = list_results)

if __name__ == "__main__":
  app.run()
