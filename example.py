#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import logging

logging.basicConfig(level=logging.INFO)
logging = logging.getLogger(__file__)

from context_sensitive_summarizer import ContextSensitiveSummarizer
from summarizers import *

if __name__ == '__main__':


    tests = [
     {"url": "https://hyperallergic.com/455690/what-do-you-do-when-a-project-you-curate-is-censored-by-the-state/", "contexts": ["art", "Yoko Ono", "Spencer Museum", "sculpture"]},
     {"url": "https://www.britannica.com/biography/Yoko-Ono", "contexts": ["Paul McCartney", "Beatles", "Sarah Lawrence"]},
     {"url": "https://hackernoon.com/top-3-most-popular-programming-languages-in-2018-and-their-annual-salaries-51b4a7354e06", "contexts": ["python", "java"]}
    ]

    for test in tests:
        for summarizer in [MaxFrequencyParagraphSummarizer(), EarliestSentenceSummarizer(), LongestSentenceSummarizer()]:
            css = ContextSensitiveSummarizer(summarizer)
            print('-'*80)
            print('----', "/".join(test['contexts']), '---', summarizer.__class__.__name__)
            print('-'*80)
            for context, summary in css.summarize(test['url'], test['contexts']):
                print('[%s]: %s' % (context, summary))
            print('-'*80)
            print('\n\n')
