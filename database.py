import sqlite3
import json


def create_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("CREATE TABLE multas (id varchar, data)")
    conn.close()

    return


def insert_data(data):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute("INSERT INTO multas values (?, ?)",
                [data['id'], json.dumps(data)])
    conn.commit()
    conn.close()

    return


def get_data(id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute("SELECT data FROM multas WHERE id=?", (id,))

    multa = c.fetchone()

    if multa:
        return multa[0]
    else:
        return False


def delete_data(id):
    pass


