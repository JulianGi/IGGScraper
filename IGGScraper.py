from bs4 import BeautifulSoup
import urllib.request
import re


urlChoice = input("IGG-Games Link:")
if not (urlChoice.startswith("http://") or urlChoice.startswith("https://")):
    urlChoice = "http://" + urlChoice
    
req = urllib.request.Request(
    urlChoice, 
    data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
)

possibelSources = ["MegaUp.net","Rapidgator","Mega.co.nz", "Openload.co","KumpulBagi", "UpFile","FileCDN","Go4Up (Multi Links)","Uploaded","Uptobox","Google Drive"] #Download Sources
existingSources = []

try:
    r = urllib.request.urlopen(req)
except:
    print("Url could not be opend.")
    exit()

soup = BeautifulSoup(r, "lxml")

for x in soup.find_all("p"):
    for y in possibelSources:
        if "Link " + y in x.text:
            existingSources.append(y)

if not existingSources:
    print("No Link sources found.")
    exit()

for i in range(0, len(existingSources)):
    print(str(i + 1) + ") " + existingSources[i])
    


sourceChoice = input("Choose download source: ")
while type(sourceChoice) != int:
    try:
        sourceChoice = int(sourceChoice)
        if sourceChoice > len(existingSources):
            raise ValueError
    except:
        sourceChoice = input("Please enter a number between 1 and "+str(len(existingSources))+ ": ")
    


for x in soup.find_all("p"):
    if existingSources[sourceChoice - 1] in x.text:
        print("\n")
        for a in x("a"):
            string = a.get('href')
            string = re.sub('%23', '#', string)
            print("http"+string[string.rfind("://"):])
        print()
        break
