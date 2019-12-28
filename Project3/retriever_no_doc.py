# George A Gabricht
# 56735102 - ggabrich
# CS 121 - HW3 Part 1
# =====================
# |     Retriever     |
# =====================


import sys
# import os
# from html.parser import HTMLParser
import tokenizer
# import transformer
from nltk.stem import PorterStemmer
# from nltk.tokenize import sent_tokenize, word_tokenize
from collections import defaultdict
import time
# from contextlib import ExitStack


def process_query(query):
    q_tokens = tokenizer.tokenList(query)
    # q_tokens = word_tokenize(query)
    ps = PorterStemmer()
    q_stem = []
    for term in q_tokens:
        q_stem.append(ps.stem(term))
    return q_stem


def gather_term_dicts(q_stem):
    index_terms = dict()
#    filenames = []
#    files = []
#    for term in q_stem:
#        filenames.append("CurIndex/" + term + ".txt")
#    with ExitStack() as stack:
#        files = [stack.enter_context(open(fname)) for fname in filenames]
#        for ndx in range(len(q_stem)):
#            index_terms[term] = eval(files[ndx].read()[10:])
    for term in q_stem:
        try:
            with open("Index1/" + term + ".txt") as iFile:
                index_terms[term] = eval(iFile.read()[10:])
        except FileNotFoundError:
            continue
    return index_terms


def rank_pages(index_terms):
    score_dict = defaultdict(lambda: 0)
    for term in index_terms:
        for url, vals in index_terms[term]:
            tfidf, is_title, is_head = vals
            if is_title:
                score_dict[url] += tfidf * 2
            elif is_head:
                score_dict[url] += tfidf * 1.5
            elif term in url:
                score_dict[url] += tfidf * 1.25
            else:
                score_dict[url] += tfidf
    return sorted(score_dict.items(), key = lambda x: -x[1])


if __name__ == "__main__":
    start_time = time.time()
    query = ""
    if len(sys.argv) == 2:
        query = sys.argv[1]
    else:
        query = input("Please enter a search query: ")
    
    index_terms = gather_term_dicts(process_query(query))
    # print(index_terms)
    ranked = rank_pages(index_terms)
    # print(ranked)
#    for ndx in range(min(len(ranked), 50)):
#        print(ranked[ndx][0])
    print("--- %s seconds ---" % (time.time() - start_time))

