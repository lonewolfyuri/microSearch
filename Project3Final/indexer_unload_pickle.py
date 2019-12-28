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
import transformer
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import OrderedDict
from collections import defaultdict
from urllib.parse import urlparse
import math
import pickle

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
    and finally calculating the tfidf and checking if is within a header
    or title tag before inserting into the Index all pertinent information.
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
        # creates a dictionary for word freq of terms w/ default val 0
        for term in result:
            # stems each term using porter stemmer (nltk)
            term = self.ps.stem(term)
            # increments the occurence of this term by 1
            if term not in index:
                try:
                    with open("Index/" + term + ".p", "rb") as iFile:
                        temp_index = pickle.load(iFile)
    #                    print(temp_index)
                        for id, val in temp_index.items():
                            index[term][id] = val
                except OSError:
                    pass
            term_dict[term] = 0
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
        url, terms, length = doc_id[ndx]
        doc_id[ndx] = (url , self.tknSize, length)



def get_batch(files):
    result = []
    f_len = len(files)
    result.append(files[0 : (f_len // 4)])
    result.append(files[(f_len // 4) : 2 * (f_len // 4)])
    result.append(files[2 * (f_len // 4) : 3 * (f_len // 4)])
    result.append(files[3 * (f_len // 4) : ])
    return result


def sort_write_to_disk():
    for term, o_dict in index.items():
        try:
            with open("Index/" + term + ".p", "wb") as oFile:
                pickle.dump(o_dict, oFile)
        except OSError:
            print("os error")
            continue


#    with open("temp_index_" + str(ndx_batch) + ".txt", "w") as oFile:
#        oFile.write(str(index))
#    for term, val in index.items():
#        with open("temp_index_" + ndx + ".txt", "a") as oFile:
#            oFile.write(str(sorted(vals.items(), key = lambda x: x[0])))


def build_index(doc_files):
    global index
    global curUrl
    global doc_id
    global doc_count
    global ndx
    global term_dict
    global curDict
    batches = get_batch(doc_files)
    for batch in batches:
        for doc in batch:
            curDict = defaultdict(termTracker)
            with open(doc) as iFile:
                ndx += 1
                jsn = iFile.read()
                doc_count += 1
                parsed = json.loads(jsn)
                if '#' in parsed["url"]:
                    curUrl = parsed["url"][0:parsed["url"].find('#')]
                else:
                    curUrl = parsed["url"]
                print(curUrl)
                doc_id[ndx] = (curUrl, 0, 0)
                # creates a new HTML parser
                parser = HTMLPrsr()
                # parses the html content as seen above
                parser.feed(parsed["content"])
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
#                    if term not in stop_list or item.count < 100:
#                        index[term][ndx] = (tf, idf, item.isTitle, item.isHead, item.isStrong, item.isAnchor, item.pos)
#                    else:
#                        index[term][ndx] = (tf, idf, item.isTitle, item.isHead, item.isStrong, item.isAnchor, [])
        sort_write_to_disk()
        index = defaultdict(OrderedDict)


def calculate_idfs(term):
    global doc_id
    global long_postings_lists
    term_index = dict()
    # try to create a new file with term.txt as file name
    try:
        with open("Index/" + term + ".p", "rb") as iFile:
            term_index = pickle.load(iFile)
            sz = len(term_index)
            tfidfs = {}
            if term not in stop_list and len(term_index) > 1000:
                long_postings_lists.append(term)
            for id, val in term_index.items():
                tf, idf, isTitle, isHead, isStrong, isAnchor = val
                idf = math.log10(len(doc_id) / sz)
                url, sz, length = doc_id[id]
                length += (tf * idf) * (tf * idf)
                doc_id[id] = url, sz, length
                term_index[id] = (tf, idf, isTitle, isHead, isStrong, isAnchor)
                tfidfs[id] = tf * idf
            term_index[-1] = [item for item in sorted(tfidfs.items(), key = lambda x: -x[1])][0:50]
        with open("Index/" + term + ".p", "wb") as oFile:
            pickle.dump(term_index, oFile)
    # except in the case of file name too long
    except OSError:
        pass


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
    # index = defaultdict(OrderedDict)
    # rebuild_index()
    token_count = 0
    # iterates through the index, term is the term being used & val is dict
    for term in term_dict:
#        token_count += 1
        calculate_idfs(term)
    for id in doc_id:
        url, sz, length = doc_id[id]
        doc_id[id] = (url, sz, math.sqrt(length))
    with open("docID.p", "wb") as oFile:
        pickle.dump(doc_id, oFile)
    with open("long_postings_lists.p", "wb") as oFile:
        pickle.dump(long_postings_lists, oFile)
    # creates a file for out report containing doc count and token count
#    with open("indexer_output.txt", "w") as oFile:
#        oFile.write("Doc Count: " + str(doc_count) + "\n")
#        oFile.write("Token Count: " + str(token_count))
