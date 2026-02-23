import requests
import sys
from bs4 import BeautifulSoup


def get_soup(page_url):
    response = requests.get(page_url )
    return BeautifulSoup(response.text, 'lxml')

def get_title_text(s):
    if s.title:
        return s.title.text.strip()
    else:
        return ""
    

def get_body_text(s):
    
    if s.body:
        return s.body.get_text()
    else:
        return ""


def get_all_urls(s):
    urls=[]
    for link in s.find_all('a'):
        href = link.get('href')
        if href:
            urls.append(href)

    return urls

page_url = sys.argv[1]
s=(get_soup(page_url))
print(get_title_text(s))
print(get_body_text(s))

for url in get_all_urls(s):
    print(url)
    