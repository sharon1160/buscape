from flask import Flask, render_template, request
from flask_paginate import Pagination, get_page_args
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


def make_results(pid, n_coincidences, page_rank, list_results):
    url = pages_ref.child(pid).get()
    list_results.append(
        {'url': url, 'n_coincidences': n_coincidences, 'page_rank': page_rank})


async def results(pid, n_workers, list_results, n_coincidences, page_rank, event_loop):
    with concurrent.futures.ThreadPoolExecutor(max_workers=n_workers + 2) as executor:
        # print("Fetching: ", pid)
        return await event_loop.run_in_executor(executor, make_results, pid, n_coincidences, page_rank, list_results)


async def results_range(word, list_results, event_loop):
    # inverted index
    page_ids = idx_ref.child(word).get()
    print("Page ids fetched", len(page_ids))

    # page rank
    page_rank_ids = ranks_ref.get()

    coroutines = [results(pid, len(page_ids), list_results, page_ids[pid],
                          page_rank_ids[pid], event_loop) for pid in page_ids if pid in page_rank_ids]
    await asyncio.gather(*coroutines)


def sort_by_pagerank(list_results):
    return sorted(list_results, key=lambda d: d['page_rank'], reverse=True)

def get_results(list_results, offset=0, per_page=10):
    return list_results[offset: offset + per_page]

@app.route("/")
def home():
    return render_template('index.html')


list_results = []
word = ''

@app.route("/search", methods=['POST', 'GET'])
def search():
    global list_results
    global word
    if request.method == 'POST':
        word = request.form['word-input']

        if word != '':

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

            list_results = sort_by_pagerank(list_results)

            page, per_page, offset = get_page_args(page_parameter="page",per_page_parameter="per_page")

            total = len(list_results)

            pagination_results = get_results(list_results, offset = offset, per_page = per_page)

            pagination = Pagination(page = page, per_page = per_page, total = total, css_framework = 'bootstrap5')

            return render_template('results.html',
                                    n_results = total,
                                    word = word,
                                    pagination_results = pagination_results,
                                    page = page,
                                    per_page = per_page,
                                    pagination = pagination)
    else:
        page, per_page, offset = get_page_args(page_parameter="page",per_page_parameter="per_page")

        total = len(list_results)

        pagination_results = get_results(list_results, offset = offset, per_page = per_page)

        pagination = Pagination(page = page, per_page = per_page, total = total, css_framework = 'bootstrap5')

        return render_template('results.html',
                                n_results = total,
                                word = word,
                                pagination_results = pagination_results,
                                page = page,
                                per_page = per_page,
                                pagination = pagination)

if __name__ == "__main__":
    app.run()
