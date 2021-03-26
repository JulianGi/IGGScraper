# credit tingtingths https://greasyfork.org/en/scripts/423435-igg-games-bluemediafiles-bypass/code
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

    possible_sources = ["MegaUp.net", "Rapidgator", "Mega.co.nz", "Mega.nz", "TusFiles", "KumpulBagi",
                        "UpFile", "FileCDN", "Go4Up (Multi Links)", "Uploaded", "Uptobox",
                        "Google Drive", "1Fichier", "Direct", "ClicknUpload", "AnonFiles"]  # Download Sources
    existing_sources = []

    try:
        request = urllib.request.urlopen(req)
    except urllib.error.URLError:
        print("URL could not be opened.")
        exit()

    soup = BeautifulSoup(request, "lxml")

    for paragraph in soup.find_all("b"):
        for source in possible_sources:
            if "Link " + source in paragraph.text:
                existing_sources.append(source)

    if not existing_sources:
        print("No Link sources found.")
        exit()
    for counter, value in enumerate(existing_sources):
        print(str(counter + 1) + ") " + value)
    source_choice = input("Choose download source: ")
    while not isinstance(source_choice, int):
        try:
            source_choice = int(source_choice)
            if source_choice > len(existing_sources):
                raise ValueError
        except ValueError:
            source_choice = input(
                "Please enter a number between 1 and " + str(len(existing_sources)) + ": ")

    finalOutput = ""
    for paragraph in soup.find_all("p"):
        if existing_sources[source_choice - 1] in paragraph.text:
            print("\n")
            for hyperlink in paragraph("a"):
                string = hyperlink.get('href')
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
                        print(request.geturl())
                        finalOutput += request.geturl() + "\n"

            print("\n")
            if input("Copy to Clipboard? y/n ").lower() == "y":
                pyperclip.copy(finalOutput)

                
main()
