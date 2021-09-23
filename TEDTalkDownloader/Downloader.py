import requests #Getting content of the TED Talk Page
from bs4 import BeautifulSoup #Web Scraping
import re #Regular Expression pattern matching
import sys #For Argument Parsing, ie; code generalization

#### Exception Handling
# To handle arguments passed via Command Line Interface and process if they are legitemate URLs

if len(sys.argv) >1:
    url = sys.argv[1]
else:
    sys.exit("Error: Please enter the TED Talk URL")
    
### Committing HTTP Request for TED Talk Page
r = requests.get(url) # Response of the get request stored in "r"
print("Download about to start")

### Extracting video URL using RegEx
soup = BeautifulSoup(r.content, features="lxml")
# Identify location of video content on the page
# Video located inside "talkPage.init" in the script-tag

for val in soup.findAll("script"):
    if(re.search("talkPage.init", str(val))) is not None:
        result = str(val)
result_mp4 = re.search("(?P<url>https?://[^\s]+)(mp4)", result).group("url")
mp4_url = result_mp4.split('"')[0]
print("Downloading video from " + mp4_url)
# Dynamically generating filename from URL Title
file_name = mp4_url.split("/")[len(mp4_url.split("/"))-1].split('?')[0]
print("Storing video in ..." + file_name) 

### Storing video locally

r = requests.get(mp4_url)

with open(file_name, 'wb') as f:
    f.write(r.content)
    
print('Download process completed successfully')