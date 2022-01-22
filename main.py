import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import random
import json


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
}


def get_goods_urls(main_url):
    response = requests.get(url=main_url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    last_page = int(soup.find_all('span', class_='cef202m_plp')[-2].text)

    goods_url_list = []
    for page in tqdm(range(1, 3), colour='green'):
    # for page in range(1, 2):
        response = requests.get(url=f'https://leroymerlin.ru/catalogue/elektroinstrumenty/?page={page}', headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        goods_list = soup.find_all('a', class_='bex6mjh_plp b1f5t594_plp p5y548z_plp pblwt5z_plp nf842wf_plp')

        for item in goods_list:
            goods_url_list.append(f'https://leroymerlin.ru{item.get("href")}')
        time.sleep(random.randrange(2, 5))

    with open('urls.txt', 'w', encoding='utf-8') as file:
        for url in goods_url_list:
            file.write(f'{url}\n')


def get_goods_info():
    with open('urls.txt', encoding='utf-8') as file:
        urls_list = [line.strip() for line in file.readlines()]
    result = []
    for i in tqdm(urls_list):
        try:
            response = requests.get(url=i, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')

            title = soup.find('h1', class_='header-2').text
            price = int(soup.find('span', slot='price').text.replace(' ',''))
            goods_dict = {
                'title': title,
                'price': price,
            }
            result.append(goods_dict)

        except Exception as ex:
            pass

        time.sleep(random.randrange(0, 2))
    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)




def main():
    get_goods_urls('https://leroymerlin.ru/catalogue/elektroinstrumenty/')
    get_goods_info()


if __name__ == '__main__':
    main()