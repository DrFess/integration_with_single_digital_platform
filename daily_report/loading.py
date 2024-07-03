import json

import requests

from daily_report.data_for_trauma_point import get_ready_data
from daily_report.trauma_point import search_patients_ext6, date_in_milliseconds, get_evn_pl_number, \
    save_first_data_vizit, save_visit, create_template, save_text_protocol, finished
from parse_l2 import authorization_l2
from read_xlsx import read_xlsx
from settings import DOCTORS_LIST, login_l2, password_l2, proxies
from single_digital_platform import entry, mkb


test = read_xlsx('/Users/aleksejdegtarev/PycharmProjects/integration_with_single_digital_platform/daily_report/tables/29.06.2024 первичные.xlsx')
for item in test:
    try:
        if item[0] is not None:
            number = item[1].split(' ')[0]
            doctor_surname = item[12].split(' ')[0]

            """Блок получения данных из L2"""
            session = requests.Session()
            authorization_l2(session, login=login_l2, password=password_l2)
            data_for_ecp = get_ready_data(session, number)
            session.close()
            with open('/Users/aleksejdegtarev/PycharmProjects/integration_with_single_digital_platform/jsonS/doctors.json', 'r') as file:
                doctors = json.load(file)

            """Блок выгрузки в ЕЦП"""
            if doctor_surname in DOCTORS_LIST:
                login = doctors.get(doctor_surname).get('login')
                password = doctors.get(doctor_surname).get('password')
                med_personal_id = doctors.get(doctor_surname).get('MedPersonal_id')
                med_staff_fact_id = doctors.get(doctor_surname).get('MedStaffFact_id')

                session = requests.Session()
                session.proxies.update(proxies)

                authorization = entry(session, login=login, password=password)

                patient_data = search_patients_ext6(
                    session,
                    surname=data_for_ecp.get('Фамилия'),
                    name=data_for_ecp.get('Имя'),
                    patronymic=data_for_ecp.get('Отчество').strip(','),
                    birthday=data_for_ecp.get('Дата рождения')
                )

                for_number = date_in_milliseconds()
                pl_number = get_evn_pl_number(session, for_number)

                correct_format_date = '.'.join(data_for_ecp.get('Дата осмотра').split('-')[::-1])

                first_save = save_first_data_vizit(
                    session,
                    med_staff_fact_id=med_staff_fact_id,
                    med_personal_id=med_personal_id,
                    person_evn_id=patient_data[0].get('PersonEvn_id'),
                    person_id=patient_data[0].get('Person_id'),
                    server_id=patient_data[0].get('Server_id'),
                    date_pl=correct_format_date,
                    time_pl=data_for_ecp.get('Время осмотра'),
                    evn_pl_number=pl_number,
                )

                mkb_index = data_for_ecp.get('Диагноз по МКБ').split(' ')[0]
                diag_id = mkb(session, letter=mkb_index)[0]['Diag_id']

                next_save = save_visit(
                    session,
                    date_save_revers=data_for_ecp.get('Дата осмотра'),
                    evn_vizit_pl_id=first_save.get('EvnVizitPL_id'),
                    person_id=patient_data[0].get('Person_id'),
                    person_evn_id=patient_data[0].get('PersonEvn_id'),
                    date_save=correct_format_date,
                    time_save=data_for_ecp.get('Время осмотра'),
                    med_staff_fact_id=med_staff_fact_id,
                    diag_id=diag_id,
                    diagnos_text=data_for_ecp.get('Диагноз'),
                )

                for_template = date_in_milliseconds()
                template_number = create_template(
                    session,
                    date_in_ms=f'{for_template}',
                    person_id=patient_data[0].get('Person_id'),
                    evn_vizit_pl_id=first_save.get('EvnVizitPL_id'),  # из first_save
                    med_personal_id=med_personal_id,
                    med_staff_fact_id=med_staff_fact_id,
                )

                text = 'Консультация травматолога (первичный прием)\n' \
                       f'Дата осмотра: {correct_format_date};\n' \
                       f'Время осмотра: {data_for_ecp.get("Время осмотра")}.\n' \
                       f'Жалобы: Боль в: {data_for_ecp.get("Боль в:")}\n' \
                       f'Вид травмы: {data_for_ecp.get("Вид травмы")}\n' \
                       f'Дата: {data_for_ecp.get("Дата")}\n' \
                       f'Обстоятельства травмы: {data_for_ecp.get("Обстоятельства травмы")}\n' \
                       f'Локальный статус: Локализация: {data_for_ecp.get("Локализация")};\n' \
                       f'{data_for_ecp.get("Локализация")}' \
                       f'Боль при пальпации: {data_for_ecp.get("Боль при пальпации ")}\n' \
                       f'Движения в суставах: {data_for_ecp.get("Движения в суставах ")}' \
                       f'Обследование: {data_for_ecp.get("Обследование")}\n' \
                       f'Заключительный диагноз: {data_for_ecp.get("Диагноз")}\n' \
                       f'Диагноз по МКБ: {data_for_ecp.get("Диагноз по МКБ")}\n' \
                       f'Лечение: {data_for_ecp.get("Проведенное")}\n' \
                       f'Рекомендации: {data_for_ecp.get("Консультация в городском детском травмпункте")}\n' \
                       f'{data_for_ecp.get("Наблюдение и лечение специалистами на амбулаторном этапе (в поликлинике по месту жительства)")}\n' \
                       f'{data_for_ecp.get("Обезболивание (название препарата, кратность и длительность")}\n' \
                       f'{data_for_ecp.get("Освобождение от занятий физической культурой и спортом")}\n' \
                       f'{data_for_ecp.get("Срок иммобилизации (фиксации)")}\n' \
                       f'{data_for_ecp.get("Местное лечение")}\n' \
                       f'{data_for_ecp.get("Домашний режим")}'

                template = save_text_protocol(
                    session,
                    evn_xml_id=template_number[0].get('EvnXml_id'),
                    evn_vizit_pl_id=first_save.get('EvnVizitPL_id'),
                    protocol_text=text
                )

                finished(
                    session,
                    evn_pl_id=first_save.get('EvnPL_id'),
                    diag_id=diag_id,
                    text_diag=data_for_ecp.get('Диагноз'),
                    diag_w='13950',  # пока так оставить, но нужен справочник id обстоятельств травм по МКБ
                )

                print(data_for_ecp.get('Фамилия'), 'выгружен!')
                session.close()
            else:
                print(f'{doctor_surname} нет в DOCTORS_LIST')
    except KeyError as error:
        print(f'{data_for_ecp.get("Фамилия")}: evn_xml_id=template_number[0].get("EvnXml_id")')
    except AttributeError as error:
        print(f"{data_for_ecp.get('Фамилия')}: correct_format_date = '.'.join(data_for_ecp.get('Дата осмотра').split('-')[::-1])")
    except Exception as error:
        print(f'{data_for_ecp.get("Фамилия")}: {error}')
