import json
import requests

from read_xlsx import edit_xlsx_ECP_table, cell_color_edit
from settings import proxies
from single_digital_platform import entry


def get_ECP_departments_data(ses, department_id):

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'priority': 'u=1, i',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'Search',
        'm': 'searchData',
    }

    data = {
        'Person_Surname': '',
        'EvnSection_disDate_Range': '01.07.2024 - 31.07.2024',
        'LpuSection_cid': f'{department_id}',
        'isLeave': '1',
        'PersonCardStateType_id': '1',
        'PersonPeriodicType_id': '1',
        'PrivilegeStateType_id': '1',
        'SearchFormType': 'EvnSection',
        'Person_Firname': '',
        'Person_Birthday_Range': '',
        'Person_Secname': '',
        'MedPersonal_iid': '',
        'limit': '3000',
        'start': '0',
    }

    answer = ses.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data).json()
    return answer


session = requests.Session()
session.proxies.update(proxies)
authorization = entry(session, login='daa87', password='Daa026')

with open('jsonS/departments_in_table.json', 'r') as file:
    data = json.load(file)

path_to_excel_tabel = '/Users/aleksejdegtarev/Desktop/ЕЦП выгрузка.xlsx'

for department in data:
    response = get_ECP_departments_data(session, data.get(department)[1])
    index = f'R{data.get(department)[0]}'
    value = response.get('totalCount')
    edit_xlsx_ECP_table(
        path=path_to_excel_tabel,
        index=index,
        value=value,
    )
    print(department, response.get('totalCount'))

for item in range(3, 25):
    cell_color_edit(path_to_excel_tabel, f'T{item}')
