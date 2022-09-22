import requests
from bs4 import BeautifulSoup
import smtplib
import os

'''include the url to the product'''
url = "https://www.lazada.com.my/products/philips-fully-automatic-espresso-coffee-machines-series-2200-ep2220-ep222010-i1843218230-s7337748360.html?clickTrackInfo=query%253Acoffee%252Bmachine%253Bnid%253A1843218230%253Bsrc%253ALazadaMainSrp%253Brn%253A4c1ed4a22c585032c498e48e302af4f0%253Bregion%253Amy%253Bsku%253A1843218230_MY%253Bprice%253A1849%253Bclient%253Adesktop%253Bsupplier_id%253A1000125690%253Basc_category_id%253A10000288%253Bitem_id%253A1843218230%253Bsku_id%253A7337748360%253Bshop_id%253A327601&freeshipping=0&fs_ab=1&search=1&spm=a2o4k.searchlist.list.i40.749b7b4b7nFJE8"

'''Use request.get to make request to the web page and get its response(status)'''
response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36", "Accept-Language":"en-GB,en-US;q=0.9,en;q=0.8"})
product = response.text

'''Use BeautifulSoup to parse the product price'''
soup = BeautifulSoup(product, "lxml")
product_price_tags = soup.select("#module_product_price_1 div div span")

'''Use os library to set values outside the script/program for security reasons.'''
email_sender = os.environ["SENDER_EMAIL"]
password = os.environ["PASSWORD"]
email_receiver = os.environ["RECEIVER_EMAIL"]

'''Create a function to return the current_price of the product'''
def current_price():
    all_values= [(values.getText().strip("RM").replace(',',"").replace('%',"")) for values in product_price_tags]
    current_price= ([float() for x in all_values])[0]
    return current_price

'''Compare the current price with the desired product price using Class Inheritance and send an email to the receiver to notify on the prices '''
def compare_price(current_price):
    msg = f"Subject: CoffeeMachine Price Alert- Price Dropped! \n\nPurchase it now! Price has dropped below RM 1,800.Go to the page:{url}."
    if current_price() < 1800.00:
        connection = smtplib.SMTP("smtp.gmail.com",port=587)
        connection.starttls()
        connection.login(user=email_sender,password=password)
        connection.sendmail(from_addr=email_sender, to_addrs= email_receiver, msg = msg)
        connection.close()

    else:
        connection = smtplib.SMTP("smtp.gmail.com",port=587)
        connection.starttls()
        connection.login(user=email_sender, password=password)
        connection.sendmail(from_addr=email_sender, to_addrs=email_receiver, msg = "Subject: CoffeeMachine Price Alert- Still above RM 1,800 \n\n Price is still above RM 1,800.")
        connection.close()

compare_price(current_price)





