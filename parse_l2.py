import requests
import json
from datetime import datetime
from settings import proxies, login_l2, password_l2

import gspread


session = requests.Session()
session.proxies.update(proxies)


def get_patients_from_table(interval: str) -> list:
    """Получение списка номеров выписанных историй из сводной гугл-таблице"""
    gs = gspread.service_account(filename='access.json')
    sh = gs.open_by_key('1feNhDOpE41gwPwuvtW_V5kZH2hFSt9qc8gZvmoH2UIE')

    worksheet = sh.get_worksheet_by_id(0)

    result = []
    for item in worksheet.get(interval):
        if len(item) > 0:
            result.append(item[0])
    return result


def authorization_l2(connect, login, password):
    """Авторизация в L2"""
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Origin': 'http://192.168.10.161',
        'Referer': 'http://192.168.10.161/ui/login',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'X-KL-kav-Ajax-Request': 'Ajax_Request',
    }

    json_data = {
        'username': f'{login}',
        'password': f'{password}',
        'totp': '',
    }

    response = connect.post('http://192.168.10.161/api/users/auth', headers=headers, json=json_data, verify=False)
    return response.status_code, response.json()


def get_all_favorites(connect):
    """Получение историй из Избранное"""
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'http://192.168.10.161',
        'Referer': 'http://192.168.10.161/ui/stationar',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'X-KL-kav-Ajax-Request': 'Ajax_Request',
    }

    response = connect.post(
        'http://192.168.10.161/api/directions/all-directions-in-favorites',
        headers=headers,
        json={},
        verify=False,
    )
    return response.json()


def get_all_pk_history(connect, number):
    """Получение всех номеров направлений в истории"""

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Origin': 'http://192.168.10.161',
        'Referer': 'http://192.168.10.161/ui/stationar',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    }

    json_data = {
        'direction': number,
        'r_type': 'all',
        'every': False,
    }

    response = connect.post(
        'http://192.168.10.161/api/stationar/directions-by-key',
        headers=headers,
        json=json_data,
        verify=False,
    )
    return response.json()


def get_initial_examination(connect):
    """Получение данных из первичного осмотра"""
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Origin': 'http://192.168.10.161',
        'Referer': 'http://192.168.10.161/ui/stationar',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'X-KL-kav-Ajax-Request': 'Ajax_Request',
    }

    json_data = {
        'direction': 2350741, # забирать из get_all_favorites(connect)
        'r_type': 'primary receptions',
        'every': False,
    }

    response = connect.post(
        'http://192.168.10.161/api/stationar/directions-by-key',
        headers=headers,
        json=json_data,
        verify=False,
    )
    return response.json()


def get_history_content(connect, number):

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Origin': 'http://192.168.10.161',
        'Referer': 'http://192.168.10.161/ui/stationar',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'X-KL-kav-Ajax-Request': 'Ajax_Request',
    }

    json_data = {
        'pk': number, # номер направления, не истории
        'force': True,
    }

    response = connect.post(
        'http://192.168.10.161/api/directions/paraclinic_form',
        headers=headers,
        json=json_data,
        verify=False,
    )

    return response.json()


authorization_l2(session, login_l2, password_l2)
all_discharged_patients = get_all_favorites(session)['data'] # direction - история болезни, client - ФИО и дата рождения
# get_initial_examination(session) # pk - номер направления
# discharged = get_patients_from_table('P3:P42') # список выписанных номеров историй


for elem in all_discharged_patients:
    patient_data = {}

    discharge_summary = get_all_pk_history(session, elem['direction'])['data'][0]['pk']
    data = get_history_content(session, discharge_summary)

    patient_data["surname"] = data['patient']['fio_age'].split()[0]
    patient_data["name"] = data['patient']['fio_age'].split()[1]
    patient_data["patronymic"] = data['patient']['fio_age'].split()[2]
    patient_data["birthday"] = data['patient']['fio_age'].split()[4]
    patient_data["doc"] = data['patient']['doc'].split()[0]

    patient_data["date_start"] = data['researches'][0]['research']['groups'][1]['fields'][0]['value']
    patient_data["time_start"] = data['researches'][0]['research']['groups'][1]['fields'][1]['value']
    raw_date_end = data['researches'][0]['research']['groups'][2]['fields'][0]['value']
    patient_data["date_end"] = datetime.strptime(raw_date_end, '%Y-%m-%d').strftime('%d.%m.%Y')
    patient_data["time_end"] = data['researches'][0]['research']['groups'][2]['fields'][1]['value']
    patient_data["bed_days"] = data['researches'][0]['research']['groups'][2]['fields'][2]['value']

    patient_data["icd_diagnosis"] = data['researches'][0]['research']['groups'][4]['fields'][1]['value'].split()[0]

    treatment = ''
    for element in data['researches'][0]['research']['groups'][6]['fields']:
        treatment += f'{element["value"]}\n'
    patient_data["treatment"] = treatment

    recommendations = ''
    for element in data['researches'][0]['research']['groups'][8]['fields']:
        recommendations += f'{element["title"]}: {element["value"]}\n'
    patient_data["recommendations"] = recommendations

    with open(f'patients/{patient_data["surname"]}.json', 'w') as file:
        json.dump(patient_data, file, ensure_ascii=False, indent=4)
