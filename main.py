import json

import requests


from settings import login, password, proxies
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
session = requests.Session()
session.proxies.update(proxies)

authorization = entry(session, login=login, password=password)

with open('patients/Юрошева.json', 'r') as file:
    data = json.load(file)

search = search_patient(
    session,
    name=data['name'],
    surname=data['surname'],
    patronymic=data['patronymic'].strip(','),
    birthday=data['birthday'],
)

patient = search['data'][0]['Person_id']

diagnosis_id = mkb(session, letter=data['icd_diagnosis'])[0]['Diag_id']

ksg_and_koef = get_KSG_KOEF(
    session,
    date_start=data['date_start'],
    date_end=data['date_end'],
    patient_id=patient,
    diagnosis_id=diagnosis_id
)

evn_number = get_evn_number(session)

evn_card = save_EVN(
    session,
    patient_id=search['data'][0]['Person_id'],
    patient_person_evn_id=search['data'][0]['PersonEvn_id'],
    patient_server_id=search['data'][0]['Server_id'],
    date_start=data['date_start'],
    time_start=data['time_start'],
    numcard=evn_number['EvnPS_NumCard']
)

fourth_step = save_data(
    session,
    date_start=data['date_start'],
    date_end=data['date_end'],
    ksg_val=ksg_and_koef['KSG'],
    ksg_mes_tid=ksg_and_koef['Mes_tid'],
    ksg_mestarif_id=ksg_and_koef['MesTariff_id'],
    ksg_mes_old_usluga_complex_id=ksg_and_koef['MesOldUslugaComplex_id'],
    ksg_coeff=ksg_and_koef['KOEF'],
    patient_id=search['data'][0]['Person_id'],
    patient_person_evn_id=search['data'][0]['PersonEvn_id'],
    patient_server_id=search['data'][0]['Server_id'],
    time_start=data['time_start'],
    time_end=data['time_end'],
    evn_section_id=evn_card['EvnSection_id'],
    evn_section_pid=evn_card['EvnPS_id'],
    diag_id=diagnosis_id
)

template = create_template(session, evn_card['EvnSection_id'])

update_treatment_evn_template(
    session,
    template_id=template['EvnXml_id'],
    text=data['treatment']
)

update_recommendation_evn_template(
    session,
    template_id=template['EvnXml_id'],
    text=data['recommendations']
)
