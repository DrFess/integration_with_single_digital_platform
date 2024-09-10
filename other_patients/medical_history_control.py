from pprint import pprint

import requests

from parse_l2 import authorization_l2
from settings import login_l2, password_l2


def get_all_records(connect, history_number: int):
    """Получает все записи по номеру истории"""
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Origin': 'http://192.168.10.161',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://192.168.10.161/ui/stationar',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    json_data = {
        'direction': history_number,
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


def get_record_details(connect, record_number: int):

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Origin': 'http://192.168.10.161',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://192.168.10.161/ui/stationar',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    json_data = {
        'pk': record_number,
        'force': True,
    }

    response = connect.post(
        'http://192.168.10.161/api/directions/paraclinic_form',
        headers=headers,
        json=json_data,
        verify=False,
    ).json()
    return response.get('researches')[0].get('research').get('groups')[0].get('fields')[0].get('value')


def add_diaries(connect, service_id: int, history_number: int):
    """Создаёт новый дневник"""
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Origin': 'http://192.168.10.161',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://192.168.10.161/ui/stationar',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    json_data = {
        'service': service_id,
        'main_direction': history_number,
    }

    response = connect.post(
        'http://192.168.10.161/api/stationar/make-service',
        headers=headers,
        json=json_data,
        verify=False,
    )
    return response.json()


"""Создание диагностического эпикриза"""
session = requests.Session()
authorization_l2(session, login_l2, password_l2)

all_records = get_all_records(session, 3083187)

title_records = {}

for item in all_records.get('data'):
    title_records[item.get('pk')] = item.get('researches')[0]

diaries = []

if 'Диагностический эпикриз' not in title_records.values():
    for key in title_records:
        if title_records.get(key) == 'Осмотр':
            diaries.append(key)

title_examination = []
for number in diaries:
    title_examination.append(get_record_details(session, number))

if 'лечащим врачом совместно с заведующим отделением' in title_examination:
    add_diaries(session, service_id=20, history_number=3083187)  # Добавляем диагностический эпикриз при 'service': 20, при 'service': 2 - простой дневник


"""Создание протокола операции"""


def get_patient_pk(connect, history_number: str):
    """Возвращает pk пациента"""
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Origin': 'http://192.168.10.161',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://192.168.10.161/ui/stationar',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    json_data = {
        'pk': history_number,
        'every': False,
    }

    response = connect.post('http://192.168.10.161/api/stationar/load', headers=headers, json=json_data, verify=False)
    return response.json().get('data').get('patient').get('card_pk')


def is_surgery_planned(connect, patient_number: int):
    """Проверяет, есть ли запланированная операция"""

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Origin': 'http://192.168.10.161',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://192.168.10.161/ui/stationar',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    json_data = {
        'card_pk': patient_number,  # pk карточки пациента, не номер истории или номер протокола истории
    }

    response = connect.post(
        'http://192.168.10.161/api/plans/get-plan-operations-by-patient',
        headers=headers,
        json=json_data,
        verify=False,
    )
    return response.json()  # возвращает словарь с ключом data, если нет операции - {'data': []}, иначе .get('data')[0]


# session = requests.Session()
# authorization_l2(session, login_l2, password_l2)
#
# patient_pk = get_patient_pk(session, '2872958')
# if is_surgery_planned(session, patient_pk).get('data'):
#     print('True')
# else:
#     add_diaries(session, 5, 	2872958)
