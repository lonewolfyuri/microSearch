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
            with open("CurIndex2/" + term + ".txt") as iFile:
                index_terms[term] = eval(iFile.read())
        except FileNotFoundError:
            continue
    return index_terms


def rank_pages(index_terms):
    score_dict = defaultdict(lambda: 0)
    for term in index_terms:
        for id, vals in index_terms[term]:
            tfidf, isTitle, isHead = vals
            if isTitle:
                score_dict[doc_id[id]] += tfidf * 2
            elif isHead:
                score_dict[doc_id[id]] += tfidf * 1.5
#            elif isStrong:
#                score_dict[doc_id[id]] += tfidf * 1.5
            else:
                score_dict[doc_id[id]] += tfidf
    return sorted(score_dict.items(), key = lambda x: -x[1])


if __name__ == "__main__":
    global doc_id
    doc_id = dict()
    with open("CurdocID.txt") as iFile:
        doc_id = eval(iFile.read())
    # print(doc_id)
    
    query = input("Please enter a search query ('quit' to exit): ")
    while(query != "quit"):
        start_time = time.time()
        index_terms = gather_term_dicts(process_query(query))
        # print(index_terms)
        ranked = rank_pages(index_terms)
        # print(ranked)
        for ndx in range(min(len(ranked), 50)):
            print(ranked[ndx][0])
        print("--- %s seconds ---" % (time.time() - start_time))
        query = input("Please enter a search query ('quit' to exit): ")
