# Scrape an nginx Fancy Index directory, save all links in a .txt for aria2

import requests
from bs4 import BeautifulSoup
import os
import urllib.parse as urp
import sys

file = open(os.path.expanduser('~') + '\\Desktop\\links.txt', 'w', encoding='utf-8')
visited = set()
frontier = list()

s = requests.Session()

def find_urls(url):
    r = s.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    ite = soup.find_all('a')

    return [urp.urljoin(url, link.get('href')) for link in ite if link.get('href') != '../']

def is_valid(url:str, base:str):
    try:
        parsed = urp.urlparse(url)
        if parsed.netloc != urp.urlparse(base).netloc:  # different domain name
            return False
        
        if url in visited:                              # visited url
            return False
        
        if parsed.query != "":                          # url with query string (starting with '?')
            return False

        return True

    except:
        return False

def run(base:str):
    while len(frontier) != 0:
        url = frontier.pop()
        print('visit: ' + url)
        visited.add(url)
        if url[-1] == "/":
            new_urls = find_urls(url)
            frontier.extend([link for link in new_urls if is_valid(link, base)])
        else:
            file.write(url + '\n')
            file.write(' out=' + urp.unquote(url[len(base):]) + '\n\n')

if __name__ == '__main__':
    base = sys.argv[1]
    frontier.append(base)
    run(base)

file.close()
