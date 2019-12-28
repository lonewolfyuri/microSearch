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
import threading


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


def thread_load(term):
    global champs
    global term_index
    global all_terms
    global sem_terms
#    global sem_all_terms
#    global sem_term_index
#    global sem_champs
    term_temp = []
    champ_list = []
    try:
        with open("Index/" + term + ".txt") as iFile:
            term_temp = eval(iFile.read()[11:])
    except FileNotFoundError:
        return
    sem_terms.acquire()
    # gather docs in posting list and gather champs
    for item in term_temp:
        id, vals = item
#        sem_all_terms.acquire()
        all_terms[term][id] = vals
#        sem_all_terms.release()
        if id == -1:
            champ_list = vals
        else:
#            sem_term_index.acquire()
            term_index[term][id] = vals
#            sem_term_index.release()
    sem_terms.release()
    sem_champs.acquire()
    # insert champ docs into champ dictionary for uniqueness
    for id, score in champ_list:
        champs[id] = score
    sem_champs.release()


'''
This function calculates the cosine similarity between
the query and any documents with terms that match the query.
It utilizes champion lists of size 50 to speed up the whole process.
'''
def cosine_score(query_terms):
    global term_freq
    global doc_id
    global all_terms
#    global sem_all_terms
#    global sem_term_index
    global sem_champs
    global sem_terms
    global term_index
    global champs
    sem_terms = threading.Semaphore()
#    sem_all_terms = threading.Semaphore()
#    sem_term_index = threading.Semaphore()
    sem_champs = threading.Semaphore()
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
    thread_terms = []
    threads = []
    '''
    For every term in the processed query,
    1) check if we have seen the term before
    2) if so, reuse it else load it
    3) gather the champion lists for future use
    '''
    for term in query_terms:
        # if we have NOT seen this term in the current query,
        # gather its information for cosine similarity
        if term not in seen_terms:
            term_index[term] = {}
            # if we have seen the term before, gather it from all_terms
            if term in all_terms:
                term_temp = []
                champ_list = []
                # gather docs in posting list and gather champs
                for id, vals in all_terms[term].items():
                    if id == -1:
                        champ_list = vals
                    else:
                        term_index[term][id] = vals
                # insert champ docs into champ dictionary for uniqueness
                for id, score in champ_list:
                    champs[id] = score
            # else, load the term from file and add it to all_terms
            else:
                thread_terms.append(term)
        # insert term into terms we have seen this query
        seen_terms[term] = 0
    for term in thread_terms:
        all_terms[term] = {}
        new_thread = threading.Thread(target = thread_load, args = (term,))
        new_thread.start()
        threads.append(new_thread)
    for thread in threads:
        thread.join()
    '''
    for each term that we have seen in the query,
    we iterate through each id in the champs list
    and we calculate the tfidf for the query and
    for each document that contains the term,
    then we calculate the length of the query.
    '''
    for term in seen_terms:
        # iterates through the champs dict for ids with higher scores
        for id, score in champs.items():
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
    global all_terms
    common_terms = []
    for term in common_terms:
        cosine_score(process_query(term))


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
    with open("docID.txt") as iFile:
        doc_id = eval(iFile.read())
    
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


