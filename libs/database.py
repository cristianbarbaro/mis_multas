import sqlite3
import json


def create_db(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("CREATE TABLE multas (id varchar, dominio varchar, data)")
    conn.close()

    return


def insert_data(data, db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("INSERT INTO multas values (?, ?, ?)",
                [data['id'], data['dominio'], json.dumps(data)])
    conn.commit()
    conn.close()

    return


def get_data(id, db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("SELECT data FROM multas WHERE id=?", (id,))

    multa = c.fetchone()

    if multa:
        return multa[0]
    else:
        return False


def delete_data(id, db_name):
    pass


