# import sqlite3

from api_bd import sql_connection


def sql_table(connect):
    cursor = connect.cursor()

    # TODO подумать над структурой полей таблице что должно быть в каждой строке запроса
    # TODO как хранить данные в числах или строках ?
    cursor.execute(
        "CREATE TABLE price("
        "id integer PRIMARY KEY, "
        "cp_cena_m_roz text, "
        "cp_cena_m_org text, "
        "cp_cena_m_ocn text, "
        "cp_cena_m_st text, "
        "cp_cena_medi text, "
        "cp_cena_allum text, "
        # TODO cp_cena_br_lt -> бронза
        "cp_cena_br_lt text, "
        "cp_cena_nerg text, "
        # TODO cp_cena_acb -> латунь
        "cp_cena_acb text, "
        "cp_cena_sv text, "
        "created_data text)")

    connect.commit()


if __name__ == "__main__":
    con = sql_connection()
    sql_table(con)
