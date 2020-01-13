from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import bs4, requests
import regex as reG

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


import bs4, requests
import regex as reG

from gensim.summarization import keywords

import json

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}

LANGUAGE = "english"


def textFunction(search, text_sentence_count, no_article):
    address = 'http://www.google.com/search?q=' + search + '&num=' + str(no_article)
    res = requests.get(address, headers=headers)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    links = soup.select('div.r a')

    link_list = []  # Empty list to display only the top 5 links

    # Clean the soup by filtering only the information requested
    for link in links:
        if "webcache.googleusercontent.com" in link.attrs["href"]:
            pass
        elif "#" in link.attrs["href"]:
            pass
        elif "/search?q=related:" in link.attrs["href"]:
            pass
        else:
            link_res = requests.get(link.attrs["href"], headers=headers)
            link_soup = bs4.BeautifulSoup(link_res.text, 'html.parser')
            link_title = link_soup.title.text
            link_list.append({
                # 'title': link.title,
                'title': link_title,
                'href': link.attrs["href"]
            })

    content_dict = {}

    for link in link_list:
        LANGUAGE = "english"
        SENTENCES_COUNT = 10

        parser = HtmlParser.from_url(link['href'], Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)

        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)

        finalText = ''
        for sentence in summarizer(parser.document, text_sentence_count):
            finalText += str(sentence)

        key_words = keywords(finalText, ratio=0.1)
        content_dict[link['href']] = {
            'title': link['title'],
            'summary': finalText,
            'keywords': key_words
        }

    return content_dict




