# George A Gabricht
# 56735102 - ggabrich
# CS 121 - HW3 Part 1
# =====================
# |     Retriever     |
# =====================


import sys
import tokenizer
from nltk.stem import PorterStemmer
from collections import defaultdict
import time
import math
from collections import OrderedDict
import pickle


'''
This function takes the query as a string and tokenizes it,
then it checks for stop words, if so it ignores them.
Afterwards, it stems each of the remaining terms and returns
the list of stemmed terms in the query.
'''
def process_query(query):
    global stop_dict
    ps = PorterStemmer()
#    q_tokens = tokenizer.tokenList(query)
#    q_stem = []
#    for token in q_tokens:
#        if token not in stop_dict:
#            q_stem.append(ps.stem(token))
#    return q_stem
    return [ps.stem(term) for term in [token for token in tokenizer.tokenList(query) if token not in stop_dict]]


'''
This function analyzes the query for term frequencies,
for the purpose of tfidf. It calcultes the 1 + log10(tf) for
the term in the query.
'''
def analyze_query(query_terms):
    global term_freq
    for term in query_terms:
        term_freq[term] += 1
    for term in term_freq:
        term_freq[term] = 1 + math.log10(term_freq[term])


'''
This function calculates the cosine similarity between
the query and any documents with terms that match the query.
It utilizes champion lists of size 50 to speed up the whole process.
'''
def cosine_score(query_terms):
    global term_freq
    global doc_id
    global all_terms
    # analyzes the query for tf as seen in function above
    analyze_query(query_terms)
    # declares/initializes all necessary variables for cosine similarity
    score_dict = defaultdict(lambda: 0)
    length_dict_query = defaultdict(dict)
    length_dict = {}
    w_tq = defaultdict(dict)
    seen_terms = {}
    champs = {}
    term_index = {}
    '''
    For every term in the processed query,
    1) check if we have seen the term before
    2) if so, reuse it else load it
    3) gather the champion lists for future use
    '''
    for term in query_terms:
        term_index[term] = {}
        # if we have NOT seen this term in the current query,
        # gather its information for cosine similarity
        if term not in seen_terms:
            term_temp = []
            champ_list = []
            # if we have seen the term before, gather it from all_terms
            if term in all_terms:
                # gather docs in posting list and gather champs
                for id, vals in all_terms[term].items():
                    if id == -1:
                        champ_list = vals
                    else:
                        term_index[term][id] = vals
            # else, load the term from file and add it to all_terms
            else:
                all_terms[term] = {}
                term_temp_index = 0
                term_docs = 0
                temp_term = term
                if len(term) >= 3:
                    temp_term = term[0:3]
                try:
                    with open("Index/" + temp_term + ".p", "rb") as iFile:
                        term_temp_index = pickle.load(iFile)
                        term_docs = term_temp_index[term]
#                        print(term_docs)
                except FileNotFoundError:
                    continue
#                print(term_temp_index)
#                print(type(term_temp_index))
                # gather docs in posting list and gather champs
                for id, vals in term_docs.items():
                    all_terms[term][id] = vals
                    if id == -1:
                        champ_list = vals
                    else:
                        term_index[term][id] = vals
            # insert champ docs into champ dictionary for uniqueness
            for id, score in champ_list:
                champs[id] = 0
        # insert term into terms we have seen this query
        seen_terms[term] = 0
    '''
    for each term that we have seen in the query,
    we iterate through each id in the champs list
    and we calculate the tfidf for the query and
    for each document that contains the term,
    then we calculate the length of the query.
    '''
    for term in seen_terms:
        # iterates through the champs dict for ids with higher scores
        for id in champs:
            # if the id is valid for this term, calculate its tfidf
            # (champs list spans multiple terms)
            if id in term_index[term]:
                # weight of term in query for doc is tf(t,q) * idf(t,d)
                w_tq[term][id] = term_freq[term] * term_index[term][id][1]
                tf, idf, isTitle, isHead, isStrong, isAnchor = term_index[term][id]
                if isTitle:
                    score_dict[id] += score * w_tq[term][id] * 1.5
                elif isHead:
                    score_dict[id] += score * w_tq[term][id] * 1.25
                elif isStrong:
                    score_dict[id] += score * w_tq[term][id] * 1.25
                else:
                    score_dict[id] += score * w_tq[term][id]
                # length of query needs w(t,q) squared
                length_dict_query[id][term] = w_tq[term][id] ** 2
                # length_dict_query[id][term] = w_tq[term][id] * w_tq[term][id]
    '''
    this loop iterates through each w(t,q) squared
    and gathers the sum, then calculates the total length
    for cosine similarity purposes.
    '''
    for id, terms in length_dict_query.items():
        len_sum_query = 0
        # for each term and its value in the document, calculate the length
        for term in terms:
            # calculates the sum of all w(t,q) squared
            len_sum_query += length_dict_query[id][term]
        # calculates the squareroot of both lengths and multiplies them
        length_dict[id] = math.sqrt(doc_id[id][2]) * math.sqrt(len_sum_query)
    # calculates the final cosine similarity for each doc
    for id in score_dict:
        score_dict[id] = score_dict[id]/length_dict[id]
    # returns list of all docs ordered by descending cosine similarity
    return sorted(score_dict.items(), key = lambda x: -x[1])
    

def preloadCommonTerms():
#    return
    start_time = time.time()
    global all_terms
    ps = PorterStemmer()
    with open("long_postings_lists.p", "rb") as iFile:
        common_terms = pickle.load(iFile)
#        print(len(common_terms))
#        common_terms_processed = [ps.stem(term) for term in common_terms]
        all_ndx = 0
        for term in common_terms:
            if term not in all_terms:
                term_temp = []
                term_temp_index = {}
                all_terms[term] = {}
                temp_term = term
                if len(term) >= 3:
                    temp_term = term[0:3]
                try:
                    with open("Index/" + temp_term + ".p", "rb") as iFile:
                        term_temp_index = pickle.load(iFile)
    #                    term_temp = term_temp_index[term]
                except FileNotFoundError:
                    continue
                except KeyError:
                    continue
                # gather docs in posting list and gather champs
    #            print(term_temp)
                for cur_term, ids in term_temp_index.items():
                    if cur_term not in all_terms:
#                        all_ndx += 1
                        all_terms[cur_term] = {}
                        for id, vals in ids.items():
                            all_terms[cur_term][id] = vals
#    print(all_ndx)
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    # dict that contains the url, token size and length of each doc
    global doc_id
    # a dictionary of stop words for query processing
    global stop_dict
    # a dictionary of 1 + log10(tf) for terms in the query
    global term_freq
    # dictionary of all terms we have seen in all queries, saves load time
    global all_terms
    stop_list = ["and", "i", "a", "about", "an", "are", "as", "at", "be", "by", "com", "for", "from", "how", "in", "is", "it", "of", "on", "or", "that", "the", "this", "to", "was", "what", "when", "where", "who", "will", "with", "the", "www"]
    stop_dict = {}
    all_terms = {}
    for term in stop_list:
        stop_dict[term] = 0
    doc_id = dict()
    with open("docID.p", "rb") as iFile:
        doc_id = pickle.load(iFile)
    
    preloadCommonTerms()
    
    query = input("Please enter a search query ('quit' to exit): ")
    while (query != "quit"):
        term_freq = defaultdict(lambda: 0)
        start_time = time.time()
        ranked = cosine_score(process_query(query))
        result = []
        for ndx in range(min(len(ranked), 50)):
            print(doc_id[ranked[ndx][0]][0])
        print(len(ranked))
        print("--- %s seconds ---" % (time.time() - start_time))
        query = input("Please enter a search query ('quit' to exit): ")

