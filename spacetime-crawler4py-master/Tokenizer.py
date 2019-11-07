# George Gabricht
# 56735102

import sys


# helper function that tokenizes a file string in C style.
# this function runs in O(M) time. M is # chars in file
def tokenList(fileString):
    stopWords = ["and", "i", "a", "about", "an", "are", "as", "at", "be", "by", "com", "for", "from", "how", "in", "is", "it", "of", "on", "or", "that", "the", "this", "to", "was", "what", "when", "where", "who", "will", "with", "the", "www"]
    res = []  # 1
    temp = ""  # 1
    for charz in fileString:  # m
        try:  # 1
            curChar = ord(charz)  # 1
            if curChar < 48 or (57 < curChar < 65) or (90 < curChar < 97) or curChar > 122:  # 1
                if temp != "" and len(temp) > 1:
                    temp = temp.lower()
                    isStop = False
                    for word in stopWords:
                        if (word == temp):
                            isStop = True;
                            break;
                    if not isStop:
                        res.append(temp)  # 1
                temp = ""  # 1
            else:  # 1
                temp += charz  # 1
        except:  # 1
            temp = ""  # 1
    if len(temp) > 0:  # 1
        res.append(temp)  # 1
    return res  # 1


# List<Token> tokenize(TextFilePath)
# reads in text file, returns list of tokens in file.
# token = sequence of alphanumeric chars, case-less.
# this function runs in O(M + N) time. Where M is # chars & N is # words in file.
def tokenize(TextFilePath):
    try:  # 1
        iFile = open(TextFilePath, 'r')  # 1
    except:  # 1
        print("File Error, Exiting Now")  # 1
        raise IOError()  # 1

    fileStr = iFile.read()  # 1
    wordList = tokenList(fileStr)  # m
    result = []  # 1
    for word in wordList:  # n
        try:
            result.append(word.lower())  # 1
        except:  # 1
            continue  # 1
    return result  # 1


# Map<Token, Count> computeWordFrequencies(List<Token>)
# counts number of occurrences of each token in token list
# this function runs in O(N) time. N is the # of words in list
def computeWordFrequencies(tokens):
    wordFreq = {}  # 1
    for token in tokens:  # n
        if token in wordFreq:  # 1
            wordFreq[token] += 1  # 1
        else: # 1
            wordFreq[token] = 1  # 1
    return wordFreq  # 1


# void print(Map<Token, Count>)
# prints out word frequency onto screen in decreasing order
# this function runs in O(N log N) time. N is the # of keys in map
def Print(wordFreq):
    sortedWords = sorted(wordFreq.items(), key=lambda x: -x[1])  # n log n
    for word in sortedWords:  # n
        print(word)  # 1


if __name__ == "__main__":
    if len(sys.argv) != 2:  # 1
        print("Invalid Arguments: Terminating Program!")  # 1
        sys.exit()  # 1

    firstWords = tokenize(sys.argv[1])  # m + n
    wordFreq = computeWordFrequencies(firstWords)  # n
    Print(wordFreq)  # n log n
