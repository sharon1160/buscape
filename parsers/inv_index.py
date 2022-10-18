results_path = '../output/invertedindex.txt'


def get_index(res_file=None):
    if res_file is None:
        res_file = open(results_path, 'r', encoding='utf-8')
    lines = res_file.readlines()
    inv_index = {}
    for line in lines:
        word, links = line.split('\t')
        inv_index[word] = {}
        out_links = links.strip().split('|')
        for i in range(0, len(out_links) - 1, 2):
            inv_index[word][out_links[i]] = int(out_links[i + 1])
    return inv_index


if __name__ == '__main__':
    indexes = get_index()
    for word, olinks in indexes.items():
        print(word, olinks)
