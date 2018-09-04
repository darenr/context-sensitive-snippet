from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.edmundson import EdmundsonSummarizer   #found this is the best as
from nltk.corpus import stopwords
from string import punctuation


LANGUAGE = "english"
SENTENCES_COUNT = 5

if __name__ == "__main__":

    url="https://www.artsy.net/article/artsy-editorial-photographing-fading-american-dream-prefab-homes"

    parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))

    print ("--EdmundsonSummarizer--")
    summarizer = EdmundsonSummarizer()
    summarizer.bonus_words = ("deep", "learning", "neural" )
    summarizer.stigma_words = set(stopwords.words('english') + list(punctuation))
    summarizer.null_words = ["art"]
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        print(sentence)
