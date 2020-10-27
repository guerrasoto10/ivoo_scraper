import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://ivoo.com'
XPATH_LINK_TO_PRODUCT = '//div[@class="product-inner"]/a/@href'
XPATH_PRODUCT_NAME = '//div[@class="single-product-wrapper"]/div[@class="summary entry-summary"]/div[@class="single-product-header"]/h1[@class="product_title entry-title"]/text()'
XPATH_PRICE_PROMOTION = '//div[@class="product-actions"]/p[@class="price"]/ins/span[@class="woocommerce-Price-amount amount"]/text()'
XPATH_PRICE = '//div[@class="product-actions"]/p[@class="price"]/span[@class="woocommerce-Price-amount amount"]/text()'       
XPATH_MERIDA_PRICE ='//div[@class="woocommerce-product-details__short-description"]/h4[@class="precio-oferta-flash"]/span/text()' 
XPATH_DETAILS = '//div[@class=woocommerce-product-details__short-description]/text()'

def parse_product(link, today):
    try:
        response=requests.get(link)
        if response.status_code == 200:
            product = response.content.decode('utf-8')
            parsed = html.fromstring(product)

            try:
                product_name = parsed.xpath(XPATH_PRODUCT_NAME)[0]
                product_name = product_name.replace('/','')
                try:
                    product_price = parsed.xpath(XPATH_PRICE_PROMOTION)[0]
                except:
                    product_price = parsed.xpath(XPATH_PRICE)[0]
            except IndexError:
                return

            with open(f'{today}/{product_name}.txt', 'w' , encoding='utf-8') as f:
                f.write(product_name)
                f.write('\n\n')
                f.write('Precio: ')
                f.write(product_price)
     

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_product = parsed.xpath(XPATH_LINK_TO_PRODUCT)
            #print(links_to_product)
            today = datetime.date.today().strftime('%d-%m-%y')
            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_to_product:
                parse_product(link, today)

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == "__main__":
    run()