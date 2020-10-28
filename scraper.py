import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://ivoo.com'
XPATH_LINK_TO_CATEGORY = '//div/a/@href[contains(.,"category")]'
XPATH_LINK_TO_PRODUCT = '//div[@class="product-inner"]/a/@href'
XPATH_PRODUCT_NAME = '//div[@class="single-product-wrapper"]/div[@class="summary entry-summary"]/div[@class="single-product-header"]/h1[@class="product_title entry-title"]/text()'
XPATH_PRICE_PROMOTION = '//div[@class="product-actions"]/p[@class="price"]/ins/span[@class="woocommerce-Price-amount amount"]/text()'
XPATH_PRICE = '//div[@class="product-actions"]/p[@class="price"]/span[@class="woocommerce-Price-amount amount"]/text()'       
XPATH_MERIDA_PRICE ='//div[@class="woocommerce-product-details__short-description"]/h4[@class="precio-oferta-flash"]/span/text()' 
XPATH_DETAILS = '//div[@class="woocommerce-Tabs-panel woocommerce-Tabs-panel--description panel entry-content wc-tab"]/*/text()'

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
                
                try:
                    product_details = parsed.xpath(XPATH_DETAILS)
                except:
                    product_details = 'Producto sin descripcion'
                
                product_price_merida = parsed.xpath(XPATH_MERIDA_PRICE)[0]

            except IndexError:
                return

            with open(f'{today}/{product_name}.txt', 'w' , encoding='utf-8') as f:
                f.write(product_name)
                f.write('\n')
                f.write('Precio: ')
                f.write(product_price)
                f.write('\n')
                f.write(product_price_merida)
                f.write('\n\n')
                for p in product_details:
                    f.write(p)
                    f.write('\n')
     

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
            links_to_category = list(set(parsed.xpath(XPATH_LINK_TO_CATEGORY)))
            #print(links_to_category)
            print(f'Hemos encontrado {len(links_to_category)} categorias')

            today = datetime.date.today().strftime('%d-%m-%y')
            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_to_category:
                try:
                    new_response = requests.get(link)
                    if new_response.status_code == 200:
                        new_home = new_response.content.decode('utf-8')
                        new_parsed = html.fromstring(new_home)
                        links_to_product = new_parsed.xpath(XPATH_LINK_TO_PRODUCT)
                        #print(links_to_product)
                        print(f'En esta categoria hay {len(links_to_product)} productos')
                        for new_link in links_to_product:
                            parse_product(new_link, today)
                    else:
                        raise ValueError(f'Error: {new_response.status_code}')
                except ValueError as new_ve:
                    print(new_ve)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == "__main__":
    run()