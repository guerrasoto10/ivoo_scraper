import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://ivoo.com/'
XPATH_LINK_TO_PRODUCT= '//h2[@class="woocommerce-loop-product__title"]/text()'
XPATH_PRICES = '//span[@class=woocommerce-Price-amount amount]/text()'
XPATH_DETAILS = '//div[@class=woocommerce-product-details__short-description]/text()'

def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_product = parsed.xpath(XPATH_LINK_TO_PRODUCT)
            print(links_to_product)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == "__main__":
    run()