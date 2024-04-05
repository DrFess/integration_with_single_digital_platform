import json
from pprint import pprint
from datetime import datetime
import requests

from parse_l2 import extract_patient_data_from_L2, get_patients_from_table
from settings import proxies
from single_digital_platform import (
    entry,
    search_patient,
    get_KSG_KOEF,
    get_evn_number,
    save_EVN,
    save_data,
    mkb,
    create_template,
    update_treatment_evn_template,
    update_recommendation_evn_template
)


with open('doctors.json', 'r') as file:
    doctors = json.load(file)

session = requests.Session()
session.proxies.update(proxies)

for item in get_patients_from_table('Q3:Q43'):
    try:
        data = extract_patient_data_from_L2(int(item))
        doctor_surname = data.get('Лечащий врач')

        login = doctors.get(doctor_surname).get('login')
        password = doctors.get(doctor_surname).get('password')
        med_personal_id = doctors.get(doctor_surname).get('MedPersonal_id')
        med_staff_fact_id = doctors.get(doctor_surname).get('MedStaffFact_id')

        authorization = entry(session, login=login, password=password)

        search = search_patient(
            session,
            name=data.get('Имя'),
            surname=data.get('Фамилия'),
            patronymic=data.get('Отчество'),
            birthday=data.get('Дата рождения'),
        )
        patient = search.get('data')[0]['Person_id']

        diagnosis_id = mkb(session, letter=data.get('Основной диагноз по МКБ'))[0]['Diag_id']

        ksg_and_koef = get_KSG_KOEF(
            session,
            date_start=data.get('Дата поступления'),
            date_end=data.get('Дата выписки'),
            patient_id=patient,
            diagnosis_id=diagnosis_id
        )

        evn_number = get_evn_number(session)
        try:
            if data.get('Вид госпитализации') == 'экстренная':
                evn_card = save_EVN(
                    session,
                    patient_id=patient,
                    patient_person_evn_id=search.get('data')[0]['PersonEvn_id'],
                    patient_server_id=search.get('data')[0]['Server_id'],
                    date_start=data.get('Дата поступления'),
                    time_start=data.get('Время поступления'),
                    numcard=evn_number.get('EvnPS_NumCard'),
                    type_hospitalization='1',
                    date_of_referral='',
                    number_of_referral='',
                    other_hosp='',
                    org_id='',
                    med_personal_id=med_personal_id,
                    med_staff_fact_id=med_staff_fact_id
                ) # тут может быть ошибка при пересечении случаев госпитализации с другими отделениями. Нужен обработчик ошибок
            elif data.get('Вид госпитализации') == 'плановая':
                evn_card = save_EVN(
                    session,
                    patient_id=patient,
                    patient_person_evn_id=search.get('data')[0]['PersonEvn_id'],
                    patient_server_id=search.get('data')[0]['Server_id'],
                    date_start=data.get('Дата поступления'),
                    time_start=data.get('Время поступления'),
                    numcard=evn_number.get('EvnPS_NumCard'),
                    type_hospitalization='2',
                    date_of_referral=data.get('Дата выдачи направления'),
                    number_of_referral=data.get('Номер направления'),
                    other_hosp='2',
                    org_id=data.get('Org_id'),
                    med_personal_id=med_personal_id,
                    med_staff_fact_id=med_staff_fact_id
                )
            else:
                evn_card = 'Ошибка на этапе вида госпитализации'
                print(evn_card)

            fourth_step = save_data(
                session,
                date_start=data.get('Дата поступления'),
                date_end=data.get('Дата выписки'),
                ksg_val=ksg_and_koef['KSG'],
                ksg_mes_tid=ksg_and_koef['Mes_tid'],
                ksg_mestarif_id=ksg_and_koef['MesTariff_id'],
                ksg_mes_old_usluga_complex_id=ksg_and_koef['MesOldUslugaComplex_id'],
                ksg_coeff=ksg_and_koef['KOEF'],
                patient_id=search['data'][0]['Person_id'],
                patient_person_evn_id=search['data'][0]['PersonEvn_id'],
                patient_server_id=search['data'][0]['Server_id'],
                time_start=data.get('Время поступления'),
                time_end=data.get('Время выписки'),
                evn_section_id=evn_card['EvnSection_id'],
                evn_section_pid=evn_card['EvnPS_id'],
                diag_id=diagnosis_id,
                med_personal_id=med_personal_id,
                med_staff_fact_id=med_staff_fact_id
            )

            template = create_template(session, evn_card['EvnSection_id'], med_staff_fact_id=med_staff_fact_id)

            update_treatment_evn_template(
                session,
                template_id=template['EvnXml_id'],
                text=f'{data.get("Консервативное")}\n{data.get("Оперативные вмешательства (операции), включая сведения об анестезиологическом пособии")}'
            )

            update_recommendation_evn_template(
                session,
                template_id=template['EvnXml_id'],
                text=f'{data.get("Наблюдение специалистов на амбулаторном этапе (явка на осмотр специалистов не позднее 7 дней после выписки из стационара в поликлинику по месту жительства)")}'
                     f'\n{data.get("Ограничение физических нагрузок")}\n{data.get("Уход за послеоперационной раной")}\n'
            )
            print(f'{data.get("Фамилия")} в ЕЦП загружен')
            with open('uploaded_stories.txt', 'a') as file:
                file.write(f'{datetime.now()}: {data.get("Фамилия")} в ЕЦП загружен')
        except Exception as error:
            print(f'{error} {data.get("Фамилия")}')
    except Exception as err:
        print(f'Ошибка: {err}')
        with open('errors.txt', 'a') as file:
            file.write(f'{datetime.now()}: {err}')
