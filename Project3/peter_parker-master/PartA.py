import re
import sys

stop_word = {"a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as",
             "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "but", "buy", "can't",
             "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
             "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having",
             "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how",
             "i", "is", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "it", "it's", "its", "itself", "let's", "me",
             "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or",
             "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd",
             "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their",
             "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll",
             "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "under", "up", "very",
             "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when",
             "where", "when's", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "won't", "would",
             "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"}

# Time Complexity : O(n), n is the length of input text file(number of characters).
# Linear scan the input and find each token that matches the pattern.
# The output is a list of tokens with only lowercase letters, digits, and _
def tokenize(TextFilePath):
    listOfToken = []
    f = open(TextFilePath, "r")
    for line in f:
        line = line.lower()
        listOfToken.extend(re.findall("[a-zA-Z0-9_']+", line))
    f.close()

    return listOfToken
# Time Complexity : O(n), n is the number of tokens of @param listOfToken
# Loop through the list and put into dictionary
# This function only return a dictionary that maps token to number of its occurrences, but not sorting by frequencies.
def computeWordFrequencies(listOfToken):
    myDict = {}
    for token in listOfToken:
        token = str(token)
        if token in stop_word:
            continue
        if token in myDict:
            myDict[token] = myDict[token] + 1
        else:
            myDict[token] = 1
    return myDict

# Time Complexity : O(n log n), n is number of entries in the dictionary
# sort the dictionary by value, then print each entry
def frequencies(myDict):
    sorted_dict = sorted(myDict.items(), key=lambda value: value[1], reverse=True)
    count = 0
    for key, value in sorted_dict:
        print(str(key) + '\t' + str(value))
        count += 1
        if count > 50 :
            break


# Overall, in order to print every key value pairs, the time complexity is O(n log n)
frequencies(computeWordFrequencies(tokenize(sys.argv[1])))


# if alphabetical order is required when same frequency occurs
# sorted_dict = sorted(myDict.items(), key=lambda value: value[0])
# sorted_dict.sort(key=sortByValue, reverse=True)