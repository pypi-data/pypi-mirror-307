import re
import requests
def upload(filename):
    with open(filename, 'rb') as file:
        response = requests.post('https://bashupload.com/', files={'file': file})
            
        match = re.search(r'wget (https?://[^\s]+)', response.text)
        if match:
            picurl = match.group(1)
            return picurl
        else:
            print("Fehler beim Upload")