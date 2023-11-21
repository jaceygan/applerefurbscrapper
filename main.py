from bs4 import BeautifulSoup
import requests

searchList= 'air 15 starlight m2'.split()

sendEmail = True

mainurl = "https://www.apple.com/sg/shop/refurbished/mac"
urlprefix = "https://www.apple.com"
response = requests.get(mainurl).text

soup = BeautifulSoup(response, 'lxml')
products = soup.find_all('h3') #this returns some other garbage that is taken care of later

def searchMatch(sl, p):
    pUp = p.upper()
    for s in sl:
        if s.upper() not in pUp:
            return False
    return True

count = 0
for product in products:
    if product.find('a'): #conveiently, the other garbage doesnt have a href
        pName = product.text.replace('Refurbished', '').strip()
        if searchMatch(searchList, pName):
            count += 1
            pURL = urlprefix+product.find('a')['href']  
            pDetails = requests.get(pURL).content
            pSoup = BeautifulSoup(pDetails, 'lxml')
            print(str(count)+ '. '+ pName)
            print()

            print("Price:",pSoup.find("div", class_="rf-pdp-currentprice").text)
            print('Info:')
            
            for info in pSoup.find("div", class_="rc-pdsection-mainpanel column large-9 small-12"):
                print(info.text.strip())

            print(pURL)
            print()
            
            print ("=================================================")
            print()


print(count, "items found")
            