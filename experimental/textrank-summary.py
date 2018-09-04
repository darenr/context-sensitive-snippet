from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords

import requests

from bs4 import BeautifulSoup

url="https://en.wikipedia.org/wiki/Deep_learning"

page = requests.get(url).text
soup = BeautifulSoup(page, "lxml")
text = ' '.join(map(lambda p: p.text, soup.find_all('p')))


print ('Summary:')
print (summarize(text, ratio=0.01))

print ('\nKeywords:')
print (keywords(text, ratio=0.01))
