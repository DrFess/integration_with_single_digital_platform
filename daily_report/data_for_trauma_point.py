from datetime import datetime
from datetime import timedelta
from pprint import pprint
import requests

from parse_l2 import get_history_content, authorization_l2
from settings import login_l2, password_l2, proxies


def get_data_for_traum_point(connect, number_in_table: int):

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Origin': 'http://192.168.10.161',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://192.168.10.161/ui/direction/history',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    json_data = {
        'q': f'{number_in_table}',
    }

    response = connect.post(
        'http://192.168.10.161/api/directions/direction-history',
        headers=headers,
        json=json_data,
        verify=False,
    ).json()
    return response[0].get('events')[0]


def get_patient_pk(connect, number: str):

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Origin': 'http://192.168.10.161',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://192.168.10.161/ui/directions',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    json_data = {
        'type': 5,
        'query': number,
        'list_all_cards': False,
        'inc_rmis': False,
        'inc_tfoms': False,
    }

    response = connect.post(
        'http://192.168.10.161/api/patients/search-card',
        headers=headers,
        json=json_data,
        verify=False,
    ).json()
    return response.get('results')[0].get('pk')


def get_history(connect, pk_number: int, date_1: str, date_2: str):

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Origin': 'http://192.168.10.161',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://192.168.10.161/ui/directions',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    json_data = {
        'iss_pk': None,
        'services': [],
        'forHospSlave': False,
        'type': 3,
        'patient': pk_number,
        'date_from': date_1,
        'date_to': date_2,
    }

    response = connect.post(
        'http://192.168.10.161/api/directions/history',
        headers=headers,
        json=json_data,
        verify=False,
    ).json()
    return response.get('directions')


def get_ready_data(connect, number_from_table, date: str) -> dict:
    raw_data = get_data_for_traum_point(connect, number_from_table)

    last_date = datetime.strptime(date, '%d.%m.%Y').date()
    previous_date_date = last_date + timedelta(days=30)
    previous_date = datetime.strftime(previous_date_date, '%d.%m.%Y')

    for data_item in raw_data:
        if 'Карта' in data_item:
            cart_number = data_item[1].split(' ')[0]
            pk = get_patient_pk(connect, cart_number)
            if get_history(connect, pk, date_1=date, date_2=previous_date):
                for item in get_history(connect, pk, date_1=date, date_2=previous_date):
                    if ('Консультация травматолога (первичный прием)' in item.get('researches') and 'Консультация травматолога (повторный прием)' not in item.get('researches')) or 'Консультация травматолога (повторный прием)' in item.get('researches'):
                        doctor = get_history_content(connect, item.get('pk')).get('researches')[0].get('whoConfirmed').split(',')[0]
                        fio_age = get_history_content(connect, item.get('pk')).get('patient').get('fio_age').split(' ')
                        surname = fio_age[0]
                        name = fio_age[1]
                        patronymic = fio_age[2]
                        age = fio_age[4]

                        ready_data = {
                            'Врач': doctor,
                            'Фамилия': surname,
                            'Имя': name,
                            'Отчество': patronymic,
                            'Дата рождения': age
                        }

                        case_raw_data = get_history_content(connect, item.get('pk')).get('researches')[0].get('research').get('groups')
                        for part in case_raw_data:
                            for field in part.get('fields'):
                                if field.get('title') != '' and field.get('value') != '':
                                    ready_data[field.get('title')] = field.get('value')

                        return ready_data


# session = requests.Session()
# session.proxies.update(proxies)
# authorization_l2(session, login=login_l2, password=password_l2)
#
# pprint(get_ready_data(session, 3049102, '13.08.2024'))
# test = get_data_for_traum_point(session, 3040917)
# for data_item in test:
#     if 'Карта' in data_item:
#         cart_number = data_item[1].split(' ')[0]
#         pk = get_patient_pk(session, cart_number)
#         data = get_history(session, pk, '09.08.2024', '09.08.2024')
#         pprint(get_history_content(session, data[0].get('pk')))
