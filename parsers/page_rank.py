results_path = './data/resultpagerank.txt'


def get_pages(res_file=None, withRank=False):
    if res_file is None:
        res_file = open(results_path, 'r', encoding='utf-8')
    lines = res_file.readlines()
    pages = []
    for line in lines:
        pageAndRank, outlinks = line.split('\t')
        page, rank = pageAndRank.split('|')
        if withRank:
            pages.append((page, float(rank)))
        else:
            pages.append(page)
    return pages


if __name__ == '__main__':
    pages = get_pages()
    set_pages = set(pages)
    print(pages, len(pages), len(set_pages))
