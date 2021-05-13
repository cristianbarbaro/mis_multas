import requests
from bs4 import BeautifulSoup


def get_actas_caba(dominio, url):
    data = {
    'tipo_consulta': 'Dominio',
    'dominio': dominio,
    'form_build_id': 'form-RNR8NNKEoHkY8_4Y-lmoeW5HZpCmANVjrzXunqYBfOs',
    'form_id': 'gcaba_infracciones_form'
    }

    response = requests.post(url, data=data, verify=False)

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