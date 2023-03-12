import os
import sqlite3
from pathlib import Path
from collections.abc import Sequence, Iterable
from sqlite3 import Error, IntegrityError, Connection


FILE_DB = os.path.join(Path(__file__).parent.resolve(), 'maxlom_price.db')


def sql_connection() -> Connection | None:
    try:
        connect_ = sqlite3.connect(FILE_DB)
        return connect_
    except Error:
        print(Error)


def sql_insert(connect_: Connection, entities_: Iterable) -> None:
    cursor = connect_.cursor()
    try:
        cursor.execute(
            """INSERT INTO price(
            id, cp_cena_m_roz, cp_cena_m_org, cp_cena_m_ocn, cp_cena_m_st, cp_cena_medi, 
            cp_cena_allum, cp_cena_br_lt, cp_cena_nerg,
            cp_cena_acb, cp_cena_sv, created_data) 
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", [item for item in entities_])
        connect_.commit()
    except IntegrityError as exp:
        print(f"ДАННЫЕ С ТАКИМ ID уже есть в БД! >>> {exp}")


def get_all_data_sql_fetch(connect_: Connection) -> list[tuple]:
    cursor = connect_.cursor()
    cursor.execute('SELECT * FROM price')
    rows = cursor.fetchall()

    return rows


def get_last_id_number_sql_fetch(connect_: Connection) -> int:
    """
    Функция нужна для получения id крайней записи, для дальнейшего увеличение +1
    :param connect_: Коннект базы данных
    :return number_id[0]: Последняя запись в поле id
    """
    cursor = connect_.cursor()
    cursor.execute('SELECT id FROM price ORDER BY id DESC')
    number_id = cursor.fetchone()

    return number_id[0]


if __name__ == "__main__":
    connect = sql_connection()

    # entities = ('65',
    #             '22 000',
    #             '22 002',
    #             '7 000',
    #             '14 000',
    #             '630',
    #             '123',
    #             '480',
    #             '93',
    #             '355',
    #             '51',
    #             '11.03.2023')
    # sql_insert(connect, entities)

    all_data = get_all_data_sql_fetch(connect)
    print(all_data)

    print('*'*70)
    print('\n')
    for index, row in enumerate(all_data, 1):
        print(f"Line {index} >>> ", row)
    print('\n')
    print('*'*70)

