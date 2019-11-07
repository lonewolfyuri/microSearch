# George Gabricht
# 56735102

# This program runs in O(N + M) time. N is # words and M is # chars in largest file

import PartA, sys

if __name__ == "__main__":
    if len(sys.argv) != 3: # 1
        print("Invalid Arguments: Terminating Program!") # 1
        sys.exit() # 1

    firstWords = PartA.tokenize(sys.argv[1]) # n + m
    secondWords = PartA.tokenize(sys.argv[2]) # n + m

    firstFreq = PartA.computeWordFrequencies(firstWords) # n
    secondFreq = PartA.computeWordFrequencies(secondWords) # n

    result = 0 # 1
    common = [] # 1

    for key in firstFreq.keys(): # n
        if key in secondFreq: # 1
            result += min(firstFreq[key], secondFreq[key]) # 1
            common.append(key) # 1

    print(result) # 1

