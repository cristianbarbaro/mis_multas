import sys
import os
import json
from pprint import pprint
from libs import database, pba
from dotenv import dotenv_values


script_path = os.path.dirname(os.path.realpath(__file__))
config = dotenv_values(script_path + "/.env")
db_path = script_path + "/data/" + config['DB_NAME']


def run(dominio):
    pba_url = config['PBA_URL']
    result = pba.get_actas_pba(dominio, pba_url)
    new = []

    if 'actas' in result.keys():
        for acta in result['actas']:
            if not database.get_data(acta['id'], db_path):
                database.insert_data(acta, db_path)
                new.append(acta)

    if len(new) > 0:
        # tambien debo enviar un mail al usuario correspondiente:
        result['actas_nuevas'] = new
    # retorna las multas obtenidas por la api y las multas nuevas, si existen.
    # de esta manera las multas se van almacenando en la base de datos.

    return result

dominio = sys.argv[1].upper()

pprint(run(dominio))