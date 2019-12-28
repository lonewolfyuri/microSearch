# George A Gabricht
# 56735102 - ggabrich
# CS 121 - HW3 Part 1
# =====================
# |      Indexer      |
# =====================

import json
import sys
import os
from html.parser import HTMLParser
import tokenizer
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import OrderedDict
from collections import defaultdict
from urllib.parse import urlparse
import math
import pickle

# container class that holds
# important information for term in doc
class termTracker:
    count = 0
    pos = []
    isTitle = False
    isHead = False
    isStrong = False
    isAnchor = False


'''
Python Standard Library provides an abstract base class
for HTML Parsing. This class inherits from this base class
and parses all HTML tags as well as data.
'''
class HTMLPrsr(HTMLParser):
    isTitle = False
    isHead = False
    isStrong = False
    isAnchor = False
    ps = PorterStemmer()
    tknSize = 0
    pos = 1

    # This method handles start tags and checks for headers or title tags
    def handle_starttag(self, tag, attrs):
        if "title" in tag:
            self.isTitle = True
        if "h1" or "h2" or "h3" in tag:
            self.isHead = True
        if "strong" in tag:
            self.isStrong = True
        if "href" in attrs:
            self.isAnchor = True
        if tag == "a":
            self.isAnchor = True
    
    # This method handles end tags and checks for headers or title tags
    def handle_endtag(self, tag):
        if "title" in tag:
            self.isTitle = False
        if "h1" or "h2" or "h3" in tag:
            self.isHead = False
        if "strong" in tag:
            self.isStrong = False
        if tag == "a":
            self.isAnchor = False
        
    
    '''
    This method handles data blocks appropriately by first tokenizing
    then counting number of times it occurs in doc, stemming each term
    and checking if is within a header or title tag. Furthermore, if the term is not currently in the index, it loads the term from disk and merges in order of docID.
    '''
    def handle_data(self, data):
        global index
        global curUrl
        global term_dict
        global curDict
        # tokenizes the data using the tokenizer we built in project 1
        result = tokenizer.tokenList(data)
        # calculates the number of total tokens in the document
        self.tknSize += len(result)
        # iterates through every tokenized term
        for term in result:
            # stems each term using porter stemmer (nltk)
            term = self.ps.stem(term)
            # if the term is not already present in the index
            # attempt to load it from disk
            if term not in index:
                # grab the first 3 chars or less if term is short
                temp_term = term
                if len(term) >= 3:
                    temp_term = term[0:3]
                # try to open the term from file
                try:
                    # reads the file frmo disk in binary mode
                    with open("Index/" + temp_term + ".p", "rb") as iFile:
                        # pickle load the dictionary from disk
                        term_index = pickle.load(iFile)
                        # for each term in the new dictionary,
                        # insert its values into the index
                        for cur_term, ids in term_index.items():
                            # for each docID in the term dict,
                            # insert its postings into index
                            for id, val in ids.items():
                                index[cur_term][id] = val
                # except if file does not exist
                except FileNotFoundError:
                    pass
            # inserts the term into the terms dictionary
            term_dict[term] = 0
            # increments the occurence of this term by 1
            curDict[term].count += 1
            #curDict[term].pos.append(self.pos)
            #self.pos += 1
            if not curDict[term].isHead:
                curDict[term].isHead = self.isHead
            if not curDict[term].isTitle:
                curDict[term].isTitle = self.isTitle
            if not curDict[term].isStrong:
                curDict[term].isStrong = self.isStrong
            if not curDict[term].isAnchor:
                curDict[term].isAnchor = self.isAnchor
        # updates docID with the documents new length
        url, terms, length = doc_id[ndx]
        doc_id[ndx] = (url , self.tknSize, length)


'''
This function splits the files into 4 batches
of equal length, for the purpose of offloading
the index from memory later.
'''
def get_batch(files):
    result = []
    f_len = len(files)
    result.append(files[0 : (f_len // 4)])
    result.append(files[(f_len // 4) : 2 * (f_len // 4)])
    result.append(files[2 * (f_len // 4) : 3 * (f_len // 4)])
    result.append(files[3 * (f_len // 4) : ])
    return result


# This function dumps the current index to disk
def sort_write_to_disk():
    print("Dumping")
    terms_to_write = defaultdict(dict)
    # gathers the terms in the index
    for term, o_dict in index.items():
        # determines which file term will go into
        temp_term = term
        if len(term) >= 3:
            temp_term = term[0:3]
        # prepares term to be written to proper file
        terms_to_write[temp_term][term] = o_dict
    # for term in gathered terms, dump term into appropriate file
    for temp_term, terms in terms_to_write.items():
        with open("Index/" + temp_term + ".p", "wb") as oFile:
            pickle.dump(terms, oFile)


#    with open("temp_index_" + str(ndx_batch) + ".txt", "w") as oFile:
#        oFile.write(str(index))
#    for term, val in index.items():
#        with open("temp_index_" + ndx + ".txt", "a") as oFile:
#            oFile.write(str(sorted(vals.items(), key = lambda x: x[0])))

'''
this function builds the index batch by batch,
offloading the partial index at the end of each batch
and starting fresh with a new index.
'''
def build_index(doc_files):
    global index
    global curUrl
    global doc_id
    global doc_count
    global ndx
    global term_dict
    global curDict
    # gets the batches to be iterated over
    batches = get_batch(doc_files)
    # for each batch in batches, build partial index
    for batch in batches:
        # for each document in the batch, process the document
        for doc in batch:
            # creates a new dictionary for the current document
            curDict = defaultdict(termTracker)
            # opens the document for processing
            with open(doc) as iFile:
                # keeps track of the docID
                ndx += 1
                # reads the file for json parsing
                jsn = iFile.read()
                # tracks number of documents
                doc_count += 1
                # parses the json file
                parsed = json.loads(jsn)
                # strips the fragment from the url
                if '#' in parsed["url"]:
                    curUrl = parsed["url"][0:parsed["url"].find('#')]
                else:
                    curUrl = parsed["url"]
#                if "maven-contents.txt" in curUrl:
#                    continue
                # prints the url for debugging purposes
                print(curUrl)
                # initializes the docID in the docID dict
                doc_id[ndx] = (curUrl, 0, 0)
                # creates a new HTML parser
                parser = HTMLPrsr()
                # parses the html content as seen above
                parser.feed(parsed["content"])
            '''
            for each term in the document,
            calculates the normalized tf and inserts
            the term into the index, if it isn't already in the index
            for that particular posting
            '''
            for term, item in curDict.items():
                # if current url is not already in dict under term
                if ndx not in index[term]:
                    # computer tfidf (term count / total doc word count
                    tf = 1 + math.log10(item.count)
                    idf = 0
                    # store the tfidf, title and header status under value
                    # of current url in the index dictionary's term value dict.
    #                index[term][ndx] = (tfidf, self.isTitle, self.isHead, item.pos)
                    index[term][ndx] = (tf, idf, item.isTitle, item.isHead, item.isStrong, item.isAnchor)
        # dumps the partial index to disk
        sort_write_to_disk()
        # resets the index as new dict for future processing
        index = defaultdict(OrderedDict)


'''
This function loads each term from disk, calculates the idf,
calculates champion lists and dumps the term back to disk.
'''
def calculate_idfs(term_dict):
    global doc_id
    global long_postings_lists
    seen_terms = {}
    # for each term in the terms dictionary, calculate the term's idf
    for term in term_dict:
        # if we haven't already processe the term
        if term not in seen_terms:
            temp_term_index = 0
            # try to create a new file with term.txt as file name
            temp_term = term
            if len(term) >= 3:
                temp_term = term[0:3]
            # opens the file for binary reading
            with open("Index/" + temp_term + ".p", "rb") as iFile:
                # pickle loads the file into dict
                temp_term_index = pickle.load(iFile)
                # for each term in the dict, calculate its idf
                for cur_term, ids in temp_term_index.items():
                    temp_ids = ids
                    sz = len(ids)
                    tfidfs = {}
                    # calculates the most common terms across all docs
                    if cur_term not in stop_list and sz > 1000:
                        long_postings_lists.append(term)
                    # for each posting in the term, update its values
                    for id, val in ids.items():
                        tf, idf, isTitle, isHead, isStrong, isAnchor = val
                        # idf = log10(size of corpus / # of docs term appears in)
                        idf = math.log10(len(doc_id) / sz)
                        url, size, length = doc_id[id]
                        # length of doc is sqrt(tfidf(t,d)**2)
                        length += (tf * idf) ** 2
                        doc_id[id] = url, size, length
                        temp_ids[id] = (tf, idf, isTitle, isHead, isStrong, isAnchor)
                        tfidfs[id] = tf * idf
                    # calculates champions list for the term
                    temp_ids[-1] = [item for item in sorted(tfidfs.items(), key = lambda x: -x[1])][0:50]
                    # makes note of seen terms so we don't repeat
                    seen_terms[cur_term] = 0
                    # loads the updated postings list into dict
                    temp_term_index[cur_term] = temp_ids
            # dumps the postings list to disk for each term.
            with open("Index/" + temp_term + ".p", "wb") as oFile:
                pickle.dump(temp_term_index, oFile)=


if __name__ == '__main__':
    
    global index
    global curUrl
    global doc_id
    global ndx
    global doc_count
    global term_dict
    global stop_list
    global long_postings_lists
    long_postings_lists = []
    stop_list = ["and", "i", "a", "about", "an", "are", "as", "at", "be", "by", "com", "for", "from", "how", "in", "is", "it", "of", "on", "or", "that", "the", "this", "to", "was", "what", "when", "where", "who", "will", "with", "the", "www"]
    term_dict = {}
    doc_count = 0
    index = defaultdict(OrderedDict)
    curUrl = ""
    doc_id = dict()
    ndx = 0
    path = ""
    
    # checks for command line path input
    if len(sys.argv) == 2:
        path = sys.argv[1]
    # else uses DEV path as default
    else:
        path = "./DEV"
    files = []
    # walks the path directory tree and joins paths together for each file.
    for root, folderNames, fileNames in os.walk(path):
        for file in fileNames:
            if not file.endswith(".DS_Store"):
                files.append(os.path.join(root, file))
                
    build_index(files)
    token_count = 0
    # iterates through the index, term is the term being used & val is dict
    calculate_idfs(term_dict)
    for id in doc_id:
        url, sz, length = doc_id[id]
        doc_id[id] = (url, sz, math.sqrt(length))
    with open("docID.p", "wb") as oFile:
        pickle.dump(doc_id, oFile)
    with open("long_postings_lists.p", "wb") as oFile:
        pickle.dump(long_postings_lists, oFile)
