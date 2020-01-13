from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_search import YoutubeSearch

from gensim.summarization import keywords

import json


LANGUAGE = "english"


def videoFunction(search, video_sentence_count, no_video):
    results = YoutubeSearch(search, max_results=no_video).to_json()
    results = json.loads(results)
    filtered_results = []
    for result in results['videos']:
        v = result['id']
        transcript_flag = True
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(v)
        except:
            print("no transcripts")
            transcript_flag = False

        if transcript_flag:
            try:
                transcript = transcript_list.find_manually_created_transcript(['en', 'en-UK', 'en-US'])
            except:
                print("no transcript")
                transcript_flag = False

        if transcript_flag:
            transcript_proto = transcript.fetch()
            final_transcript = ''
            for obj in transcript_proto:
                final_transcript += obj['text'] + ' '

            key_words = keywords(final_transcript, ratio=0.1)

            parser = PlaintextParser.from_string(final_transcript, Tokenizer("english"))
            stemmer = Stemmer(LANGUAGE)

            summarizer = Summarizer(stemmer)
            summarizer.stop_words = get_stop_words(LANGUAGE)

            summary = ''
            for sentence in summarizer(parser.document, video_sentence_count):
                summary += str(sentence)

            result['summary'] = summary
            result['id'] = result['id'].split('&')[0]
            result['keywords'] = key_words
            filtered_results.append(result)

    return filtered_results