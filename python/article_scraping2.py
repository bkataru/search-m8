from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import bs4, requests
import summary
from readability import Document
import regex as reG

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
# search="Subsidies in UK"
search=input("Enter Keywords: ")
address='http://www.google.com/search?q='+search
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
        link_list.append(link.attrs["href"])


# link_list = [x for x in link_list if x not in ]
# final_link_list = []
# for x in link_list:
    # if x not 
    
# print(re.match('https://translate.google.com', '//translate.google.com/translate?hl=ko&sl=en&u=https://www.facebook.com/Nani/&prev=search'))
    
    
content_dict = {}

for link in link_list:
    print(link)
    
    
for link in link_list:
    LANGUAGE = "english"
    SENTENCES_COUNT = 10
    
    parser = HtmlParser.from_url(link, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    
    finalText = ''
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        print(sentence)
        finalText += str(sentence)
    content_dict[link] = finalText

    #print(content_dict)
    
    
#print(content_dict)
#summary.main(content_dict)
    
# print(content_dict)
# output.write(str(content_dict))

    