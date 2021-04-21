# credit tingtingths https://greasyfork.org/en/scripts/423435-igg-games-bluemediafiles-bypass/code
# Decryption process of the Goroi_n_Create_Button token
def _bluemediafiles_decodeKey(encoded):
    key = ''
    i = int(len(encoded) / 2 - 5)
    while i >= 0:
        key += encoded[i]
        i = i - 2
    i = int(len(encoded) / 2 + 4)
    while i < len(encoded):
        key += encoded[i]
        i = i + 2
    return key


def main():
    try:
        from bs4 import BeautifulSoup
        import urllib.request
        import re
        import pyperclip
    except ImportError:
        print("Some modules are not installed. Run \n python -m pip install -r requirements.txt")
        exit()

    url_choice = input("IGG-Games Link: ")
    if not (url_choice.startswith("http://") or url_choice.startswith("https://")):
        url_choice = "http://" + url_choice
    req = urllib.request.Request(
        url_choice,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    try:
        request = urllib.request.urlopen(req)
    except urllib.error.URLError:
        print("URL could not be opened.")
        exit()

    soup = BeautifulSoup(request, "lxml")
    source_list = []

    # Iterate through all sources
    for source in soup.find_all("b"):
        source_list += re.findall(r"Link [0-9]*[a-zA-Z]+\.* *[0-9]*[a-zA-Z]+\.*[a-zA-Z]*", str(source))
        # Remove torrent link if available
        if str(source).__contains__("TORRENT"):
            source_list.pop(0)

    # Remove 'Link' text from source_list
    for count in range(len(source_list)):
        item = source_list[count]
        source_list[count] = item[5:]

    if not source_list:
        print("No Link sources found.")
        exit()
    for counter, value in enumerate(source_list):
        print(str(counter + 1) + ") " + value)
    source_choice = input("Choose download source: ")
    while not isinstance(source_choice, int):
        try:
            source_choice = int(source_choice)
            if source_choice > len(source_list):
                raise ValueError
        except ValueError:
            source_choice = input(
                "Please enter a number between 1 and " + str(len(source_list)) + ": ")

    finalOutput = ""
    for paragraph in soup.find_all("p"):
        if source_list[source_choice - 1] in paragraph.text:
            print("\n")
            for hyperlink in paragraph("a"):
                string = hyperlink.get('href')
                # Check if button is already redirecting to direct link
                if "http://bluemediafiles.com" not in string:
                    sec_req = urllib.request.Request(
                        string,
                        data=None,
                        headers={
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                        }
                    )
                    try:
                        request = urllib.request.urlopen(sec_req)
                    except urllib.error.URLError:
                        print("URL could not be opened.")
                        exit()
                    print(request.geturl())
                    finalOutput += request.geturl() + "\n"
                else:
                    sec_req = urllib.request.Request(
                        string,
                        data=None,
                        headers={
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                        }
                    )
                    try:
                        request = urllib.request.urlopen(sec_req)
                    except urllib.error.URLError:
                        print("URL could not be opened.")
                        exit()

                    soup = BeautifulSoup(request, "lxml")

                    for script in soup.find_all("script"):
                        matches = re.findall(
                            r"Goroi_n_Create_Button\(\"(.*?)\"\)", str(script))
                        if len(matches) > 0:
                            string = 'https://bluemediafiles.com/get-url.php?url=' + _bluemediafiles_decodeKey(matches[0])
                            third_req = urllib.request.Request(
                                string,
                                data=None,
                                headers={
                                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                                }
                            )
                            try:
                                request = urllib.request.urlopen(third_req)
                            except urllib.error.URLError:
                                print("URL could not be opened.")
                                exit()
                            result_url = request.geturl()
                            if("mega.nz" in result_url):
                                result_url = result_url.replace("%23", "#")
                            print(result_url)
                            finalOutput += request.geturl() + "\n"

            print("\n")
            if input("Copy to Clipboard? y/n ").lower() == "y":
                pyperclip.copy(finalOutput)


main()
