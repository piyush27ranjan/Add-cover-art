from bs4 import BeautifulSoup
import urllib
import json

def get_soup(url,header):
    return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url,headers=header)),'html.parser')

query = input("Enter the keyword: ")
query= query.split()
query='+'.join(query)
url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
soup = get_soup(url,header)

Images_Links = []

for a in soup.find_all("div",{"class":"rg_meta"}):
	    link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
	    Images_Links.append((link,Type))
        
ActualImages = []

for i in range(len(Images_Links)):
    if Images_Links[i][0].split(".")[-1] in ["png","jpeg","jpg"]:
        ActualImages.append(Images_Links[i][0])
        
for i in range(10):
    try:
        urllib.request.urlretrieve(ActualImages[i],str(i)+"."+ActualImages[i].split(".")[-1])
    except:
        continue