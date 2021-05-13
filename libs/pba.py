import requests


def get_actas_pba(dominio, url):
    response = requests.get(url + dominio, verify=False)

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
