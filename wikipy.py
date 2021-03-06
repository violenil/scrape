import sys 
import requests  #to download
import bs4  #to extract data
import csv

### When running, add a wikipedia page to start on (otherwise, will start at wikipedia home page)
### For example: SpaceX
### sys.argv (below) takes in this wikipedia page to start from

def scrapeWiki(page):
    res = requests.get(page)  #retrieves the page
    res.raise_for_status()  #check for errors
    wikiSoup = bs4.BeautifulSoup(res.text, "html.parser") #res.text is text from page, html.parser helps to structure the text into html format
    wikiHeading = ""
    for heading in wikiSoup.select('h1'):
        wikiHeading += heading.getText()

    wikiBody = ""
    for body in wikiSoup.select('p'):
        wikiBody += body.getText()
    return([wikiHeading, wikiBody])

#def scrapeOther(page):


res = requests.get('https://en.wikipedia.org/wiki/' + ' '.join(sys.argv[1:])) # when running, user adds page name eg. SpaceX

def retrieveLinks(page):
    res = requests.get(page)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    wikiToVisit = []
    otherToVisit = []
    repElemList = soup.find_all('a')
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
                if 'wikipedia' in repElemHref:
                    if repElemHref not in wikiToVisit:
                        wikiToVisit.append(repElemHref)
                elif repElemHref not in otherToVisit:
                    otherToVisit.append(repElemHref)
    return([wikiToVisit, otherToVisit])

for p in otherToVisit:
    print(p)
print(str(len(otherToVisit)))


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
