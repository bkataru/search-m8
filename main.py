from flask import Flask, render_template, send_file, request
import json

from python.video_scraper import videoFunction
from python.article_scraper import textFunction

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
        })
    
    
if __name__ == '__main__':
    app.run(host="127.0.0.1", port="3000", use_debugger=True)

