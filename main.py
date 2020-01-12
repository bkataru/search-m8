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

import bs4, requests
import regex as reG

from gensim.summarization import keywords

from flask import Flask, render_template, send_file, request
import json

#nostril
#sumy
#youtube transcriber
# youtube-search

# sumy - 4 different algos
# youtube transcriber - different languages

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}

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
            
            parser = PlaintextParser.from_string(final_transcript,Tokenizer("english"))
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

def textFunction(search, text_sentence_count, no_article):
    address='http://www.google.com/search?q='+search + '&num=' + str(no_article)
    res=requests.get(address,headers=headers)
    soup=bs4.BeautifulSoup(res.text,'html.parser')
    links=soup.select('div.r a')
    
    link_list = [] #Empty list to display only the top 5 links

    #Clean the soup by filtering only the information requested
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

app = Flask(__name__)

@app.route('/')
def main():
    return send_file("templates/index.html")
    
    
@app.route('/searchQuery')
def searchQuery():
    if request.method == 'GET':
        query = request.args.get('query')
        video_sentence_count = request.args.get('video_sentence_count')
        text_sentence_count = request.args.get('text_sentence_count')
        no_video = int(request.args.get('no_video'))
        no_text = int(request.args.get('no_article'))
        print(no_video, no_text, type(no_video), type(no_text))
        video_data = videoFunction(query, video_sentence_count, no_video)
        text_data = textFunction(query, text_sentence_count, no_text)
        
        return json.dumps({
            'video_data': video_data,
            'text_data': text_data
        });
    
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8080", use_debugger=True)

