from pprint import pprint

import requests

from read_xlsx import edit_xlsx_ECP_table, cell_color_edit
from settings import proxies
from single_digital_platform import entry


session = requests.Session()
session.proxies.update(proxies)
authorization = entry(session, login='daa87', password='Daa026')

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
    'EvnSection_disDate_Range': '01.06.2024 - 30.06.2024',
    'LpuSection_cid': '',
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

response = session.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data).json()

departments = {'Всего по больнице': 0}
for item in response.get('data'):
    departments[item.get('LpuSection_Name')] = 0

for item in response.get('data'):
    departments[item.get('LpuSection_Name')] += 1
    departments['Всего по больнице'] += 1

pprint(departments)
path_to_excel_tabel = '/Users/aleksejdegtarev/Desktop/ЕЦП выгрузка.xlsx'

departments_rows = {
    'Нефрологическое отделение (в том числе дневной стаицонар)': 3,
    'Инфекционное боксированное отделение (детское)': 4,
    'Травматолого-ортопедическое отделение': 5,
    'Пульмонологическое отделение (в том числе дневной стационар)': 6,
    'Отделение острых отравлений': 7,
    'Отоларингологическое отделение (в том числе дневной стационар)': 8,
    'Хирургическое отделение детское №1 (в том числе гнойный профиль, в том числе дневной стационар)': 9,
    'Хирургическое отделение детское № 3 (в том числе дневной стационар)': 10,
    'Офтальмологическое отделение детское (в том числе дневной стаицонар)': 11,
    'Урологическое отделение (в том числе дневной стационар)': 12,
    'Нейрохирургическое отделение': 13,
    'Хирургическое отделение детское № 2 (для новорожденных и недоношенных детей)': 14,
    'Гастроэнтерологическое отделение (в том числе дневной стационра)': 15,
    'Отделение медицинской реабилитации для пациентов с соматическими заболеваниями': 16,
    'Педиатрическое отделение (для детей до 1 года, в том числе дневной стаицонар)': 17,
    'Отделение медицинской реабилитации пациентов с нарушением функции центральной нервной системы': 18,
    'Педиатрическое отделение (в том числе дневной стационар)': 19,
    'Детское психоневрологическое отделение (в том числе дневной стационар)': 20,
    'Отделение патологии новорожденных и недоношенных детей': 21,
    'Отделение анестезиологии-реанимации и интенсивной терапии №2 (для новорожденных детей для хирургического отделения детского номер два)': 23,
    'Детское ожоговое отделение': 24,
    'Всего по больнице': 25
}

for item in departments_rows:
    if item in list(departments.keys()):
        index = f'N{departments_rows.get(item)}'
        value = departments.get(item)
        edit_xlsx_ECP_table(
            path=path_to_excel_tabel,
            index=index,
            value=value,
        )

for item in range(3, 25):
    cell_color_edit(path_to_excel_tabel, f'P{item}')
