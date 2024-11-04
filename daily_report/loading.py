import os
import json
from pprint import pprint

import requests

from daily_report.data_for_trauma_point import get_ready_data, create_text
from daily_report.trauma_point import search_patients_ext6, date_in_milliseconds, get_evn_pl_number, \
    save_first_data_vizit, save_visit, create_template, save_text_protocol, finished, add_initial_examination_service, \
    get_operation_id, add_operation_service
from parse_l2 import authorization_l2
from read_xlsx import read_xlsx, find_index
from settings import (login_l2, password_l2, proxies, LPU_SECTION_ID_TP, VIZIT_TYPE_ID_TP, LPU_SECTION_ID_LOR, \
                      VIZIT_TYPE_ID_LOR, LPU_SECTION_PROFILE_ID_TP, LPU_SECTION_PROFILE_ID_LOR,
                      USLUGA_COMPLEX_ID_TP_SECOND,
                      USLUGA_COMPLEX_ID_TP_FIRST, USLUGA_COMPLEX_ID_LOR, RESULTCLASS_ID_TP)
from single_digital_platform import entry, mkb


path = '/Users/aleksejdegtarev/PycharmProjects/integration_with_single_digital_platform/daily_report/tables'

duty_files = os.listdir(path)
if len(duty_files) > 1:
    print('Много отчетов уже загружено. Удали лишние')
else:
    file = duty_files[0]
    duty_date = file.split(' ')[0]  # Дата отчета
    table_data = read_xlsx(f'{path}/{file}')
    column = find_index(table_data)

    for item in table_data:
        try:
            if item[0] is not None and item[0] != 'Направление':
                ambulance_card_number = item[column].split(' ')[0]

                """Блок получения данных из L2"""
                session = requests.Session()
                authorization_l2(session, login=login_l2, password=password_l2)
                data_for_ecp = get_ready_data(session, ambulance_card_number, duty_date)
                session.close()

                with open('/Users/aleksejdegtarev/PycharmProjects/integration_with_single_digital_platform/jsonS/doctors.json', 'r') as file:
                    doctors = json.load(file)

                doctor_surname = data_for_ecp.get('Врач').split(' ')[0]

                """Блок выгрузки в ЕЦП"""
                if doctor_surname in doctors.keys():
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

                    correct_format_date = '-'.join(duty_date.split('.')[::-1])
                    """Тут деление на ТП и ЛОР"""
                    if ('Консультация травматолога (первичный прием)' in data_for_ecp.get('Протокол')
                            or 'Консультация травматолога (повторный прием)' in data_for_ecp.get('Протокол')):
                        first_save = save_first_data_vizit(
                            session,
                            med_staff_fact_id=med_staff_fact_id,
                            med_personal_id=med_personal_id,
                            person_evn_id=patient_data[0].get('PersonEvn_id'),
                            person_id=patient_data[0].get('Person_id'),
                            server_id=patient_data[0].get('Server_id'),
                            date_pl=duty_date,
                            time_pl=data_for_ecp.get('Время осмотра'),
                            evn_pl_number=pl_number,
                            lpu_section_id=LPU_SECTION_ID_TP,
                            vizit_type_id=VIZIT_TYPE_ID_TP,
                        )

                        """Добавить ветвление if для повторных осмотров"""
                        if data_for_ecp.get('Дата осмотра'):

                            mkb_index = data_for_ecp.get('Диагноз по МКБ').split(' ')[0]
                            diag_id = mkb(session, letter=mkb_index)[0]['Diag_id']

                            next_save = save_visit(
                                session,
                                date_save_revers=data_for_ecp.get('Дата осмотра'),
                                evn_vizit_pl_id=first_save.get('EvnVizitPL_id'),
                                person_id=patient_data[0].get('Person_id'),
                                person_evn_id=patient_data[0].get('PersonEvn_id'),
                                date_save=duty_date,
                                time_save=data_for_ecp.get('Время осмотра'),
                                med_staff_fact_id=med_staff_fact_id,
                                service_type_id='6',
                                diag_id=diag_id,
                                diagnos_text=data_for_ecp.get('Диагноз'),
                                lpu_section_id=LPU_SECTION_ID_TP,
                                vizit_type_id=VIZIT_TYPE_ID_TP,
                                lpu_section_profile_id=LPU_SECTION_PROFILE_ID_TP
                            )

                            examination_service = add_initial_examination_service(
                                session,
                                evn_id=first_save.get('EvnVizitPL_id'),
                                medpersonal_id=med_personal_id,
                                person_id=patient_data[0].get('Person_id'),
                                personevn_id=patient_data[0].get('PersonEvn_id'),
                                server_id=patient_data[0].get('Server_id'),
                                medstafffact_id=med_staff_fact_id,
                                exam_date=duty_date,
                                start_time=data_for_ecp.get('Время осмотра'),
                                end_time=data_for_ecp.get('Время осмотра'),
                                usluga_complex_id=USLUGA_COMPLEX_ID_TP_FIRST,
                                lpu_section_id=LPU_SECTION_ID_TP,
                                lpu_section_profile_id=LPU_SECTION_PROFILE_ID_TP
                            )

                            for_template = date_in_milliseconds()
                            template_number = create_template(
                                session,
                                date_in_ms=f'{for_template}',
                                person_id=patient_data[0].get('Person_id'),
                                evn_vizit_pl_id=first_save.get('EvnVizitPL_id'),  # из first_save
                                med_personal_id=med_personal_id,
                                med_staff_fact_id=med_staff_fact_id,
                                lpu_section_id=LPU_SECTION_ID_TP,
                            )

                            text = 'Консультация травматолога (первичный прием)\n' \
                                   f'Дата осмотра: {duty_date};\n' \
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
                                diag_w='13947',  # пока так оставить, но нужен справочник id обстоятельств травм по МКБ
                                result_class_id=RESULTCLASS_ID_TP
                            )

                        elif data_for_ecp.get('по '):
                            mkb_index = data_for_ecp.get('Код по МКБ-10').split(' ')[0]
                            diag_id = mkb(session, letter=mkb_index)[0]['Diag_id']

                            next_save = save_visit(
                                session,
                                date_save_revers=correct_format_date,
                                evn_vizit_pl_id=first_save.get('EvnVizitPL_id'),
                                person_id=patient_data[0].get('Person_id'),
                                person_evn_id=patient_data[0].get('PersonEvn_id'),
                                date_save=duty_date,
                                time_save=data_for_ecp.get('Время осмотра'),
                                med_staff_fact_id=med_staff_fact_id,
                                service_type_id='4',
                                diag_id=diag_id,
                                diagnos_text=data_for_ecp.get('Диагноз'),
                                lpu_section_id=LPU_SECTION_ID_TP,
                                vizit_type_id=VIZIT_TYPE_ID_TP,
                                lpu_section_profile_id=LPU_SECTION_PROFILE_ID_TP
                            )

                            examination_service = add_initial_examination_service(
                                session,
                                evn_id=first_save.get('EvnVizitPL_id'),
                                medpersonal_id=med_personal_id,
                                person_id=patient_data[0].get('Person_id'),
                                personevn_id=patient_data[0].get('PersonEvn_id'),
                                server_id=patient_data[0].get('Server_id'),
                                medstafffact_id=med_staff_fact_id,
                                exam_date=duty_date,
                                start_time=data_for_ecp.get('Время осмотра'),
                                end_time=data_for_ecp.get('Время осмотра'),
                                usluga_complex_id=USLUGA_COMPLEX_ID_TP_SECOND,
                                lpu_section_id=LPU_SECTION_ID_TP,
                                lpu_section_profile_id=LPU_SECTION_PROFILE_ID_TP
                            )

                            for_template = date_in_milliseconds()
                            template_number = create_template(
                                session,
                                date_in_ms=f'{for_template}',
                                person_id=patient_data[0].get('Person_id'),
                                evn_vizit_pl_id=first_save.get('EvnVizitPL_id'),  # из first_save
                                med_personal_id=med_personal_id,
                                med_staff_fact_id=med_staff_fact_id,
                                lpu_section_id=LPU_SECTION_ID_TP,
                            )

                            text = 'Консультация травматолога (повторный прием)\n' \
                                   f'Дата осмотра: {duty_date};\n' \
                                   f'Время осмотра: {data_for_ecp.get("Время осмотра")}.\n' \
                                   f'Жалобы: {data_for_ecp.get("Жалобы")}\n' \
                                   f'{data_for_ecp.get("Визуально")}\n' \
                                   f'Рекомендовано: {data_for_ecp.get("Рекомендованное")}\n' \

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
                                diag_w='13947',  # пока так оставить, но нужен справочник id обстоятельств травм по МКБ
                                result_class_id=RESULTCLASS_ID_TP
                            )
                    elif data_for_ecp.get('Протокол') == 'Консультация врача-оториноларинголога ':

                        first_save = save_first_data_vizit(
                            session,
                            med_staff_fact_id=med_staff_fact_id,
                            med_personal_id=med_personal_id,
                            person_evn_id=patient_data[0].get('PersonEvn_id'),
                            person_id=patient_data[0].get('Person_id'),
                            server_id=patient_data[0].get('Server_id'),
                            date_pl=duty_date,
                            time_pl=data_for_ecp.get('Время осмотра'),
                            evn_pl_number=pl_number,
                            lpu_section_id=LPU_SECTION_ID_LOR,
                            vizit_type_id=VIZIT_TYPE_ID_LOR,
                        )

                        mkb_index = data_for_ecp.get('Диагноз по МКБ').split(' ')[0]
                        diag_id = mkb(session, letter=mkb_index)[0]['Diag_id']

                        next_save = save_visit(
                            session,
                            date_save_revers=data_for_ecp.get('Дата осмотра'),
                            evn_vizit_pl_id=first_save.get('EvnVizitPL_id'),
                            person_id=patient_data[0].get('Person_id'),
                            person_evn_id=patient_data[0].get('PersonEvn_id'),
                            date_save=duty_date,
                            time_save=data_for_ecp.get('Время осмотра'),
                            med_staff_fact_id=med_staff_fact_id,
                            service_type_id='6',
                            diag_id=diag_id,
                            diagnos_text=data_for_ecp.get('Диагноз'),
                            lpu_section_id=LPU_SECTION_ID_LOR,
                            vizit_type_id=VIZIT_TYPE_ID_LOR,
                            lpu_section_profile_id=LPU_SECTION_PROFILE_ID_LOR
                        )

                        examination_service = add_initial_examination_service(
                            session,
                            evn_id=first_save.get('EvnVizitPL_id'),
                            medpersonal_id=med_personal_id,
                            person_id=patient_data[0].get('Person_id'),
                            personevn_id=patient_data[0].get('PersonEvn_id'),
                            server_id=patient_data[0].get('Server_id'),
                            medstafffact_id=med_staff_fact_id,
                            exam_date=duty_date,
                            start_time=data_for_ecp.get('Время осмотра'),
                            end_time=data_for_ecp.get('Время осмотра'),
                            usluga_complex_id=USLUGA_COMPLEX_ID_LOR,
                            lpu_section_id=LPU_SECTION_ID_LOR,
                            lpu_section_profile_id=LPU_SECTION_PROFILE_ID_LOR
                        )

                        for_template = date_in_milliseconds()
                        template_number = create_template(
                            session,
                            date_in_ms=f'{for_template}',
                            person_id=patient_data[0].get('Person_id'),
                            evn_vizit_pl_id=first_save.get('EvnVizitPL_id'),  # из first_save
                            med_personal_id=med_personal_id,
                            med_staff_fact_id=med_staff_fact_id,
                            lpu_section_id=LPU_SECTION_ID_LOR,
                        )

                        text = create_text(data_for_ecp, duty_date)

                        template = save_text_protocol(
                            session,
                            evn_xml_id=template_number[0].get('EvnXml_id'),
                            evn_vizit_pl_id=first_save.get('EvnVizitPL_id'),
                            protocol_text=text
                        )

                        if data_for_ecp.get('Код операции'):
                            oper_code = data_for_ecp.get('Код операции').lstrip('А ')
                            usluga_complex_id = get_operation_id(
                                session,
                                date_mls=f'{for_template}',
                                date=duty_date,
                                evn_usluga_pid=first_save.get('EvnVizitPL_id'),
                                lpu_section_pid=LPU_SECTION_ID_LOR,
                                operation_code=f'A{oper_code}'
                            )

                            add_operation_service(
                                session,
                                med_personal_id=med_personal_id,
                                evn_id=first_save.get('EvnVizitPL_id'),
                                person_id=patient_data[0].get('Person_id'),
                                person_evn_id=patient_data[0].get('PersonEvn_id'),
                                evn_usluga_oper_pid=first_save.get('EvnVizitPL_id'),
                                oper_start_date=duty_date,
                                oper_end_date=duty_date,
                                oper_start_time=data_for_ecp.get('Время осмотра'),
                                oper_end_time=data_for_ecp.get('Время осмотра'),
                                lpu_section_uid=LPU_SECTION_ID_LOR,
                                lpu_section_profile_id=LPU_SECTION_PROFILE_ID_LOR,
                                med_staff_fact_id=med_staff_fact_id,
                                usluga_complex_id=usluga_complex_id
                            )

                        finished(
                            session,
                            evn_pl_id=first_save.get('EvnPL_id'),
                            diag_id=diag_id,
                            text_diag=data_for_ecp.get('Диагноз'),
                            diag_w='13947',  # пока так оставить, но нужен справочник id обстоятельств травм по МКБ
                            result_class_id=RESULTCLASS_ID_TP
                        )

                    print(data_for_ecp.get('Фамилия'), 'выгружен!')
                    session.close()
                else:
                    print(f'{doctor_surname} нет в doctors.json')
        except KeyError as error:
            print(f'{data_for_ecp.get("Фамилия")}: evn_xml_id=template_number[0].get("EvnXml_id")')
        except AttributeError as error:
            print(error)
        except Exception as error:
            print(f'{data_for_ecp.get("Фамилия")}: {error}')
