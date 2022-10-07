import requests
from bs4 import BeautifulSoup
import csv

CSV = 'hotels.csv'
HOST = 'https://ostrovok.ru/'
URL = 'https://ostrovok.ru/hotel/russia/p/central_russia_podmoskovie_vicinity/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.124 YaBrowser/22.9.2.1495 Yowser/2.5 Safari/537.36'
}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.select('.hotels-inner > .hotel-wrapper')
    hotels = []

    for item in items:
        hotels.append(
            {
                'title': item.find('div', class_='zen-hotelcard-content-main').find('a').get_text(strip=True),
                'price': item.find('div', class_='zen-hotelcard-rate-price-value').get_text(strip=True)[0:2] + ' ' + item.find('div', class_='zen-hotelcard-rate-price-value').get_text(strip=True)[2:-1],
                'location': item.find('div', class_='zen-hotelcard-content-main').find('p').get_text(strip=True),
                'link': HOST + item.find('div', class_='zen-hotelcard-nextstep').find('a').get('href')[1:]
            }
        )
    return hotels


def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название отеля', 'Стоимость за ночь', 'Расположение отеля', 'Ссылка на отель'])
        for item in items:
            writer.writerow([item['title'], item['price'], item['location'], item['link']])


def parser():
    pagenation = input('Укажите количество страниц для парсинга: ')
    pagenation = int(pagenation.strip())
    html = get_html(URL)
    if html.status_code == 200:
        hotels = []
        for page in range(1, pagenation + 1):
            print(f'Программа парсит страницу: {page}')
            html = get_html(URL, params={'page': page})
            hotels.extend(get_content(html.text))
            save_doc(hotels, CSV)
    else:
        print('Error')


parser()
