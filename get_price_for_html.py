import datetime

from collections.abc import Callable

from dataclasses import dataclass, field
from sqlite3 import Error, Connection

from bs4 import BeautifulSoup
from database.api_bd import sql_insert, sql_connection, get_last_id_number_sql_fetch

import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
}

response = requests.get("https://74vtormet.ru/", headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
data = soup.find_all('span', class_="pricing__price")

# TODO вывод на консоль, данные получаем именно в таком порядке и количестве
name_metal = ['Медь', 'Алюминий', 'Нержавеющая сталь', 'Латунь', 'Бронза', 'Черный лом', 'АКБ']
for index, item in enumerate(data):
    print(f'{name_metal[index]} - {item.text.rstrip()}')

print('*'*70)


# TODO переписать на pydantic с валидацией!!!
@dataclass
class DataPriceOneDay:
    number_id: int
    price_black_metal_retail: str
    price_black_metal_business: str
    price_metal_galvanized: str
    price_metal_shavings: str
    price_metal_copper: str
    price_metal_aluminum: str
    price_metal_bronze: str
    price_metal_stainless_steel: str
    price_metal_brass: str
    price_metal_lead: str
    created_data: str

    def __iter__(self):
        for value in self.__dict__.values():
            yield value

    # def __post_init__(self):
    #     connect_ = sql_connection()
    #     self.number_id = get_last_id_number_sql_fetch(connect_) + 1
    #     print(self.number_id)


def get_next_id_for_items(connect_) -> int:
    number_id = 0
    try:
        number_id = get_last_id_number_sql_fetch(connect_)
        print('Следующая запись под номером', number_id + 1)
    except TypeError as exp:
        print(f'{exp}, Данных нет, создаем первую запись, данная ошибка возникает при создании '
              f'первой записи.')
    return number_id + 1


def get_result_raw(result_raw_: list[str], connect_: Connection, get_next_id_for_items_: Callable) -> dict:
    # TODO написать проверку на длину списка
    number_id_data = get_next_id_for_items_(connect_)
    results_data_ = {
        'number_id': number_id_data,
        'price_black_metal_retail': f'{result_raw_[5]}',
        'price_black_metal_business': f'{result_raw_[5]}',
        'price_metal_galvanized': '7 000',
        'price_metal_shavings': '14 000',
        'price_metal_copper': f'{result_raw_[0]}',
        'price_metal_aluminum': f'{result_raw_[1]}',
        'price_metal_bronze': f'{result_raw_[4]}',
        'price_metal_stainless_steel': f'{result_raw_[2]}',
        'price_metal_brass': f'{result_raw_[3]}',
        'price_metal_lead': f'{result_raw_[6]}',
        'created_data': f'{datetime.datetime.now()}'
    }

    return results_data_


connect = sql_connection()
result_raw = [item.text.rstrip() for item in data]
results_data = get_result_raw(result_raw, connect, get_next_id_for_items)
result = DataPriceOneDay(**results_data)

# TODO поменять нейминг, запись строки в БД
sql_insert(connect, result)


# TODO нужно написать проверку на получаемые данные - числа
# Медь - 480
# Алюминий - 98
# Нержавеющая сталь - 75
# Латунь - 290
# Бронза - 390
# Черный лом - 16
# АКБ - 50

