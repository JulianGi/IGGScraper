from selenium import webdriver
from time import sleep
from os import system
import re

sources = ["0", "Mega.co.nz", "Openload.co","KumpulBagi", "UpFile","FileCDN","Go4Up (Multi Links)","Uploaded","Uptobox","Google Drive"] #Download Sources
Openlinks = [] #Links to IGGs on site link generator 
FinalList = [] #Links to the final file downloads



game = input("Link to game: ")#get game to scrape links for
if "://igg-games.com" not in game:
    print("Please enter a valid http://igg-games.com or  https://igg-games.com link!") #input validation
    exit()


for i in range(1, len(sources)):#display sources to choose from
    print(str(i) + ") " + sources[i])
    

source = int(input("Please select your download source: ")) #Get user choice


def GotCookie(cookie):#if cookie exists return true
    for cookies in driver.get_cookies():
        if cookies["name"] == cookie:
            return True
    return False

print("Loading Webdriver...")

options = webdriver.ChromeOptions()
options.add_argument("headless")#setting browser to start headless(without GUI)

driver=webdriver.Chrome("C:\\SeleniumDrivers\\chromedriver.exe", chrome_options=options) #loading chrome

print("Loading Website...")
driver.get(game)    #opening website

for element in driver.find_elements_by_tag_name("p"):#hrefs to all parts of one source are contained in a single paragraph #loop to find the right one
    if sources[source] in element.text: #Check if current iteration is the right one
        for links in element.find_elements_by_tag_name("a"): #loop through all <a tags cuz they contain the hrefs
            Openlinks.append(links.get_attribute("href")) #add hrefs that lead to the linkgenerator to list that we will loop through later
       
        
        driver.get(Openlinks[0])  #open first link to get the cf_clearance cookie that is needed to get the correct html source
        print("Grabbing required cookies...")
        while not GotCookie("__cfduid"):
            sleep(0.1)

        
        system("cls")#clear screen

        print("----------------------------------------------------------------------")
        for x in Openlinks:#loop through the list we created earlier
            driver.get(x) #open websites
            string = driver.find_element_by_tag_name("a").get_attribute("href")#only a single <a tag in the linkgen source so no need for using find_elements
            if "xurl=s:" in string:#string will be smth like: http://bluemediafiles.com/creatinglinks8qJG9LfyFidlaldiwli1kTUSkSn82FylsejFCipVsahU2r2FXfgX2LgYHme3?xurl=s://mega.nz/%23!BSoEFIbD!RX9dgGV0mVC9dlLf2swp7gI90kcfvbXVJ2cUqkS6mcU
                string = string[string.find("xurl=s:") + 8 :]#only display the final part of a string depending on whether it contains xurl=s: or xurl=: 
            else:
                string = string[string.find("xurl=:") + 7 :]
            string = re.sub('%23', '#', string)#change %23 in megalinks to #
            string = "http://" + string

            if source == 2:#get direct download links for openload 
                driver.get(string)
                string = driver.execute_script("""if($('#streamurl').html().length){ 
    return 'https://openload.co/stream/'+$('#streamurl').html();
}""")
            print(string)#add http::// to the beginning of each string so downloadmanagers recognize the string as a link

        print("----------------------------------------------------------------------")           
        break;    #stop the loop since we got the links that we wanted
        
        
driver.quit() #quit driver


