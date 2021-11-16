import requests
import re
from bs4 import BeautifulSoup

URL = "http://www.rsdb.org/race/blacks" #change code to accept race as a command line argument
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

slurs = []
table = soup.find("table")

rows=table.find_all("tr")   # here you have to use find_all for finding all rows of table

for tr in rows:
    cols = tr.find_all('td') #here also you have to use find_all for finding all columns of current row
    if cols==[]: # This is a sanity check if columns are empty it will jump to next row
        continue
    slur = cols[0].text.strip()
    category = cols[1].text.strip()
    slurs.append((slur, category))
    
    #print(slur)
    #print(category)
    print(slurs)

#write to file here