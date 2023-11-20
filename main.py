from bs4 import BeautifulSoup
import requests

searchString = 'm2 air 13 starlight'
searchList = searchString.upper().split()


mainurl = "https://www.apple.com/sg/shop/refurbished/mac/macbook-air"
urlprefix = "https://www.apple.com"
response = requests.get(mainurl).text

soup = BeautifulSoup(response, 'lxml')
products = soup.find_all('h3') #this returns some other garbage that is taken care of later

productDict = {}

def searchMatch(sl, p):
    pUp = p.upper()
    for s in sl:
        if s.upper() not in pUp:
            return False
    return True

for product in products:
    if product.find('a'):
        productDict[product.text.replace('Refurbished', '').strip()] = urlprefix+product.find('a')['href']
        #print(product.text.replace('Refurbished', '').strip()+':')
        #print(urlprefix+product.find('a')['href'])
counter = 0
for p in productDict.keys():
    if searchMatch(searchList, p):
        counter +=1
        print(p)
        print(productDict[p])
print (counter, 'items found')



