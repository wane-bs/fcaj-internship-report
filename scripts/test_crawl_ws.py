import urllib.request
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

url = "https://000005.awsstudygroup.com/vi/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')
    topics = soup.find('ul', class_='topics')
    if topics:
        links = []
        for a in topics.find_all('a', href=True):
            full = urljoin(url, a['href'])
            title = a.get_text(strip=True)
            links.append((title, full))
        print(f"Extracted {len(links)} navigation links from {url}:")
        for t, l in links[:10]:
            print(f"  - {t} -> {l}")
    else:
        print("No ul.topics found, using regex")
except Exception as e:
    print(f"Error: {e}")
