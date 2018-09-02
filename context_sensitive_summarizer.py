#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import requests, logging
from bs4 import BeautifulSoup

from summarizers import *

class ContextSensitiveSummarizer(object):


    def __init__(self, summarizer):
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
