from bs4 import BeautifulSoup
import re
import time
import requests

from random import randint

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

data = []
for i in range(1, 22):
    link = "https://tiki.vn/o-to-xe-may-xe-dap/c8594?src=c.8594.hamburger_menu_fly_out_banner&page=" + str(i)
    response = requests.get(link, headers=headers)
    time.sleep(randint(2,10))
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    if len(soup.find_all('div', {"class":"product-item"})) == 0:
        print(soup.find('div', {"class":"product-item"}))
        print(link)
        print('Request Denied or end of the list')
    FREESHIP_IMG = "https://salt.tikicdn.com/ts/upload/f3/74/46/f4c52053d220e94a047410420eaf9faf.png"
    TIKINOW_IMG = "https://salt.tikicdn.com/ts/upload/9f/32/dd/8a8d39d4453399569dfb3e80fe01de75.png"
    SHOCKING_IMG = "https://salt.tikicdn.com/ts/upload/75/34/d2/4a9a0958a782da8930cdad8f08afff37.png"
    for index, product in enumerate(soup.find_all('div', {"class":"product-item"})):
        d = {}
        print(f"Product {index}")
        print(f"Page: {i}")

        #Seller ID
        d['Seller ID'] = product["data-id"]
        print("Seller ID:", d['Seller ID'])

        #Product ID
        d['Product ID'] = product["product-sku"]
        print("Product ID:", d['Product ID'])

        #Product price
        d['Product Price'] = product["data-price"]
        print("Product price:", d['Product Price'])

        #Product title
        d['Product Titlte'] = product["data-title"]
        print("Product title:", d['Product Titlte'])

        #Product image
        d['Product Image'] = product.find('img', {"class": "product-image"})["src"]
        print("Product image:", d['Product Image'])

        #Product link
        d['Product Link'] = "https://tiki.vn/"+re.findall(r'^.*\.html', product.find('a')["href"])[0]
        print("Product link:", d['Product Link'])

        #Tikinow available
        service_badge = product.find('div', {'class': 'badge-service'})
        d['TikiNow'] = bool(service_badge) and service_badge.img["src"] == TIKINOW_IMG
        print("TikiNow:", d['TikiNow'])

        #Freeship available
        badge_top= product.find('div', {'class': 'badge-top'})
        d['Freeship'] = bool(badge_top) and badge_top.img["src"] == FREESHIP_IMG
        print("Freeship available:", d['Freeship'])

        #Shocking price
        badge_top = product.find('div', {'class': 'badge-top'})
        d['Shocking Price'] = bool(badge_top) and badge_top.img["src"] == SHOCKING_IMG
        print("Shocking price:", d['Shocking Price'])

        #Reviews
        has_reviews = bool(product.find('div', {'class': 'review-wrap'}))
        d['Reviews'] = re.findall(r'\d+', product.find('p', {'class': 'review'}).text)[0] if has_reviews else 0
        print("# of reviews:", d['Reviews'])

        #Rating average
        #average = product.find('span', {'class': 'rating-content'}).span["style"] if has_reviews else 0
        #print("Average score:", 0.05*int(re.findall(r'\d+', average)[0]))

        #Underpricing
        d['Underpricing'] = bool(product.find('div', {'class': 'badge-under_price'}))
        print("Under price:", d['Underpricing'])

        #Discount
        #discount = product.find('span', {'class': 'sale-tag'})
        #print("Discount:", discount.text if discount else "None")

        #Paid by installments
        d['Installments Allowed'] = bool(product.find('div',{'class':'installment-wrapper'}))
        print("Paid by installments:", d['Installments Allowed'])

        #Freegifts
        d['Freegifts'] = bool(product.find('div',{'class':'freegift-list'}))
        print("Freegift:", d['Freegifts'])
        
        #Additional info
        d['Additional Info'] = product.find('div', {'class': 'ship-label-wrapper'}).text.strip()
        print('Additional info:', d['Additional Info'])
        data.append(d)

import pandas as pd
articles = pd.DataFrame(data)
print(articles)
articles.to_csv("./result.csv", index=False)