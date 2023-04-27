import json
import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

client_id = '855070'
api_key = '69028463-5dd9-4b53-a49b-b1d0bae2cf5e'
headers = {
    'Client-Id': client_id,
    'Api-Key': api_key
}


with open('text.html', 'r', encoding='UTF-8') as f:
    data = f.read()
soup = BeautifulSoup(data, features='html.parser')
soup = soup.find('div', {'schema': '[object Object]'}).find_all('div')[1::]

d = {}
for index, element in enumerate(soup):
    if 'Характеристики' in element.next:
        continue
    if 'index_row' in str(element):
        response = element.find_all('div')
        d[response[0].text.strip()] = response[1].text.strip().replace('\xa0', '').replace('₽', '')

if 'Вес с упаковкой, г' in d.keys():
    d['weight'] = d['Вес с упаковкой, г']
    d['weight_unit'] = 'g'
else:
    d['weight'] = d['Вес с упаковкой, кг']
    d['weight_unit'] = 'kg'
d['Длина × Ширина × Высота'] = d['Длина × Ширина × Высота'].split(' x ')
d['depth'] = d['Длина × Ширина × Высота'][0]
d['width'] = d['Длина × Ширина × Высота'][1]
d['height'] = d['Длина × Ширина × Высота'][2]

data_el = {
    "offer_id": "",
    "product_id": 483801986,
    "sku": 0
}
r = requests.post('https://api-seller.ozon.ru/v2/product/info', headers=headers, data=json.dumps(data_el)).json()[
    'result']
# print(r)
url = 'https://api-seller.ozon.ru/v2/product/import'
data = {
    'items': [
        {
            'attributes': [],
            'category_id': r['category_id'],
            'depth': d['depth'],  # TODO: Check it
            'dimension_unit': 'mm',  # TODO: Check it
            'height': d['height'],
            'images': ['https://ir.ozone.ru/s3/multimedia-t/6382045493.jpg',
                       'https://ir.ozone.ru/s3/multimedia-l/6332904873.jpg',
                       'https://ir.ozone.ru/s3/multimedia-m/6332904874.jpg',
                       'https://ir.ozone.ru/s3/multimedia-k/6332904872.jpg',
                       'https://ir.ozone.ru/s3/multimedia-p/6332904877.jpg',
                       'https://ir.ozone.ru/s3/multimedia-j/6332904871.jpg'],
            'name': d['Название'],
            'offer_id': 'blablabla4',
            'price': "3000",
            'vat': '0',
            'weight': d['weight'],
            'weight_unit': d['weight_unit'],
            'width': d['width']
        }
    ]
}
# print(d)
req = requests.post('https://api-seller.ozon.ru/v3/category/attribute', headers=headers, data=json.dumps({
    "attribute_type": "ALL",
    "category_id": [
        r['category_id']
    ],
    "language": "RU"
}
)
                    ).json()['result'][0]['attributes']
atrs = []

for i in req:
    if i['name'] in d.keys():
        atrs.append({
            'complex_id': 0,
            'id': i['id'],
            'values': [
                {
                    'dictionary_value_id': i['dictionary_id'],
                    'value': d[i['name']]
                }
            ]
        })
data['items'][0]['attributes'] = atrs
print(atrs)
exit(0)
task_id = requests.post(url, headers=headers, data=json.dumps(data)).json()['result']['task_id']
r = requests.post('https://api-seller.ozon.ru/v1/product/import/info', headers=headers, data=json.dumps({
    'task_id': task_id
}))
print(r.json())
#exit(0)


exit(0)
item_url = 'https://seller.ozon.ru/app/products/483801974/edit/preview'
url = 'https://seller.ozon.ru/app/products?filter=all'
options = uc.ChromeOptions()
# options.headless = True
driver = uc.Chrome(use_subprocess=True, options=options)
driver.get(url)
driver.maximize_window()
time.sleep(3)
driver.save_screenshot("datacamp1.png")
driver.find_element(By.CLASS_NAME, 'button-module_text_2lz6v').click()
time.sleep(3)
driver.find_element(By.NAME, 'autocomplete').send_keys('9870739395')
driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

time.sleep(3)
driver.find_element(By.NAME, 'otp').send_keys(input())
time.sleep(5)
driver.get('https://seller.ozon.ru/app/products/483801986/edit/preview')
time.sleep(5)
print(driver.page_source)
driver.save_screenshot("datacamp2.png")
driver.close()
