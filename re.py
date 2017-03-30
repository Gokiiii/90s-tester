import re
from bs4 import BeautifulSoup
html_cont = "<a target=_blank href='/view/2974.htm'></a><a target=_blank href='/view/592974.htm'></a>"
soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
links = soup.find_all('a', href=re.compile(r"/view/\d+\.htm"))
print(links)
for link in links:
    print(link['href'])
    print(link['target'])
