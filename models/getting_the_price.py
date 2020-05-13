import requests
from bs4 import BeautifulSoup
import re

header = {
    'User-Agent': 'Monzilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

#<span class="_35KyD6">IFB 6 kg 2D Wash Fully Automatic Front Load with In-built Heater White&nbsp;&nbsp;(Diva Aqua VX)</span>
def flipkart(flipkart_url):
    tag_name="div"
    query= {"class":"_1vC4OE _3qQ9m1"}
    response = requests.get(flipkart_url, headers=header)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    pricestr = soup.find(tag_name, query).text.strip()
    productName = soup.find("span", {"class":"_35KyD6"}).text
    price = float(pricestr[1:].replace(",", ""))
    return price, productName


def amazon(amazon_url):
    tag_name = "span"
    query = {"class": "a-size-medium a-color-price priceBlockBuyingPriceString", "id": "priceblock_ourprice"}
    response = requests.get(amazon_url, headers=header)
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    price = float(soup.find_all(tag_name, query)[0].text[2:].replace(",", ""))
    productName = soup.find("title").text.split(":")[0]
    return price, productName

def myntra(myntra_url):
    tag_name= "script"
    query = {"type": "application/ld+json"}
    response = requests.get(myntra_url, headers=header)
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    pricestr = str(soup.find_all(tag_name, query)[1])
    productName = soup.find("title").text.split("-")[0][4:].strip()
    price = float(re.compile("\"price\" : \"\d+\"").findall(pricestr)[0][10:].replace("\"", ""))
    return price, productName


def ajio(ajio_url):
    tag_name = "meta"
    query = {"name": "description"}
    response = requests.get(ajio_url, headers=header)
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    pricestr = str(soup.find_all(tag_name, query)[0])
    productName = soup.find("title").text.split("|")[0][4:].strip()
    price = float(re.compile("Rs. \d*,?\d*,?\d+").findall(pricestr)[0][4:].replace(",", ""))
    return price, productName


def get_price_name(url):
    if re.search("flipkart", url):
        price, name = flipkart(url)
    elif re.search("amazon", url):
        price, name = amazon(url)
    elif re.search("myntra", url):
        price, name = myntra(url)
    elif re.search("ajio", url):
        price, name = ajio(url)
    return price, name


