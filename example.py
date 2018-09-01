#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import logging

logging.basicConfig(level=logging.DEBUG)
logging = logging.getLogger(__file__)

from context_sensitive_summarizer import ContextSensitiveSummarizer

if __name__ == '__main__':

    css = ContextSensitiveSummarizer()

    tests = [
     {"url": "https://hyperallergic.com/455690/what-do-you-do-when-a-project-you-curate-is-censored-by-the-state/", "contexts": ["art", "Yoko Ono", "Spencer Museum", "sculpture"]},
     {"url": "https://www.britannica.com/biography/Yoko-Ono", "contexts": ["Paul McCartney", "Beatles", "Sarah Lawrence"]}
    ]

    for test in tests:
        print('-'*70)
        print('----', test['url'])
        print('-'*70)
        for context, summary in css.summarize(test['url'], test['contexts']):
            print('[%s]: %s' % (context, summary))
        print('-'*70)
        print('\n\n')
