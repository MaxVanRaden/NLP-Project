import requests
import sys
from bs4 import BeautifulSoup

try:
    outFile = sys.argv[1] #first argument after script name must be present
    categories = sys.argv[2:] #second argument after script name must be present
except:
    print("Error. Not enough command line arguments.")
    exit()

slurs = []

print(categories)
for race in categories:
    counter = 0
    if race == '':
        break
    URL = "http://www.rsdb.org/race/" + str(race)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table')
    rows=table.find_all('tr')   # here you have to use find_all for finding all rows of table
    for tr in rows:
        cols = tr.find_all('td') #here also you have to use find_all for finding all columns of current row
        if cols==[]: # This is a sanity check if columns are empty it will jump to next row
            continue
        slur = cols[0].text.strip()
        category = cols[1].text.strip()
        slurs.append((slur, category))
        counter += 1
    print('{}: {} slurs'.format(race, counter))
    #print((slur, category))
        #print(category)
    #print(slurs)

with open(outFile, "a", encoding = 'utf-8') as f_out:
    for slur in slurs:
        f_out.write('({},{}),\n'.format(slur[0], slur[1]))
    f_out.close()

print("{} slurs from the Racial Slur Database written to {}".format(len(slurs), category, outFile))
#add readme for usage

