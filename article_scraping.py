import bs4
from urllib.request import Request, urlopen
import regex as re

# search = input("Enter keyword/sentence to search: ")
search = "Lorem Ipsum Dolor Sir Amen"
search_split = re.split(" ", search)
google_search_format = "+".join(search_split)

req = Request(f'https://www.google.com/search?q={google_search_format}', headers={'User-Agent':'Mozilla/5.0'})
page = urlopen(req).read()

google_page = bs4.BeautifulSoup(page, 'lxml')
google_page_neat = google_page.prettify()

# print(google_page_neat)

id_with_links = google_page.find_all(id="KcrYT")
# for x in id_with_links:
#     print(x)
print(id_with_links)