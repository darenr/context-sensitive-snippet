import requests
from bs4 import BeautifulSoup
from gensim.summarization import summarize
from gensim.summarization import keywords

url = "https://hyperallergic.com/455690/what-do-you-do-when-a-project-you-curate-is-censored-by-the-state/"

page = requests.get(url, headers = {'User-agent': 'Mozilla/5.0'})

soup = BeautifulSoup(page.text, 'lxml')
doc = u"\n".join([x.get_text() for x in soup.find_all('p')])
print "keywords", "/", keywords(doc, lemmatize=True, deacc=True).split('\n')
print "-"*70

paragraphs = soup.find_all('p')

contexts = ["Yoko Ono", "Spencer Museum", "sculpture"]

results = {}

for c in contexts:
    results[c] = []

    for p in paragraphs:
        if c.lower() in p.get_text().lower():
            results[c].append(p.get_text())

for k,v in results.iteritems():
    print k, "/", summarize(u"\n".join(v), ratio=0.4, split=True)[0], "\n-----\n"
