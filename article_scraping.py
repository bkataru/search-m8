import bs4
from urllib.request import Request, urlopen
import regex as re

search = input("Enter keyword/sentence to search: ")
search_split = re.split(" ", search)
google_search_format = "+".join(search_split)

req = Request(f'https://www.google.com/search?q={google_search_format}')
page = urlopen(req).read()

google_page = bs4.BeautifulSoup(page, 'lxml')
google_page.prettify()

print(google_page)

id_with_links = google_page.find_all(id="search")



# output_file = open("output.txt", "w")
# paragraphs = []

# for link in links:
#     scraped_data = urllib.request.urlopen(link)
#     article = scraped_data.read()

#     parsed_article = bs4.BeautifulSoup(article,'lxml')

#     paragraphs = parsed_article.find_all('p')

#     article_text = ""

#     for p in paragraphs:
#         article_text += p.text

#     paragraphs.append(article_text)