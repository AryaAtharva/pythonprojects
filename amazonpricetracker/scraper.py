import requests
from bs4 import BeautifulSoup
import smtplib
import time
def send_mail():
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('YourEmail@gmail.com','yourpassword')

    subject= 'Price went down'
    body  = 'check the link https://www.amazon.in/dp/B07V5PK8NT/ref=fs_a_mn_0'

    msg = f"Subject:{subject}\n\n{body}"

    server.sendmail(
        'sendermail@gmail.com'
        'recieveermail@gmail.com',
        msg
    )

    print('Mail has been sent')

    server.quit()

def check_price():

    URL = 'https://www.amazon.in/dp/B07V5PK8NT/ref=fs_a_mn_0'
    headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    page = requests.get(URL , headers =headers)
    soup = BeautifulSoup(page.content,'html.parser')
    title = soup.find(id="productTitle").get_text()

    price  = soup.find(id="priceblock_ourprice").get_text()
    price1= price[2:8]
    price2 = float(price1.replace(',',''))
    print(price2)
    if(price2< 90000.0):
        send_mail()


while (True):
    check_price()
    time.sleep(60*60)