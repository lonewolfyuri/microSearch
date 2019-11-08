from pathlib import Path
from bs4 import BeautifulSoup as bs4
import json

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


def scanning_files(mypath: Path) -> [Path]:
    '''
    It is for two purpose.
    1.	scanning files in the path.
    2. 	make temporary list and sort it. After that, return the sorted files list

    '''
    temp = []
    for x in mypath.iterdir():
        if (x.is_file() and (not x.name == '.DS_Store')):
            ''' if x is file and the name is not ".DS_Store" '''
            temp.append(x)
    temp = sorted(temp)
    print(len(temp))
    return temp


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


def print_all(mylist: [Path]) -> [Path]:
    '''It is just to see what are stored in the mylist'''
    for x in mylist:
        print(x)


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


if __name__ == '__main__':
    mylist = []
    mypath = Path('/users/davidlee/downloads/03_CS121_project03/part_of_Analyst_for_practice/')

    scanning_doc(mypath)
    ###################
    #
    # Below contains some drills which may not be directly related.
    # But these are outcome of learning result in progress
    # and I think these will probably be used for making outcome.
    # Any comments are welcome.
    #
    ####################
    '''
    HTML extraction after loading JSON file.
    '''
    my_html_list = []
    for x in mylist:
        print('mylist loop')
        try:
            with open(x) as f:
                test_dict = json.load(f)
                # print('printing content', test_dict["content"])
                my_html_list.append(test_dict['content'])
                ''' it is because html is the value of key content'''

        except:
            print(x)
            print('There is no key "content" ')

    '''
    I scanned folder that I intentionally made.
    In the folder, there were three JSON file.
    However, two were not containing html content, but only one.
    Just want to see above for-loop scan the right file and
    put the right thing into the list.

    After confirming it works well, Below was to figure out which text/string
    is stored along with which html_tag. Of course, it is also for my drilling purpose to learn BeautifulSoup more.

    '''
    print(len(my_html_list))
    print(type(my_html_list[0]))
    soup = bs4(my_html_list[0], "html.parser")

    print(soup.prettify())
    print('============================')
    print('soup.title', soup.title)
    print()
    print('soup.find_all("title")', soup.find_all(['title']))
    print()
    print('soup.title.string', soup.title.string)
    print()
    print('soup.p', soup.p)
    print()
    print('soup.find_all("p")', soup.find_all(['p']))
    print()
    print('soup.find_all("b")', soup.find_all(['b']))
    print()
    print('soup.find_all("a")', soup.find_all(['a']))
    print()
    print('soup.find("a")', soup.find(['a']))
