import sys 
import requests  #to download
import bs4  #to extract data
import csv

### When running, add a wikipedia page to start on (otherwise, will start at wikipedia home page)
### For example: SpaceX
### sys.argv (below) takes in this wikipedia page to start from

res = requests.get('https://en.wikipedia.org/wiki/' + ' '.join(sys.argv[1:])) # when running, user adds page name eg. SpaceX
res.raise_for_status() # to check for errors

wiki = bs4.BeautifulSoup(res.text, "html.parser")   #res.text is text from page, html.parser will help structure text into html format

spaceXheading = ""
for i in wiki.select('h1'):
    spaceXheading += i.getText()

spaceXbody = ""
for i in wiki.select('p'):
    spaceXbody += i.getText()
    #print(i.getText())

#print(spaceXheading)
#print(spaceXbody)

pagesToVisit = []

count = 0
repElemList = wiki.find_all('a')
for repElem in repElemList:
    repElemHref = repElem.get('href')
    if repElemHref:
        if 'cite' in repElemHref:
            pass
        elif repElemHref[:1] == "#":
            pass
        elif repElemHref[-12:] == '/wiki/SpaceX':
            pass
        elif repElemHref[-4:] == '.pdf':
            pass
        elif 'youtube' in repElemHref:
            pass
        else:
            if repElemHref[:1] == '/':
                repElemHref = 'https://en.wikipedia.org' + repElemHref
            if repElemHref not in pagesToVisit:
                pagesToVisit.append(repElemHref)
                #print(repElemHref)
                #print(" ")
                count += 1
print("Count: " + str(count))
for p in pagesToVisit:
    print(p)
print(str(len(pagesToVisit)))

with open('spaceX.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([spaceXheading, spaceXbody])
    for page in pagesToVisit:
        try:
            r = requests.get(page)
            print(page)
        except:
            print("Error")
            print(type(r.raise_for_status()))
            pass
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        body = ""
        for i in soup.select('p'):
            body += i.getText()
        heading = ""
        for i in soup.select('h1'):
            heading += i.getText()
            writer.writerow([heading, body])
