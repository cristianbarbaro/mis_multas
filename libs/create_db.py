import os
import sqlite3
from dotenv import dotenv_values

script_path = os.path.dirname(os.path.realpath(__file__))
config = dotenv_values(script_path + "/../.env")
db_path = script_path + "/../data/" + config['DB_NAME']

conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("CREATE TABLE multas (id varchar, dominio varchar, data)")
conn.close()

exit(0)