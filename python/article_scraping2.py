import bs4, requests
import summary

output = open('output.txt', 'a')

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

content_dict = {}

for link in link_list[0:1]:
    site = requests.get(link, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'})
    site_html = bs4.BeautifulSoup(site.text, 'html.parser')
    site_parsed = site_html.select('p')
    # site_parsed=site_parsed.prettify()
    content_dict[link] = site_parsed
    
# print(content_dict)
output.write(str(content_dict))