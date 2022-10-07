from flask import Flask, render_template, request
import app_init
import asyncio
import concurrent.futures
import time

from firebase_admin import db

pages_ref = db.reference('/pages')
ranks_ref = db.reference('/ranks')
idx_ref = db.reference('/indexes')

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/")
def home():
    return render_template('index.html')


def make_results(pid, n_coincidences, list_results):
    url = pages_ref.child(pid).get()
    if url is not None:
        list_results.append({'url': url, 'n_coincidences': n_coincidences})


async def results(pid, n_workers, list_results, n_coincidences, event_loop):
    with concurrent.futures.ThreadPoolExecutor(max_workers=n_workers + 2) as executor:
        # print("Fetching: ", pid)
        return await event_loop.run_in_executor(executor, make_results, pid, n_coincidences, list_results)


async def results_range(word, list_results, event_loop):
    # inverted index
    page_ids = idx_ref.child(word).get()
    print("Page ids fetched", len(page_ids))

    coroutines = [results(pid, len(page_ids), list_results,
                          page_ids[pid], event_loop) for pid in page_ids]
    await asyncio.gather(*coroutines)


@app.route("/search", methods=['POST'])
def search():
    word = request.form['word-input']

    list_results = []

    ###
    t0 = time.time()
    event_loop = asyncio.new_event_loop()
    try:
        event_loop.run_until_complete(
            results_range(word, list_results, event_loop))
    finally:
        event_loop.close()
        print('Time elapsed:', (time.time() - t0), 'seconds')
    ###

    return render_template('results.html', results_list=list_results, n_results=len(list_results), word=word)


if __name__ == "__main__":
    app.run()
