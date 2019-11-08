import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs
from crawler.file import urlFile, contentFile
import crawler.file as file
from bs4.element import Comment

urlSet = set()


def tag_visible(element):
    # Return false if element is in certain tags
    if element.parent.name in {'style', 'script', 'head', 'title', 'meta', '[document]'}:
        return False
    # Return false if element is a comment in HTML
    if isinstance(element, Comment):
        return False
    if re.match(r"[\s\r\n]+", str(element)):
        return False
    return True


def write_to_file(url, soup):
    true_link = str(url).split('#')[0]
    result = urlparse(url)
    if true_link not in urlSet:
        urlSet.add(true_link)                                   # Add unique url to set
        if "pdf" not in result.path.lower():
            urlFile.write(true_link + '\n')                     # Append unique url to file
            content = soup.findAll(text=True)                   # Finding text in HTML file

            real_text = filter(tag_visible, content)

            length = 0
            for frag in real_text:
                length += len(str(frag).split())
                contentFile.write(frag+"\n")

            # Finding file that has largest content
            if length > file.maxLength:
                file.maxLength = length
                file.maxLengthURL = url
                print("Current largest page is ", url, "      word count : ", str(file.maxLength))


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    # Only extract links that is 200 or 302 status code
    if 200 <= resp.status <= 399:
        raw_resp = resp.raw_response
        soup = bs(raw_resp.content, 'lxml')

        # Getting all href link
        all_links = soup.findAll("a")

        # Writing content to file
        write_to_file(url, soup)

        # should remove fragment from here
        to_return = [(link.get("href")) for link in all_links]
        print("We found " + str(len(urlSet)) + " unique URLs")
        return to_return
    else:
        return list()


def is_valid(url):
    parsed = ''
    try:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            return False

        '''
        Links that matches *.ics.uci.edu*
                        *.cs.uci.edu*
                        *informatics.uci.edu*
                        *stat.uci.edu*
                        www.today.uci.edu/department/information_computer_sciences
        are valid links
        '''
        #good_link = re.match(r"((www\.)?([a-zA-Z0-9\-]+\.)+(i?cs|informatics|stat)\.uci\.edu)"
        #                     + r"|(www\.)?today\.uci\.edu/department/information_computer_sciences", parsed.netloc)

        authority = parsed.netloc
        is_today = re.match(r"(www\.)?today\.uci\.edu/department/information_computer_sciences", url)
        valid_domain = (authority.endswith("ics.uci.edu") or authority.endswith("cs.uci.edu")
                        or authority.endswith("stat.uci.edu") or authority.endswith("informatics.uci.edu") or is_today)

        # Avoid redundant url
        #redundant = re.match(r"(www\.)?(archive\.ics\.uci\.edu)", url)

        bad_link = authority.endswith("archive.ics.uci.edu")
        return valid_domain and not bad_link and "calendar" not in url and not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz|txt|r|c|py|m|rb|nb)$", parsed.path.lower())

    except TypeError:
        print("TypeError for ", parsed)
        raise
