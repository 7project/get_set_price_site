from bs4 import BeautifulSoup
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
}

response = requests.get("https://74vtormet.ru/", headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
data = soup.find_all('span', class_="pricing__price")

name_metal = ['Медь', 'Алюминий', 'Нержавеющая сталь', 'Латунь', 'Бронза', 'Черный лом', 'АКБ']
for index, item in enumerate(data):
    print(f'{name_metal[index]} - {item.text.rstrip()}')

# TODO нужно написать проверку на получаемые данные - числа
# Медь - 480
# Алюминий - 98
# Нержавеющая сталь - 75
# Латунь - 290
# Бронза - 390
# Черный лом - 16
# АКБ - 50
