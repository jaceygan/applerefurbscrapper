from bs4 import BeautifulSoup
import requests
import emailproperties
from email.message import EmailMessage
import ssl
import smtplib

searchstring = 'm2 air 15 starlight'

searchList= searchstring.split()
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
separator = "============================="
emailbody = separator+'\n'
for product in products:
    if product.find('a'): #conveiently, the other garbage doesnt have a href
        pName = product.text.replace('Refurbished', '').strip()
        if searchMatch(searchList, pName):
            count += 1
            pURL = urlprefix+product.find('a')['href']  
            pDetails = requests.get(pURL).content
            pSoup = BeautifulSoup(pDetails, 'lxml')
            emailbody +=(str(count)+ '. '+ pName)
            emailbody += '\n'

            emailbody +="Price:"+ str(pSoup.find("div", class_="rf-pdp-currentprice").text)+'\n'
            emailbody += 'Info:'
            
            for info in pSoup.find("div", class_="rc-pdsection-mainpanel column large-9 small-12"):
                emailbody += '\t'+info.text.strip()+'\n'

            emailbody += pURL
            emailbody += '\n'
            
            emailbody += separator+'\n'
            emailbody += '\n'


emailbody = str(count) + ' items found for '+ searchstring + '\n' + emailbody

em = EmailMessage()
em['From'] = emailproperties.sender
em['To'] = emailproperties.reciepient
em['Subject'] = emailproperties.subject
em.set_content(emailbody)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(emailproperties.sender, emailproperties.password)
    smtp.sendmail(emailproperties.sender, emailproperties.reciepient, em.as_string())
