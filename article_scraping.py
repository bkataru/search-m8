import bs4
from urllib.request import Request, urlopen


search = input("Enter keyword/sentence to search: ")
# search = "Lorem Ipsum Dolor Sir Amen"
search_split = re.split(" ", search)
google_search_query = "+".join(search_split)

# req = Request(f'https://www.google.com/search?q={google_search_format}', headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'})

# headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
res=requests.get(google_search_query, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'})
search_htmll=bs4.BeautifulSoup(res.text,'html.parser')
search_links=search_html.select('div.r a')

res=Request.get(address,headers=headers)
soup=bs4.BeautifulSoup(res.text,'html.parser')
links=soup.eSselect('div.r a')

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

print(link_list)

