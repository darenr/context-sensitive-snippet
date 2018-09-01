#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import requests, logging
from bs4 import BeautifulSoup
from collections import defaultdict
from textblob import TextBlob

class MaxFrequencyParagraph(object):
    #
    # return a summary limited to the first 3 sentences for whatever
    # paragraph in the document contains the most occurences of the entity
    #
    def summarize(self, entity, paragraphs):
        haystack = []
        for p in paragraphs:
            if entity.lower() in p.lower():
                haystack.append((TextBlob(p).sentences, p.lower().count(entity.lower())))

        if haystack:
            summary_paragraph = sorted(haystack, key=lambda x: x[1], reverse=True)[0]
            summary = u'. '.join([unicode(x) for x in summary_paragraph[:2]])
            logging.debug('MaxFrequencyParagraph::summarize::entity(%s), summary = [%s]' % (entity, doc, summary))
            return summary

class EarliestSentenceSummarizer(object):
    #
    # simple text summarizer by simply returning the first sentence
    # containing the given entity
    #
    def summarize(self, entity, paragraphs):
        doc = u'\n'.join(paragraphs)
        haystack = [x for x in TextBlob(doc).sentences if entity.lower() in u''.join(x).lower()]
        if haystack:
            earliest = haystack[0]
            logging.debug('EarliestSentenceSummarizer::summarize::entity(%s), summary = [%s]' % (entity, doc, earliest))
            return earliest

class LongestSentenceSummarizer(object):
    #
    # simple text summarizer by simply returning the longest sentence
    # containing the given entity
    #
    def summarize(self, entity, paragraphs):
        doc = u'\n'.join(paragraphs)
        haystack = [x for x in TextBlob(doc).sentences if entity.lower() in u''.join(x).lower()]
        if haystack:
            longest = max(haystack, key=len)
            logging.debug('LongestSentenceSummarizer::summarize::entity(%s), summary = [%s]' % (entity, doc, longest))
            return longest

class ContextSensitiveSummarizer(object):

    def __init__(self, summarizer = MaxFrequencyParagraph()):
        self.headers = {'User-agent': 'Mozilla/5.0'}
        self.summarizer = summarizer

    def summarize(self, url, contexts):
        page = requests.get(url, headers = self.headers)

        soup = BeautifulSoup(page.text, 'lxml')
        paragraphs = [x.get_text() for x in soup.find_all('p')]
        results = []
        for k in contexts:
            summary = self.summarizer.summarize(k, paragraphs)
            if summary:
                results.append((k, summary))

        return results
