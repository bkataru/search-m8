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
import json

LANGUAGE = "english"
SENTENCES_COUNT = 5

def videoFunction(search):
    results = YoutubeSearch(search, max_results=50).to_json()
    results = json.loads(results)
    filtered_results = []
    result_count = 0
    for result in results['videos']:
        if result_count > 10:
            break
        
        v = result['id']
        transcript_list = YouTubeTranscriptApi.list_transcripts(v)
        transcript_flag = True
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
                
            parser = PlaintextParser.from_string(final_transcript,Tokenizer("english"))
            stemmer = Stemmer(LANGUAGE)

            summarizer = Summarizer(stemmer)
            summarizer.stop_words = get_stop_words(LANGUAGE)

            summary = ''
            for sentence in summarizer(parser.document, SENTENCES_COUNT):
                summary += str(sentence)

            result['summary'] = summary
            filtered_results.append(result)
            result_count += 1

    return filtered_results


print(videoFunction('minutephysics'))