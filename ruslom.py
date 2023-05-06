import requests

import os
from dotenv import load_dotenv

load_dotenv()

LOGIN = os.getenv("LOGIN_EKB")
PASS = os.getenv("PASS_EKB")


class Ruslom:
    def __init__(self):
        self.session = requests.session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        }
        self.url = 'https://ruslom-ekb.ru/wp-login.php'

    def auth_login(self):
        auth = {
            "log": LOGIN,
            "pwd": PASS,
            "testcookie": "1"
        }
        # TODO тут поменял  verify=False
        auth = self.session.post(url=self.url, data=auth, verify=True)
        cookies = auth.cookies
        print('Аутентификация')
        self.session.cookies = cookies
        data = {
            "ss_action": "save",
            "cp_cena_m_roz": "22 500",
            "cp_cena_m_org": "22 502",
            "cp_cena_m_ocn": "7 000",
            "cp_cena_m_st": "6 000",
            "cp_cena_medi": "610",
            "cp_cena_allum": "100",
            "cp_cena_br_lt": "350",
            "cp_cena_nerg": "160",
            "cp_cena_acb": "50",
            "cp_cena_sv": "90",
            "cp_save": "Сохранить"
        }

        result = self.session.post(url='https://ruslom-ekb.ru/wp-admin/themes.php?page=themadmin', data=data,
                                   verify=False, timeout=50)
        result.raise_for_status()

        print('Цены поменял! ')

    def run(self):
        self.auth_login()


if __name__ == '__main__':
    site = Ruslom()
    site.run()
