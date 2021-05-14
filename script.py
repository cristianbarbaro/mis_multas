import sys
import os
import json
import logging
from pprint import pprint
from libs import database, pba, send_email
from dotenv import dotenv_values
import users


script_path = os.path.dirname(os.path.realpath(__file__))
config = dotenv_values(script_path + "/.env")
db_path = script_path + "/data/" + config['DB_NAME']

# setting logging
logs_path = str(script_path) + "/logs/multas.log"
logging.basicConfig(filename=logs_path, level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def run(dominio, email):
    pba_url = config['PBA_URL']
    # me retorna las multas actualmente activas en PBA.
    result = pba.get_actas_pba(dominio, pba_url)
    new = []

    if 'actas' in result.keys():
        for acta in result['actas']:
            # Verifico si ya está guardada la multa, caso contrario, debo informar.
            if not database.get_data(acta['id'], db_path):
                logging.info("Nueva multa encontrada para dominio {0}. Se inserta en base de datos.".format(dominio))
                database.insert_data(acta, db_path)
                new.append(acta)

    if len(new) > 0:
        # tambien debo enviar un mail al usuario correspondiente:
        sender = config['SENDER']
        passwd = config['PASSWD']
        subject = "Nueva/s multa/s para la patente {0}.".format(dominio)
        text = "Nuevas multas ({0}): \n{1}".format(str(len(new)), json.dumps(new, indent=4, sort_keys=True))
        logging.info("Se envía un email a {0} relacionado a patente {1}".format(email, dominio))
        try:
            send_email.send_email(email, sender, passwd, subject, text, result)
        except Exception as err:
            logging.error("Ocurrió una excepción: {0}".format(err))

    return result


for dominio in users.users.keys():
    email = users.users[dominio]
    dominio = dominio.upper()
    logging.info("Ejecutando búsqueda de multas para patente {0}.".format(dominio))
    run(dominio, email)

logging.info("Fin ejecución.")
exit(0)