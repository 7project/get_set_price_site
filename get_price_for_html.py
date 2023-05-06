import datetime

from collections.abc import Callable

from dataclasses import dataclass, field
from sqlite3 import Error, Connection

from bs4 import BeautifulSoup
from database.api_bd import sql_insert, sql_connection, get_last_id_number_sql_fetch

import requests

from maxlom import Maxlom

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
}

response = requests.get("https://74vtormet.ru/", headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
data = soup.find_all('span', class_="pricing__price")

# # TODO вывод на консоль, данные получаем именно в таком порядке и количестве
# name_metal = ['Медь', 'Алюминий', 'Нержавеющая сталь', 'Латунь', 'Бронза', 'Черный лом', 'АКБ']
# for index, item in enumerate(data):
#     print(f'{name_metal[index]} - {item.text.rstrip()}')

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

    def convert_number_to_complete(number: str, default: str = '0'):
        """
        Формирование нужного формата строки
        "17,5" -> "17 500"
        "15" -> "15 000"
        :return str -> default = '0'
        """
        try:
            if default != '0':
                return default

            if ',' in number:
                return number.replace(",", " ") + "00"
            else:
                return number + " 000"

        except Exception as exp:
            print(exp)
            return default

    results_data_ = {
        'number_id': number_id_data,
        'price_black_metal_retail': f'{convert_number_to_complete(result_raw_[5])}',
        'price_black_metal_business': f'{convert_number_to_complete(result_raw_[5])}',
        'price_metal_galvanized': f'{convert_number_to_complete("", "7 000")}',
        'price_metal_shavings': f'{convert_number_to_complete("", "14 000")}',
        'price_metal_copper': f'{result_raw_[0]}',
        'price_metal_aluminum': f'{result_raw_[1]}',
        'price_metal_bronze': f'{result_raw_[4]}',
        'price_metal_stainless_steel': f'{result_raw_[2]}',
        'price_metal_brass': f'{result_raw_[3]}',
        'price_metal_lead': f'{result_raw_[6]}',
        'created_data': f'{str(datetime.datetime.now())[:-7]}'
    }

    # TODO нужно возвращать дефолтное значение если код выше упадет
    return results_data_


# TODO блок нужно вынести в функцию
connect = sql_connection()
result_raw = [item.text.rstrip() for item in data]
results_data = get_result_raw(result_raw, connect, get_next_id_for_items)
result = DataPriceOneDay(**results_data)

print(f'cp_cena_m_roz -> {result.price_black_metal_retail}\n'
      f'cp_cena_m_org -> {result.price_black_metal_business}\n'
      f'cp_cena_m_ocn -> {result.price_metal_galvanized}\n'
      f'cp_cena_m_st -> {result.price_metal_shavings}\n'
      f'cp_cena_medi -> {result.price_metal_copper}\n'
      f'cp_cena_allum -> {result.price_metal_aluminum}\n'
      f'cp_cena_br_lt -> {result.price_metal_bronze}\n'
      f'cp_cena_nerg -> {result.price_metal_stainless_steel}\n'
      f'cp_cena_acb -> {result.price_metal_brass}\n'
      f'cp_cena_sv -> {result.price_metal_lead}\n')

# TODO запись данных в БД
# TODO поменять нейминг, запись строки в БД
sql_insert(connect, result)


# TODO цены на 06.05.2023
# data_to_post = {
#         "ss_action": "save",
#         "cp_cena_m_roz": "22 500",
#         "cp_cena_m_org": "22 501",
#         "cp_cena_m_ocn": "7 000",
#         "cp_cena_m_st": "14 000",
#         "cp_cena_medi": "625",
#         "cp_cena_allum": "123",
#         # TODO бронза
#         "cp_cena_br_lt": "485",
#         "cp_cena_nerg": "93",
#         # TODO латунь
#         "cp_cena_acb": "355",
#         "cp_cena_sv": "52",
#         "cp_save": "Сохранить"
#     }

data_to_post = {
        "ss_action": "save",
        "cp_cena_m_roz": result.price_black_metal_retail,
        "cp_cena_m_org": result.price_black_metal_business,
        "cp_cena_m_ocn": result.price_metal_galvanized,
        "cp_cena_m_st": result.price_metal_shavings,
        "cp_cena_medi": result.price_metal_copper,
        "cp_cena_allum": result.price_metal_aluminum,
        # TODO бронза
        "cp_cena_br_lt": result.price_metal_bronze,
        "cp_cena_nerg": result.price_metal_stainless_steel,
        # TODO латунь
        "cp_cena_acb": result.price_metal_brass,
        "cp_cena_sv": result.price_metal_lead,
        "cp_save": "Сохранить"
    }

if __name__ == '__main__':
    # TODO старт, получения данных в нужном формате и запуск второго стрипта на замену
    site = Maxlom(data_to_post)
    site.run()
