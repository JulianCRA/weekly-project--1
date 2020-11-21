from bs4 import BeautifulSoup
import re
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
# link = "https://tiki.vn/dien-gia-dung/c1882?src=c.1882.hamburger_menu_fly_out_banner&page=5"
link = "https://tiki.vn/o-to-xe-may-xe-dap/c8594?src=c.8594.hamburger_menu_fly_out_banner&page=2"
# link = "https://tiki.vn/search?q=c310%20sony"
response = requests.get(link, headers=headers)
html = response.text

soup = BeautifulSoup(html, features="html.parser")

if len(soup.find_all('div', {"class":"product-item"})) == 0:
    print('Request Denied or end of the list')

for index, product in enumerate(soup.find_all('div', {"class":"product-item"})):
    print(" "*50)
    print("="*50)
    print(f"Product {index}")
    print("="*50)
    
    #Seller ID
    # print("Seller ID:", product["data-id"])

    # #Product ID
    # print("Product ID:", product["product-sku"])

    # #Product price
    # print("Product price:", product["data-price"])

    # #Product title
    # print("Product title:", product["data-title"])

    # #Product image
    # product_image = product.find('img', {"class": "product-image"})["src"]
    # print("Product image:", product_image)

    # #Product link
    # product_link = "https://tiki.vn/"+re.findall(r'^.*\.html', product.find('a')["href"])[0]
    # print("Product link:", product_link)

    #Tikinow available
    service_badge = product.find('div', {'class': 'badge-service'})
    service_badge = service_badge and service_badge.img["src"] == "https://salt.tikicdn.com/ts/upload/9f/32/dd/8a8d39d4453399569dfb3e80fe01de75.png"
    print("TikiNow:", service_badge)

    #Freeship available
    is_freeship = bool(product.find('div', {'class': 'badge-top'}))
    print("Free shipping:", is_freeship)

    #Reviews
    has_reviews = bool(product.find('div', {'class': 'review-wrap'}))
    reviews = re.findall(r'\d+', product.find('p', {'class': 'review'}).text)[0] if has_reviews else 0
    print("# of reviews:", reviews)

    #Rating average
    average = product.find('span', {'class': 'rating-content'}).span["style"] if has_reviews else 0
    print("Average score:", 0.05*int(re.findall(r'\d+', average)[0]))

    #Underpricing
    is_under_price = bool(product.find('div', {'class': 'badge-under_price'}))
    print("Under price:", is_under_price)

    #Discount
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
