from selenium import webdriver
import time
import re
from os import system

sources = ["0", "Mega.co.nz", "Openload.co","KumpulBagi", "UpFile","FileCDN","Go4Up (Multi Links)","Uploaded","Uptobox","Google Drive"]

game = input("Link to game: ")

if "http://igg-games.com" not in game:
    print("Please enter a valid http://igg-games.com link!")
    exit()

i = 1
while i < len(sources):
    print(str(i) + ") " + sources[i])
    i+=1

source = int(input("Please select your download source: "))

Openlinks = []
FinalList = []
print("Loading Webdriver...")
driver=webdriver.PhantomJS("C:\\SeleniumDrivers\\phantomjs.exe")
print("Loading Website...")
driver.get(game)    
paragraphs = driver.find_elements_by_tag_name("p")
for element in paragraphs:
    if sources[source] in element.text:
        for links in element.find_elements_by_tag_name("a"):
            Openlinks.append(links.get_attribute("href"))
        
        
        driver.get(Openlinks[0])
        print("Grabbing required cookies...")
        time.sleep(4)
        print("Done")
        time.sleep(1)

        system("cls")

        print("----------------------------------------------------------------------")
        for x in Openlinks:
            driver.get(x)
            string = driver.find_element_by_tag_name("a").get_attribute("href")
            if "xurl=s:" in string:
                string = string[string.find("xurl=s:") + 8 :]
            else:
                string = string[string.find("xurl=:") + 7 :]
            print("http://" + string)

        print("----------------------------------------------------------------------")           
        break;    
        
        
driver.quit()