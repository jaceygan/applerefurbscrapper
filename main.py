from bs4 import BeautifulSoup
import requests

mainurl = "https://www.apple.com/sg/shop/refurbished/mac/macbook-air"
urlprefix = "https://www.apple.com"
response = requests.get(mainurl).text

soup = BeautifulSoup(response, 'lxml')
products = soup.find_all('h3')

for product in products:
    if product.find('a'):
        print(product.text.replace('Refurbished', '').strip()+':')
        print(urlprefix+product.find('a')['href'])


