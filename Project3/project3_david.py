from pathlib import Path
from bs4 import BeautifulSoup as bs4
import json
import nltk
import sys
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.util import ngrams
from nltk.stem import PorterStemmer
import collections
import operator
import re

'''
This mocule contains four function and two are core.
1.	scanning_doc: it determind path is valid (which means path exist)
		if it exists, it calls scanning_recursive.
2.	scanning_recursive: two main actions. find subdirectory, and calling
		"scanning_files" if there is files in the specific folder.
3.	scanning_file: append the files to the list.
4.	print_all
		print them all, one file by line.

'''
def scanning_doc(mypath: Path) -> list:
    '''
    This function check the path is existing or not. That's all.
    If it exists, call scanning_recursive function. otherwise, Exception.
    '''
    mylist = []
    try:
        if (mypath.exists()):
            mylist = scanning_recursive(mypath)
        else:
            print('Something wrong. Mypath should be correct. then my list will be the return value')
        '''
        Just to memorize as a practice.
        IOError : if file can’t be opened
        KeyboardInterrupt : when an unrequired key is pressed by the user
        ValueError : when built-in function receives a wrong argument
        EOFError : if End-Of-File is hit without reading any data
        ImportError : if it is unable to find the module
        '''
        return mylist
    except IOError:
        print("IO ERROR")
    except KeyboardInterrupt:
        print("Keyboard Error")
    except ValueError:
        print("Value Error")
    except EOFError:
        print("EOFError.")
    finally:
        print("This is finall statement")

def scanning_recursive(mypath: Path) -> [Path]:
    '''
    It does with following direction.
    1.	in mypath folder, look for files there by using scanning_files function,
            then add them to mylist if there is any files.
    2. 	sort all component (files and subdirectory), and iteration.
    3. 	if a component is directory, then recursively execute
            "scanning_recursive" function meaning
            a. after enter the first subdirectory,
            b. scan files by "scanning_files", and add them to mylist
            c. After complete file iteration, sort all component (files and sub-subdirectory). If there is subdirectories of the subdirectory,
            then recursive. If not... go to step 4.
    4. 	It is the status of completion on the first subdirectory. do it work on
            the second directory... until it complete the last subdirectory component
    '''
    # This below is the function call of scanning_files.
    mylist.extend(scanning_files(mypath))

    # This is a recursive function to find subdirectories
    for x in sorted(mypath.iterdir()):
        if x.is_dir():
            scanning_recursive(x)
    return mylist

def scanning_files(mypath: Path) -> [Path]:
    '''
    It is for two purpose.
    1.  scanning files in the path.
    2.  make temporary list and sort it. After that, return the sorted files list

    '''
    temp = []
    for x in mypath.iterdir():
        if (x.is_file() and (not x.name == '.DS_Store')):
            ''' if x is file and the name is not ".DS_Store" '''
            temp.append(str(x))
    temp = sorted(temp)
    # print(len(temp))
    return temp

# def print_all(mylist: [Path]) -> [Path]:
#     '''It is just to see what are stored in the mylist'''
#     for x in mylist:
#         print(x)

def create_docID(mylist: list) -> dict:
    '''
    Assigning numbers and increase as it iterate the list.
    While numbering, creating two dictionaries.

    mylist_docID1: {0: name_of_doc0, 1: name_of_doc1 ...}
    mylist_docID2: {name_of_doc0: 0, name_of_doc1: 1 ...}
    '''
    n = 0
    mylist_docID1 = {}
    mylist_docID2 = {}
    for x in mylist:
        mylist_docID1[n] = x
        mylist_docID2[x] = n
        n += 1
    '''
    After making two dictionaries, they create JSON file respectively
    '''
    with open("project3_ID_to_DOC_david_working.json", 'w') as docID_json1:
        docID_json1.write(json.dumps(mylist_docID1))
    with open("project3_DOC_to_ID_david_working.json", 'w') as docID_json2:
        docID_json2.write(json.dumps(mylist_docID2))
    print()
    '''
    returning these two list. I don't think they must remain in memory
    However, I remained them just for interim period.
    '''
    return mylist_docID1, mylist_docID2

def reading_docID(mypath: Path) -> dict:
    with open(mypath, 'r') as project3_docID:
        docID_dict = json.load(project3_docID)

    try:
        print('docID_dict["0"] is ', docID_dict['0'])
        # print('docID_dict["55392"] is ', docID_dict['55392'])
    except:
        print('exception error in reading_docID function')
    '''
    will return dictionary from JSON file.
    '''
    return docID_dict


def extract_html_from_json(mypath: Path):
    '''
    Pulling html from JSON, and the key is whether the file has key 
    "content"
    If not, raise exception, but later it needs to be implemented.
    Because there are some text based file containing text,
    and prof answered that it also needed to be parsed/index
    in piazza post.
    '''
    
    try:
        with open(mypath) as f:
            test_dict = json.load(f)
            extracted_html = test_dict['content']
            if extracted_html == None:
                print('PATH IS ', mypath)

            return extracted_html
    except:
        print('Error of function extract_html_from_json')

def html_parse(extracted_html, path):
    soup = bs4(extracted_html, "html.parser")
    # print(soup.prettify())
    # print(soup.text)
    mystring = soup.text
    mystring2 = line = re.sub(r'\b\W*',' ',mystring)

    return text_tokenize(mystring2, path)


    '''
    It needs two separate way to getting text before tokenize.
    First. there are JSON file format having only text in "content" class. If we use filter using tag, it retuns NONE. How to handle this?

    Second, html parse, below is the right approach?


    print('\n=============\t P \t =============\n')
    for x in soup.find_all(['p']):
        print(x, n)
        print(x.string)
        print('\n\n next p \n\n ')
        n += 1
    print('\n=============\t TITLE \t =============\n')
    n = 0
    for x in soup.find_all(['title']):
        print(x, n)
        print(x.string)
        print('\n\n next title \n\n ')
        n += 1
    print('\n=============\t A \t =============\n')
    n = 0
    for x in soup.find_all(['a']):
        print(x, n)
        print(x.string)
        print('\n\n next a \n\n ')
        n += 1
    print('\n=============\t LI \t =============\n')
    n = 0
    for x in soup.find_all(['li']):
        print(x, n)
        print(x.string)
        print('\n\n next li \n\n ')
        n += 1
    '''



def text_tokenize(mystring: str, path: Path):
    sequence = word_tokenize(mystring)

    print(sequence)
    Inverted_index = collections.namedtuple('Inverted_index', ['docID', 'freq', 'stem'])
    n = docID_dict2[str(path)]
    ps = PorterStemmer()

    for i in sequence:
        
        if(i not in myinverted_index):
            i = Inverted_index(n, 1, ps.stem(i))
            # myinverted_index[i]['tdidf-score'] = 'tbd'
        elif(i in myinverted_index):
            i = i._replace(freq = i.freq + 1)
        else:
            print('=====\n=====\n===== what happens? \n\n')

    print(myinverted_index)
    '''
    After making one page tokenize, need to sort alphabetically
    '''

    sorted_inv_index = sorted(myinverted_index.items(), key=operator.itemgetter(0))
    
    sorted_inv_index = dict(sorted_inv_index)

    # print('size of sorted_inv_index', sys.getsizeof(sorted_inv_index))

    '''
    create index file.
    '''
    create_index_file(sorted_inv_index)

    return sorted_inv_index

    
def create_index_file(myindex: dict) -> None:
    with open("project3_invertedindex_david.json", 'a') as myinverted_index:
        myinverted_index.write(json.dumps(myindex))

def read_index() -> dict:
    with open("project3_invertedindex_david.json", 'r') as myindex:
        myinvertedindex = json.load(myindex)
    return myinvertedindex



'''
plan is tokenize, count frequency, adding docID


another thing might be...
making creating text based file (txt or json) that can contain {index:{docID:0, stem: 'something', frequency:22, dfidf(scoring):44}}
Aha: it can be JSON format and might be easy to convert between
JSON and dict. (right?)

setting up frequenct to transfer data in memory to file and merge etc.

'''
        

if __name__ == '__main__':
    mylist = []
    
    mypath = Path('/users/davidlee/downloads/03_CS121_project03/analyst/')

    mylist = scanning_doc(mypath)
    # print('size of mylist (full name of docs) is in mem', sys.getsizeof(mylist))

    mylist_docID1, mylist_docID2 = create_docID(mylist)
    '''
    create_docID returns dictionary of {numbering:original name of doc} just for interim. Another task in the funciton is creating json document having {index:the name of document}.
    '''
    print('size of docID/doc dict in mem', sys.getsizeof(mylist_docID1))

    docID_dict1 = reading_docID("./project3_ID_to_DOC_david_working.json")
    docID_dict2 = reading_docID("./project3_DOC_to_ID_david_working.json")

    # print(docID_dict1)
    # print(docID_dict2)
    for i in mylist:
        # print('\n\n\n')
        # # print(i)
        # print('\n\n\n')
        extracted_html = extract_html_from_json(i)
        html_parse(extracted_html, i)

    # print('\n\n\n\n\n')
    # readindex = read_index()

