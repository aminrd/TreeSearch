from bs4 import BeautifulSoup
import urllib
from urllib.parse import urlsplit
import lxml.html
import re
import argparse


# ------------------
DEBUG_MODE = True
# ==================



def getLinks(url):
    domain = base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page)
    links = []

    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        links.append(link.get('href'))

    for link in soup.findAll('a', attrs={'href': re.compile("^/")}):
        links.append(domain + link.get('href')[1:])

    return links

def doesContain(url , lookfor):

    if DEBUG_MODE:
        print('Searching url: ' + url)

    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page)

    return soup.text.__contains__(lookfor)


def TreeSearch(url = 'http://cs.ubc.ca/~aghaee/', depth = 1, lookfor = 'Amin'):

    if depth == 0:
        if doesContain(url, lookfor):
            return url
        else:
            return -1

    result = []
    links = getLinks(url)

    for link in links:
        sub_result = TreeSearch(link, depth -1 , lookfor)

        if sub_result != -1:
            result = result + sub_result

    return result


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str)
    parser.add_argument('lookfor', type=str)
    parser.add_argument('-d', '--depth', type=int, default=1)
    args = parser.parse_args()

    result = TreeSearch(args.url, args.depth, args.lookfor)

    print('Results:\n====================')
    if len(result) < 1:
        print("~~Nothing found!~~")
    else:
        print(result)
