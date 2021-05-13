import requests
import urllib3
from bs4 import BeautifulSoup
import sys
import json
from pprint import pprint
import sqlite3
import database


urllib3.disable_warnings()

dominio = sys.argv[1]

CABA_URL = "https://www.buenosaires.gob.ar/system/ajax"
PBA_URB = "https://infraccionesba.gba.gob.ar/rest/consultar-infraccion?dominio="


def get_actas_caba(dominio):
    data = {
    'tipo_consulta': 'Dominio',
    'dominio': dominio,
    'form_build_id': 'form-RNR8NNKEoHkY8_4Y-lmoeW5HZpCmANVjrzXunqYBfOs',
    'form_id': 'gcaba_infracciones_form'
    }

    response = requests.post(CABA_URL, data=data, verify=False)

    if response.status_code == 200:
        json_response = response.json()
        result = {
            'jurisdicción': 'CABA',
            'actas': []
        }
        for i in json_response:
            if 'data' in i.keys():
                html = i['data']
                soup = BeautifulSoup(html, 'html.parser')
                div_free = soup.find('div', {'class': 'libreDeuda-view mt-2'})
                div_infractions = soup.find('div', {'id': 'actasComprobantes-view'})
                if div_free:
                    p = div_free.findChild('p', recursive=False)
                    result['mensaje'] = p.text
                elif div_infractions:
                    input_tag = soup.find_all('input')
                    for tag in input_tag:
                        if 'data-json' in tag.attrs.keys():
                            result['actas'].append(json.loads(tag.attrs['data-json']))
                    result['mensaje'] = "El dominio {0} tiene {1} infracciones.".format(dominio, len(result['actas']))
    else:
        result = {
            "mensaje": "No se pudo consultar a PBA"
        }
    
    return result


def get_actas_pba(dominio):
    response = requests.get(PBA_URB + dominio, verify=False)

    if response.status_code == 200:
        res = response.json()
        result = {
                'jurisdicción': 'PBA',
                'mensaje': 'El dominio {0} posee {1} infracciones.'.format(dominio, res['tieneInfracciones']),
                'actas': res['infracciones'],
        }
    else:
        result = {
            "mensaje": "No se pudo consultar a PBA"
        }
    
    return result


def run(dominio):
    result = get_actas_pba(dominio)
    new = []

    if 'actas' in result.keys():
        for acta in result['actas']:
            if not database.get_data(acta['id']):
                database.insert_data(acta)
                new.append(acta)

    if len(new) > 0:
        result['actas_nuevas'] = new
    # retorna las multas obtenidas por la api y las multas nuevas, si existen.
    # de esta manera las multas se van almacenando en la base de datos.
    return result


print(run(dominio))