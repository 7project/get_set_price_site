import time
from pprint import pprint
import random
import requests

import os
from dotenv import load_dotenv

load_dotenv()

# TODO прод
LOGIN = os.environ.get("LOGIN_CHEL")
PASS = os.environ.get("PASS_CHEL")

# LOGIN = os.getenv("LOGIN_CHEL")
# PASS = os.getenv("PASS_CHEL")


class Maxlom:
    def __init__(self, data):
        self.session = requests.session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        }
        self.url = 'https://maxlom74.ru/wp-login.php'
        self.auth = {
            "log": LOGIN,
            "pwd": PASS,
            "testcookie": "1"
        }

        self.data_to_post = data

    def auth_login(self):
        count = 0
        while True:
            try:
                # auth = self.session.post(url=self.url, data=self.auth, verify=True)
                response = self.session.post(url=self.url, data=self.auth, verify=True)
                # pprint(response.status_code)
                # cookies = auth.cookies
                pprint('Аутентификация прошла успешно!')
                return response.status_code
                # return cookies
            except Exception as exp:
                if count < 5:
                    pprint(exp)
                    time.sleep(random.randint(2, 5))
                    count += 1
                else:
                    pprint('НЕУДАЛОСЬ АВТОРИЗОВАТЬСЯ. Прошло 5 попыток соединения!')
                    break

    # def data_post_to_url(self, cookies):
    def data_post_to_url(self):
        # self.session.cookies = cookies
        count = 0
        while True:
            try:
                # result = self.session.post(url='https://maxlom74.ru/wp-admin/themes.php?page=themadmin', data=data,
                                   # verify=True)
                self.session.post(url='https://maxlom74.ru/wp-admin/themes.php?page=themadmin', data=self.data_to_post,
                                   verify=True)
                pprint('Цены на сайте обновлены!')
                break
            except Exception as exp:
                if count < 5:
                    pprint(exp)
                    time.sleep(random.randint(2, 5))
                    count += 1
                else:
                    pprint('ЦЕНЫ НЕ ОБНОВЛЕНЫ. Прошло 5 попыток передачи!')
                    break

    def run(self):
        # cookies = self.auth_login()
        response_status_code = self.auth_login()
        # self.data_post_to_url(cookies)
        if response_status_code == 200:
            self.data_post_to_url()

# TODO дописать модуль получения данных из файла, pickle
# TODO если данных нет сделать гет запрос и получить их - Готово
# TODO если данные есть просто получить их в переменные
data_to_post = {
        "ss_action": "save",
        "cp_cena_m_roz": "22 500",
        "cp_cena_m_org": "22 501",
        "cp_cena_m_ocn": "7 000",
        "cp_cena_m_st": "14 000",
        "cp_cena_medi": "625",
        "cp_cena_allum": "123",
        # TODO бронза
        "cp_cena_br_lt": "485",
        "cp_cena_nerg": "93",
        # TODO латунь
        "cp_cena_acb": "355",
        "cp_cena_sv": "52",
        "cp_save": "Сохранить"
    }

if __name__ == '__main__':
    site = Maxlom(data_to_post)
    site.run()
