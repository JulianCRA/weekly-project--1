from bs4 import BeautifulSoup
import re
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

html = requests.get("https://tiki.vn/o-to-xe-may-xe-dap/c8594?src=c.8594.hamburger_menu_fly_out_banner&page=2", headers=headers).text

soup = BeautifulSoup(html, 'html.parser')

for product in soup.find_all('div', {"class":"product-item"}):
    print("-"*50)
    #Seller ID
    print("Seller ID:", product["data-id"])
    #Product ID
    print("Product ID:", product["product-sku"])
    #Product price
    print("Product price:", product["data-price"])
    #Product title
    print("Product title:", product["data-title"])
    #Product image
    product_image = product.find('img', {"class": "product-image"})["src"]
    print("Product image:", product_image)
    #Product link
    product_link = product.find('a')["href"]
    print("Product link:", product_link)
    #Tikinow availabled
    is_tiki_now = bool(product.find('div', {'class': 'badge-service'}))
    print("TikiNow:", is_tiki_now)
    #Freeship availabled
    is_freeship = bool(product.find('div', {'class': 'badge-top'}))
    print("Free shipping:", is_freeship)
    #Numbers of reviews
    reviews = re.findall(r'\d+', product.find('p', {'class': 'review'}).text)[0]
    print("# of reviews:", reviews)
    #Underpricing
    is_under_price = bool(product.find('div', {'class': 'badge-under_price'}))
    print("Under price:", is_under_price)
    #discount = product.find('span', {'class': 'sale-tag'})
    #print("Discount:", discount.text if discount else "None")
    #Paid by installments
    is_paid_by_installments = bool(product.find('div',{'class':'installment-wrapper'}))
    print("Paid by installments:", is_paid_by_installments)
    #Freegifts
    is_freegift = bool(product.find('div',{'class':'freegift-list'}))
    print("Freegift:",is_freegift)
    #Additional info
    is_info = product.find('div', {'class': 'ship-label-wrapper'}).text.strip()
    print('Additional info:', is_info)