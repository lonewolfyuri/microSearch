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


class HTMLPrsr(HTMLParser):
    title = False
    head = False
    ps = PorterStemmer()
    tknSize = 0

    def handle_starttag(self, tag, attrs):
        if "title" in tag:
            self.title = True
        elif "h1" or "h2" or "h3" in tag:
            self.head = True
    
    def handle_endtag(self, tag):
        if "title" in tag:
            self.title = False
        elif "h1" or "h2" or "h3" in tag:
            self.head = False
    
    def handle_data(self, data):
        global index
        global curUrl
        
        result = tokenizer.tokenList(data)
        self.tknSize += len(result)
        curDict = {}
        newResult = []
        for term in result:
            term = self.ps.stem(term)
            if term in curDict:
                curDict[term] += 1
            else:
                curDict[term] = 1
            newResult.append(term)
        for term in newResult:
            if term not in index:
                index[term] = []
            isIn = False
            for url, score, title, head in index[term]:
                if curUrl == url:
                    isIn = True
            if not isIn:
                tfidf = (curDict[term] / self.tknSize)
                index[term].append((curUrl, tfidf, self.title, self.head))
        
        
        # result = tokenizer.tokenList(data)
        # trans = transformer.transform(result)
        # for term in trans:
        #    if term not in index:
        #        index[term] = []
        #    isIn = False
        #    for item in index[term]:
        #        if curUrl == item:
        #            isIn = True
        #    if not isIn:
        #        index[term].append(curUrl)
                


if __name__ == '__main__':
    global index
    index = dict()
    global curUrl
    curUrl = ""
    path = ""
    if len(sys.argv) == 2:
        path = sys.argv[1]
    else:
        path = "./TEST"
    files = []
    for root, folderNames, fileNames in os.walk(path):
        for file in fileNames:
            if "DS_Store" in file:
                continue
            files.append(os.path.join(root, file))
    docCount = 0
    for file in files:
        with open(file) as iFile:
#                print(iFile)
            jsn = iFile.read()
            docCount += 1
            parsed = json.loads(jsn)
            for name, val in parsed.items():
                if name == "url":
                    curUrl = val
                elif name == "content":
                    parser = HTMLPrsr()
                    parser.feed(val)
                else:
                    pass
#                with open("test_out.txt", "w") as f:
#                    f.write(str(index))
    tokenCount = 0
    for name, val in index.items():
        tokenCount += 1
        with open("Index/" + name + ".txt", "w") as oFile:
            oFile.write(str(val))
    
    with open("indexer_output.txt", "w") as oFile:
        oFile.write("Doc Count: " + str(docCount) + "\n")
        oFile.write("Token Count: " + str(tokenCount))
