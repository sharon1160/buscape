from typing import Dict, List
import uuid
from firebase_admin import db
from uuid import uuid3
from tqdm import tqdm
import json

from parsers import page_rank as prp, inv_index as iip

import app_init


def poblate_pages_and_rank(pages: List, pages_ref: db.Reference, ranks_ref: db.Reference):
    print('Poblating pages and ranks node')
    pages_dict = {}
    rank_dict = {}

    for pageAndRank in tqdm(pages):
        page, rank = pageAndRank
        page_id = uuid3(uuid.NAMESPACE_DNS, page)
        page_id = str(page_id)
        pages_dict[page_id] = page
        rank_dict[page_id] = rank
    pages_ref.update(pages_dict)
    ranks_ref.update(rank_dict)


def poblate_indexes(indexes: Dict, index_ref: db.Reference, pages_ref: db.Reference):
    existent_links = {}
    counter=0
    nextupload=10000
    print('Poblating indexes')
    for word, links in tqdm(indexes.items()):
        existent_links[word] = {}
        for link in links:
            page_id = uuid3(uuid.NAMESPACE_DNS, link)
            page_id = str(page_id)
            link_ref = pages_ref.child(page_id)
            if link_ref is not None:
                    existent_links[word][page_id] = links[link]
        counter+=1
        if counter == nextupload :
            try:
                index_ref.update(existent_links)
                nextupload+=10000
            except NameError:
                print(NameError)
    try:
        index_ref.update(existent_links)
    except NameError:
        print(NameError)
    print(json.dumps(existent_links), file=open('indexes.json', 'w'))


pages = prp.get_pages(withRank=True)
inv_index = iip.get_index()

pages_ref = db.reference('/pages')
ranks_ref = db.reference('/ranks')
index_ref = db.reference('/indexes')

pages_ref.set({})
ranks_ref.set({})
index_ref.set({})

poblate_pages_and_rank(pages, pages_ref, ranks_ref)
poblate_indexes(inv_index, index_ref, pages_ref)
