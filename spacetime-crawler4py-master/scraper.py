import re
from typing import Any
from urllib.parse import urlparse, urljoin
import utils
import lxml
from lxml import html
import Tokenizer
from bs4 import BeautifulSoup
import os

pageCount = 0
wordMax = 0
wordF = {}
subDomains = {}
listUrls = []
responses = []


def scraper(url, resp):
    global pageCount
    global wordMax
    global wordF
    global subDomains
    global listUrls

    links = extract_next_links(url, resp)
    # print("LINKS: ")
    # print(links)
    result = [link for link in links if is_valid(link)]
    # print("RESULT: ")
    # print(result)

    with open("scraper_output.txt", "w") as f:
        f.write("Page Count: ")
        f.write(str(pageCount))
        f.write("\n\n")

        f.write("Max Words: ")
        f.write(str(wordMax))
        f.write("\n\n")

        f.write("Subdomains: ")
        f.write(str([dmn for dmn in sorted(subDomains.items(), key = lambda x: -x[1])]))
        f.write("\n\n")

        f.write("Sorted Words: \n")
        f.write(str([word for word in sorted(wordF.items(), key=lambda x: -x[1])]))
    return result


def extract_next_links(url, resp):
    global pageCount
    global wordMax
    global wordF
    global subDomains
    global listUrls
    global responses

    links = []
    # check for codes here
    if 200 <= resp.status < 400:
        # if resp.raw_response.is_redirect:

        pageCount += 1

        parsed = urlparse(url)
        if parsed.netloc.endswith("ics.uci.edu"):
            if parsed.netloc not in subDomains:
                subDomains[parsed.netloc] = 1
            else:
                subDomains[parsed.netloc] += 1
        if len(listUrls) > 10:
            for pge in listUrls[-6:-1]:
                if '20' or '19' in url:
                    if url[0:url.find('19')] == pge[0:pge.find('19')]:
                        return links
                    if url[0:url.find('20')] == pge[0:pge.find('20')]:
                        return links
                if len(url) >= 100 and len(pge) >= 100:
                    if url[0:100] == pge[0:100]:
                        return links

        try:
            listUrls.append(url)
            parsed = html.fromstring(resp.raw_response.content)

            # Tokenize and save to file here

            soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
            words = Tokenizer.tokenList(soup.get_text())
            wordFreq = Tokenizer.computeWordFrequencies(words)
            wordC = 0
            for word in wordFreq:
                wordC += wordFreq[word]
                if word in wordF:
                    wordF[word] += wordFreq[word]
                else:
                    wordF[word] = wordFreq[word]
            if wordC > wordMax:
                wordMax = wordC

        # urlParsed = urlparse(url)
        # fn = "index/" + urlParsed.netloc + urlParsed.path
        # try:
        #    os.makedirs(fn)
        # except:
        #    print()
        # fn = fn + ".txt"
        # f = open(fn, "w")
        # f.write(str(wordFreq))
        # f.close()

            if '#' in url:
                url = url[0:url.find('#')]

            for el, attr, link, pos in parsed.iterlinks():
                # print(link)
                if (url != link):
                    if (is_valid(link)):
                        links.append(link)
                    else:
                        links.append(urljoin(url, link))
        except:
            return links


    # Implementation requred.
    return links


def is_valid(url):
    global pageCount
    global wordMax
    global wordF
    global subDomains
    global listUrls

    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        elif not (
                parsed.netloc.endswith("ics.uci.edu") or parsed.netloc.endswith("cs.uci.edu") or parsed.netloc.endswith(
                "informatics.uci.edu") or parsed.netloc.endswith("stat.uci.edu") or parsed.netloc.endswith(
                "today.uci.edu")):
            return False
        elif parsed.netloc.endswith("today.uci.edu") and not parsed.path.startswith(
                "department/information_computer_sciences"):
            return False
        elif 'stayconnected/stayconnected' in url:
            return False
        elif 'hall_of_fame/hall_of_fame' in url:
            return False
        elif 'archive.ics' in url:
            return False
        elif 'advising/advising' in url:
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise


if __name__ == "__main__":
    pass
