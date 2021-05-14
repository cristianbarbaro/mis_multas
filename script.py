import sys
import os
import json
from pprint import pprint
from libs import database, pba, send_email
from dotenv import dotenv_values
import users


script_path = os.path.dirname(os.path.realpath(__file__))
config = dotenv_values(script_path + "/.env")
db_path = script_path + "/data/" + config['DB_NAME']


def run(dominio, email):
    pba_url = config['PBA_URL']
    # me retorna las multas actualmente activas en PBA.
    result = pba.get_actas_pba(dominio, pba_url)
    new = []

    if 'actas' in result.keys():
        for acta in result['actas']:
            # Verifico si ya está guardada la multa, caso contrario, debo informar.
            if not database.get_data(acta['id'], db_path):
                database.insert_data(acta, db_path)
                new.append(acta)

    if len(new) > 0:
        # tambien debo enviar un mail al usuario correspondiente:
        sender = config['SENDER']
        passwd = config['PASSWD']
        subject = "Nueva/s multa/s para la patente {0}.".format(dominio)
        text = "Nuevas multas ({0}): \n{1}".format(str(len(new)), json.dumps(new, indent=4, sort_keys=True))

        send_email.send_email(email, sender, passwd, subject, text, result)
    # retorna las multas obtenidas por la api y las multas nuevas, si existen.
    # de esta manera las multas se van almacenando en la base de datos.

    return result


for dominio in users.users.keys():
    email = users.users[dominio]
    dominio = dominio.upper()
    run(dominio, email)

exit(0)