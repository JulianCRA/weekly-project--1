# YOUR CODE
from bs4 import BeautifulSoup
import re
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

html = requests.get("https://tiki.vn/o-to-xe-may-xe-dap/c8594?src=c.8594.hamburger_menu_fly_out_banner&page=2", headers=headers).text
# print(html)
# results = {}

soup = BeautifulSoup(html, features="html.parser")

# print(soup.find_all('div', {"class":"cpy-right-info"}))

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
    discount = product.find('div', {"class": "price-discount"})
    print("Discount:", discount)

# for link in soup.find_all('div', {'class': "ProductList__Wrapper-sc-1dl80l2-0 healEa"}): 
#     print(link)



#   if link.text: 
#       print(link["href"])
    # results[link.text.strip()] = link["href"]

# print(results)
