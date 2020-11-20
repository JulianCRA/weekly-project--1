from bs4 import BeautifulSoup
import re
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

html = requests.get("https://tiki.vn/o-to-xe-may-xe-dap/c8594?src=c.8594.hamburger_menu_fly_out_banner&page=6", headers=headers).text

soup = BeautifulSoup(html, features="html.parser")

for product in soup.find_all('div', {"class":"product-item"}):
    print("-"*50)
    print("Seller ID:", product["data-id"])
    print("Product ID:", product["product-sku"])
    print("Product price:", product["data-price"])
    print("Product title:", product["data-title"])
    product_image = product.find('img', {"class": "product-image"})["src"]
    print("Product image:", product_image)
    product_link = product.find('a')["href"]
    print("Product link:", product_link)
    is_tiki_now = bool(product.find('div', {'class': 'badge-service'}))
    print("TikiNow:", is_tiki_now)
    is_freeship = bool(product.find('div', {'class': 'badge-top'}))
    print("Free shipping:", is_freeship)
    reviews = re.findall(r'\d+', product.find('p', {'class': 'review'}).text)[0]
    print("# of reviews:", reviews)
    is_under_price = bool(product.find('div', {'class': 'badge-under_price'}))
    print("Under price:", is_under_price)
    discount = product.find('span', {'class': 'sale-tag'})
    print("Discount:", discount.text if discount else "None")