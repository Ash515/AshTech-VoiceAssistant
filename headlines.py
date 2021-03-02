import requests
from bs4 import BeautifulSoup


def get_headlines(url):
    info = {'text': [], 'link': []}
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    for line in soup.findAll('span', {'class': 'w_tle'}):
        info['text'].append(line.text)
        link = line.find('a')['href']
        if link[0] == '/':
            link = 'https://timesofindia.indiatimes.com' + link
        info['link'].append(link)
    return info
