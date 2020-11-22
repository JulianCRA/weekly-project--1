from bs4 import BeautifulSoup
import re
import requests
import time
import random
import json

FREESHIP_IMG = "https://salt.tikicdn.com/ts/upload/f3/74/46/f4c52053d220e94a047410420eaf9faf.png"
TIKINOW_IMG = "https://salt.tikicdn.com/ts/upload/9f/32/dd/8a8d39d4453399569dfb3e80fe01de75.png"
SHOCKING_IMG = "https://salt.tikicdn.com/ts/upload/75/34/d2/4a9a0958a782da8930cdad8f08afff37.png"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
CATEGORY_LINK = "https://tiki.vn/o-to-xe-may-xe-dap/c8594?src=c.8594.hamburger_menu_fly_out_banner"

page = 1
products = []

while True:
    fails = 0
    wait_period = random.randint(10, 40)/10
    print(f'Waiting to fetch page {page} - {wait_period} seconds...')
    time.sleep( wait_period )
    link = f"{CATEGORY_LINK}&page={page}"

    response = requests.get(link, headers=HEADERS)
    html = response.text

    soup = BeautifulSoup(html, features="html.parser")

    products_json = []

    for item in soup.findAll('script', attrs={'type': "application/ld+json"}):
        item_dict = json.loads(item.text)
        if(item_dict["@type"] == "Product"):
            products_json.append(item_dict)

    if not soup.find('div', class_='panel-info'):
        fails += 1
        print(f'Request Denied or end of the list ({fails}/5)')
        
        if fails == 5: break
        continue

    product_list = soup.find_all('div', {"class":"product-item"})
    is_div = True
    if len(product_list) == 0:
        product_list = soup.find_all('a', {"class":"product-item"})
        is_div = False
        if len(product_list) == 0:
            print('No Products')
            break

    for index, product in enumerate(product_list):
        print(" "*50)
        print("="*50)
        print(f"Page {page} - Product {index}")
        print("="*50)
        
        #Seller ID
        print("Seller ID:", product["data-id"] if is_div else "Not available at the moment")
        
        #Product ID
        print("Product ID:", products_json[index]["sku"])

        #Product price
        print("Product price:", products_json[index]["offers"]["price"] )

        #Product title
        print("Product title:", products_json[index]["name"] )

        #Product image
        print("Product image:", products_json[index]["image"])

        #Product link
        product_link = "https://tiki.vn"+re.findall(r'^.*\.html', products_json[index]["url"])[0]
        print("Product link:", product_link)

        #Tikinow available
        service_badge = product.find('div', {'class': 'badge-service'})
        if service_badge:
            img = service_badge.find('img')
        print("TikiNow:", img["src"]==TIKINOW_IMG if img else False)
        

        #Freeship available
        badge_top = product.find('div', {'class': 'badge-top'})
        if badge_top:
            img = badge_top.find('img')
        print("Freeship available:", img["src"]==FREESHIP_IMG if img else False)

        #Shocking price
        badge_top = product.find('div', {'class': 'badge-top'})
        if badge_top:
            img = badge_top.find('img')
        print("Shocking price:", img["src"]==SHOCKING_IMG if img else False)

        # #Reviews
        print("# of reviews:", products_json[index]["aggregateRating"]["reviewCount"] if "aggregateRating" in products_json[index] else 0)

        # #Rating average
        print("Average score:", products_json[index]["aggregateRating"]["ratingValue"] if "aggregateRating" in products_json[index] else 0)

        #Underpricing
        is_under_price = bool(product.find('div', {'class': 'badge-under_price'}))
        print("Under price:", is_under_price)

        #Discount
        if is_div:
            discount = product.find('span', {'class': 'sale-tag'})
        else:
            discount = product.find('div', {'class': 'price-discount__discount'})
        print("Discount:", discount.text if discount else "0%")

        #Paid by installments
        if is_div:
            is_paid_by_installments = bool( product.find('div', {'class': 'installment-wrapper'}) )
        else:
            is_paid_by_installments = bool( product.find('div', {'class': 'badge-benefits'}) )
        print("Paid by installments:", is_paid_by_installments)

        #Freegifts
        is_freegift = bool(product.find('div',{'class':'freegift-list'}))
        print("Freegift:",is_freegift)

        
        #Additional info
        if is_div:
            info = product.find('div', {'class': 'ship-label-wrapper'}).text.strip()
        else:
            info = product.find('div', {'class': 'badge-additional-info'}).text.strip()
        print('Additional info:', info)

    page += 1

print("Pages:", page)
print("Products:", len(products))
