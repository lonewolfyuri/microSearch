print("TRYING TO OPEN URLS.TXT")
urlFile = open("urls.txt", "+a")
print("URLS.TXT IS OPENED")
print("TRYING TO OPEN CONTENT.TXT")
contentFile = open("content.txt", "+a")
print("CONTENT.TXT IS OPENED")
maxLength = 0
maxLengthURL = ''
stop_word = {"a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as",
             "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "but", "buy", "can't",
             "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
             "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having",
             "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how",
             "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "it", "it's", "its", "itself", "let's", "me",
             "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or",
             "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd",
             "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their",
             "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll",
             "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "under", "up", "very",
             "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when",
             "where", "when's", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "won't", "would",
             "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"}

