import sqlite3


conn = sqlite3.connect('data.db')
c = conn.cursor()
c.execute("CREATE TABLE multas (id varchar, data)")
conn.close()

exit(0)