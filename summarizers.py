#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import requests, logging, re
from textblob import TextBlob

#
# make each summarizer base off a common class that takes care
# of finding the haystacks
#

class BaseSummarizer(object):

    def _contains(self, needle, haystack):
        #
        # returns True iff needed is found with word boundaries, case-insensitive
        # _contains("java", "javascript") == False
        # _contains("java", "Java is a general purpose programming language") == True
        #
        return re.search(r"(?i)(\b|^)%s(\b|$)" % (needle.replace(' ', '(\s+)')), haystack) is not None

    def summarize(self, entity, paragraphs):
        #
        # base class will find [sentences] that contains the entity
        # for class-specific usage.
        #
        #
        self.relevant_paragraphs = []
        self.relevant_sentences = []
        for p in paragraphs:
            if self._contains(entity, unicode(p)):
                b = TextBlob(p)
                self.relevant_paragraphs.append(b)
                for s in b.sentences:
                    if len(s.words) > 3 and self._contains(entity, unicode(s)):
                        self.relevant_sentences.append(s)

class MaxFrequencyParagraphSummarizer(BaseSummarizer):
    #
    # return a summary limited to the first 2 sentences for whatever
    # paragraph in the document contains the most occurences of the entity
    #
    def summarize(self, entity, paragraphs):
        super(MaxFrequencyParagraphSummarizer, self).summarize(entity, paragraphs)

        haystack = [] # keep a count of paragraph to entity frequency
        for p in self.relevant_paragraphs:
            haystack.append( ([x for x in p.sentences if self._contains(entity, unicode(x))], unicode(p.lower()).count(entity.lower())) )

        if haystack:
            summary_paragraph = sorted(haystack, key=lambda x: x[1], reverse=True)[0][0]
            summary = u' '.join([unicode(x) for x in summary_paragraph[:2]])
            logging.debug('MaxFrequencyParagraph::summarize::entity(%s), summary = [%s]' % (entity, summary))
            return summary

class EarliestSentenceSummarizer(BaseSummarizer):
    #
    # simple text summarizer by simply returning the first sentence
    # containing the given entity
    #
    def summarize(self, entity, paragraphs):
        super(EarliestSentenceSummarizer, self).summarize(entity, paragraphs)

        if self.relevant_sentences:
            earliest = self.relevant_sentences[0]
            logging.debug('EarliestSentenceSummarizer::summarize::entity(%s), summary = [%s]' % (entity, earliest))
            return earliest

class LongestSentenceSummarizer(BaseSummarizer):
    #
    # simple text summarizer by simply returning the longest sentence
    # containing the given entity
    #
    def summarize(self, entity, paragraphs):
        super(LongestSentenceSummarizer, self).summarize(entity, paragraphs)

        if self.relevant_sentences:
            longest = max(self.relevant_sentences, key=len)
            logging.debug('LongestSentenceSummarizer::summarize::entity(%s), summary = [%s]' % (entity, longest))
            return longest
