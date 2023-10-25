import requests

from extract_document import name, surname, patronymic, birthday, date_start, date_end, time_start, time_end, \
    diagnosis_mkb
from settings import login, password
from single_digital_platform import entry, search_patient, get_KSG_KOEF, get_evn_number, save_EVN, save_data, mkb

session = requests.Session()

first_step = entry(session, login=login, password=password)

second_step = search_patient(session, name=name, surname=surname, patronymic=patronymic, birthday=birthday)

patient = second_step['data'][0]['Person_id']
diagnosis = mkb(session, letter=diagnosis_mkb)
third_step = get_KSG_KOEF(session, date_start=date_start, date_end=date_end, patient_id=patient, diagnosis_id=diagnosis)

evn_number = get_evn_number(session)

evn_card = save_EVN(
    session,
    patient_id=second_step['data'][0]['Person_id'],
    patient_person_evn_id=second_step['data'][0]['PersonEvn_id'],
    patient_server_id=second_step['data'][0]['Server_id'],
    date_start=date_start,
    time_start=time_start,
    numcard=evn_number['EvnPS_NumCard']
)


fourth_step = save_data(
    session,
    date_start=date_start,
    date_end=date_end,
    ksg_val=third_step['KSG'],
    ksg_mes_tid=third_step['Mes_tid'],
    ksg_mestarif_id=third_step['MesTariff_id'],
    ksg_mes_old_usluga_complex_id=third_step['MesOldUslugaComplex_id'],
    ksg_coeff=third_step['KOEF'],
    patient_id=second_step['data'][0]['Person_id'],
    patient_person_evn_id=second_step['data'][0]['PersonEvn_id'],
    patient_server_id=second_step['data'][0]['Server_id'],
    time_start=time_start,
    time_end=time_end,
    evn_section_id=evn_card['EvnSection_id'],
    evn_section_pid=evn_card['EvnPS_id']
)
