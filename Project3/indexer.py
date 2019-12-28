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
from collections import defaultdict
from urllib.parse import urlparse


class termTracker:
    count = 0
    pos = []


'''
Python Standard Library provides an abstract base class
for HTML Parsing. This class inherits from this base class
and parses all HTML tags as well as data.
'''
class HTMLPrsr(HTMLParser):
    isTitle = False
    isHead = False
    ps = PorterStemmer()
    tknSize = 0

    # This method handles start tags and checks for headers or title tags
    def handle_starttag(self, tag, attrs):
        if "title" in tag:
            self.isTitle = True
        elif "h1" or "h2" or "h3" in tag:
            self.isHead = True
    
    # This method handles end tags and checks for headers or title tags
    def handle_endtag(self, tag):
        if "title" in tag:
            self.isTitle = False
        elif "h1" or "h2" or "h3" in tag:
            self.isHead = False
    
    '''
    This method handles data blocks appropriately by first tokenizing
    then counting number of times it occurs in doc, stemming each term
    and finally calculating the tfidf and checking if is within a header
    or title tag before inserting into the Index all pertinent information.
    '''
    def handle_data(self, data):
        global index
        global curUrl
        # tokenizes the data using the tokenizer we built in project 1
        result = tokenizer.tokenList(data)
        # calculates the number of total tokens in the document
        self.tknSize += len(result)
        # creates a dictionary for word freq of terms w/ default val 0
        curDict = defaultdict(termTracker)
        pos = 1
        for term in result:
            # stems each term using porter stemmer (nltk)
            term = self.ps.stem(term)
            # increments the occurence of this term by 1
            curDict[term] = termTracker()
            curDict[term].count += 1
            curDict[term].pos.append(pos)
            pos += 1
        for term, item in curDict.items():
            # if current url is not already in dict under term
            if ndx not in index[term]:
                # computer tfidf (term count / total doc word count
                tfidf = (item.count / self.tknSize)
                # store the tfidf, title and header status under value
                # of current url in the index dictionary's term value dict.
#                index[term][ndx] = (tfidf, self.isTitle, self.isHead, item.pos)
                index[term][ndx] = (tfidf, self.isTitle, self.isHead)


if __name__ == '__main__':
    # creates our global index and curUrl vars
    global index
    global curUrl
    global doc_id
    global ndx
    index = defaultdict(dict)
    curUrl = ""
    doc_id = dict()
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
    docCount = 0
    for ndx in range(len(files)):
        file = files[ndx]
        # prints file for debugging / to watch progress
        print(file)
        with open(file) as iFile:
            # reads the json file and prepares for parsing
            jsn = iFile.read()
            docCount += 1
            # parses the json file into a dictionary
            parsed = json.loads(jsn)
            # gets the current url from the dictionary
            if '#' in parsed["url"]:
                curUrl = parsed["url"][0:parsed["url"].find('#')]
            else:
                curUrl = parsed["url"]
            doc_id[ndx] = curUrl
            # creates a new HTML parser
            parser = HTMLPrsr()
            # parses the html content as seen above
            parser.feed(parsed["content"])
    tokenCount = 0
    # print(str(index.items()))
    with open("docID.txt", "w") as oFile:
        oFile.write(str(doc_id))
    # iterates through the index, term is the term being used & val is dict
    for term, vals in index.items():
        tokenCount += 1
        # try to create a new file with term.txt as file name
        try:
            with open("Index/" + term + ".txt", "w") as oFile:
                oFile.write(str(sorted(vals.items(), key = lambda x: x[0])))
        # except in the case of file name too long
        except OSError:
            continue
    # creates a file for out report containing doc count and token count
    with open("indexer_output.txt", "w") as oFile:
        oFile.write("Doc Count: " + str(docCount) + "\n")
        oFile.write("Token Count: " + str(tokenCount))
