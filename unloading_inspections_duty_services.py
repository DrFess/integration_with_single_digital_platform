import json

import requests

from settings import proxies
from single_digital_platform import entry, get_evn_number
from read_xlsx import read_xlsx, search_diag_id, get_case_content, create_content_for_ECP


def search_patients_ext6(
        connect,
        surname: str,
        name: str,
        patronymic: str,
        birthday: str  # дата рождения в формате dd.mm.yyyy
):
    """Поиск пациента в ext6.js(поликлиника)"""

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
        'c': 'Person6E',
        'm': 'getPersonGrid',
    }

    data = {
        'start': '0',
        'limit': '100',
        'Double_ids': '[]',
        'Person_Surname': surname,
        'Person_Firname': name,
        'Person_Secname': patronymic,
        'Person_Birthday': birthday,
        'Address_Street': '',
        'Address_House': '',
        'PersonCard_Code': '',
        'Polis_Ser': '',
        'Polis_Num': '',
        'Person_Code': '',
        'AttachLpu_id': 'null',
        'Org_id': '10379',
        'showAll': '1',
        'dontShowUnknowns': '1',
        'page': '1',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data).json()
    return response.get('data')


def save_EVN_for_emergency(
        connect,
        med_personal_id: str,
        person_id: str,
        person_evn_id: str,
        server_id: str,
        evn_num_card: str,
        inspection_time: str,
        inspection_date: str,
        trauma_type: str,
        diag_id: str,
):
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
        'c': 'EvnPS',
        'm': 'saveEvnPS',
    }

    data = [
        ('MedPersonal_pid', med_personal_id),  # ID регистратора
        ('EvnDirection_Num', ''),
        ('LpuSection_did', ''),
        ('MedStaffFact_TFOMSCode', ''),
        ('EvnPS_IsPLAmbulance', '1'),
        ('LeaveType_fedid', ''),
        ('LpuSection_pid', '380101000006023'),  # ID травмпункта
        ('EvnDirection_setDate', ''),
        ('RepositoryObservData', '{}'),
        ('vizit_direction_control_check', '0'),
        ('ignoreEvnPSDoublesCheck', '0'),
        ('ignoreEvnPSTimeDeseaseCheck', '0'),
        ('ignoreEvnPSHemoDouble', '0'),
        ('ignoreEvnPSHemoLong', '0'),
        ('ignoreMorbusOnkoDrugCheck', '0'),
        ('ignoreCheckConciliumOnko', '0'),
        ('ignoreCheckMorbusOnko', '0'),
        ('ignoreDocumentsCheck', '0'),
        ('ignorePersonAgeByMedSpecCheck', '0'),
        ('AdditionalFields', '{}'),
        ('Person_IsUnknown', 'false'),
        ('EvnPS_id', ''),
        ('Lpu_id', ''),
        ('EvnDirectionHTM_id', ''),
        ('EvnDirectionExt_id', ''),
        ('DirType_id', ''),
        ('EvnDie_id', '0'),
        ('from', 'workplacepriem'),
        ('EvnDirection_id', '0'),
        ('EvnQueue_id', '0'),
        ('EvnLeave_id', '0'),
        ('LeaveType_id', '0'),
        ('EvnOtherLpu_id', '0'),
        ('EvnOtherSection_id', '0'),
        ('EvnOtherSectionBedProfile_id', '0'),
        ('EvnOtherStac_id', '0'),
        ('PrehospStatus_id', '0'),
        ('Person_id', person_id),  # из search_patient
        ('PersonEvn_id', person_evn_id),  # из search_patient
        ('Server_id', server_id),  # из search_patient
        ('EvnPS_IsZNO', '1'),
        ('EvnPS_IsZNORemove', ''),
        ('EvnSection_id', ''),
        ('EvnInfectNotifyPediculos_id', ''),
        ('PrimaryInspectionONMKPatient_id', ''),
        ('EvnInfectNotifyScabies_id', ''),
        ('MedPersona_sid', ''),
        ('MedPersona_tid', ''),
        ('EvnPS_IsCont', '1'),
        ('EvnPS_NumCard', evn_num_card),  # из save_EVN
        ('LpuSectionTransType_id', ''),
        ('PayType_id', '380101000000021'),  # ОМС const
        ('PayContract_id', ''),
        ('PolisDMS_id', ''),
        ('EvnPS_setDate', inspection_date),  # из карты
        ('EvnPS_setTime', inspection_time),  # из карты
        ('PrehospDirect_id', ''),
        ('EvnPS_IsWithoutDirection', '1'),
        ('Org_did', ''),
        ('DirScanFiles_id', ''),
        ('DirScanFiles_FilePath', ''),
        ('PrehospArrive_id', '1'),
        ('CmpCallCard_id', ''),
        ('Diag_did', ''),
        ('DiagValidityType_id', ''),
        ('DiagSetPhase_did', ''),
        ('EvnPS_PhaseDescr_did', ''),
        ('PrehospTraumaScale_Value', ''),
        ('ResultECG', ''),
        ('ScaleLams_id', ''),
        ('ScaleLams_Value', ''),
        ('EvnPS_IsImperHosp', '1'),
        ('EvnPS_IsShortVolume', '1'),
        ('EvnPS_IsWrongCure', '1'),
        ('EvnPS_IsDiagMismatch', '1'),
        ('PrehospType_id', '1'),
        ('EvnPS_HospCount', '1'),
        ('Okei_id', '100'),
        ('EvnPS_TimeDesease', ''),
        ('EvnPS_IsNeglectedCase', ''),
        ('PersonHeight_Height', ''),
        ('PersonWeight_Weight', ''),
        ('PersonVitalParam_SistolPress', ''),
        ('PersonVitalParam_DiastolPress', ''),
        ('PersonVitalParam_Temperature', ''),
        ('PersonVitalParam_BreathFrequency', ''),
        ('PersonVitalParam_Pulse', ''),
        ('PersonVitalParam_HeartFrequency', ''),
        ('RepositoryObserv_SpO2', ''),
        ('CovidType_id', ''),
        ('RepositoryObserv_FluorographyDate', ''),
        ('DiagConfirmType_id', ''),
        ('LungInjuryDegreeType_id', ''),
        ('PrehospTrauma_id', trauma_type),  # из карты (6-11), нужен список с кодами вида травм (бытовая, уличная и т.д.)
        ('Diag_eid', '13947'),  # ID диагноза вида травмы
        ('TraumaCircumEvnPS_Name', ''),
        ('TraumaCircumEvnPS_setDTDate', ''),
        ('TraumaCircumEvnPS_setDTTime', ''),
        ('EvnPS_IsUnlaw', '1'),
        ('EvnPS_IsUnport', ''),
        ('EntranceModeType_id', ''),
        ('MedStaffFact_pid', '380101000010384'),  # ID АРМ регистратора (врача)
        ('Diag_pid', diag_id),  # из карты. ID диагноза из БД
        ('DiagValidityType_id', ''),
        ('DiagSetPhase_pid', '1'),
        ('EvnPS_PhaseDescr_pid', ''),
        ('DeseaseType_id', ''),
        ('EPSPEF_OpenMorbusButton', 'Открытые заболевания'),
        ('ESCScaleRiskType_Name', ''),
        ('Pediculos_id', ''),
        ('EvnDiagPSPediculos_id', ''),
        ('isExamPediculosisScabies', '1'),
        ('isPediculos', '1'),
        ('PediculosDiag_id', ''),
        ('Pediculos_Sanitation_setDate', ''),
        ('Pediculos_Sanitation_setTime', ''),
        ('Scabies_id', ''),
        ('EvnDiagPSScabies_id', ''),
        ('isScabies', '1'),
        ('ScabiesDiag_id', ''),
        ('Scabies_Sanitation_setDate', ''),
        ('Scabies_Sanitation_setTime', ''),
        ('Pediculos_isPrint', ''),
        ('buttonPrint058', ''),
        ('EvnPS_CmpTltDate', ''),
        ('EvnPS_CmpTltTime', ''),
        ('ThrombolysisBSMP_58', ''),
        ('EvnPS_IsActive', '2'),
        ('TumorStage_id', ''),
        ('Diag_spid', ''),
        ('EvnPS_BiopsyDate', ''),
        ('FamilyContact_msgDate', ''),
        ('FamilyContact_msgTime', ''),
        ('FamilyContact_IsInfoAgree', ''),
        ('FamilyContact_FIO', ''),
        ('FamilyContact_Phone_Hidden', ''),
        ('FamilyContact_Phone', ''),
        ('FamilyContactPerson_id', ''),
        ('VologdaFamilyContact_FIO', ''),
        ('VologdaFamilyContact_Phone', ''),
        ('EvnPS_OutcomeDate', ''),
        ('EvnPS_OutcomeTime', ''),
        ('LeaveType_prmid', ''),
        ('LpuSection_eid', ''),
        ('EvnPSLpuSectionWard_id', ''),
        ('Bed_id', ''),
        ('NewLpuSectionBedProfile_id', ''),
        ('BedFund_setDate', ''),
        ('LpuSectionWard_id', ''),
        ('LpuSectionBedProfileLink_id', ''),
        ('PrehospWaifRefuseCause_id', ''),
        ('MesRegion_id', ''),
        ('MedicalCareFormType_id', ''),
        ('ResearchObservEmergencyReason_id', ''),
        ('LpuSectionProfile_id', ''),
        ('MedStaffFact_tid', ''),
        ('MedStaffFact_sid', ''),
        ('UslugaComplex_id', ''),
        ('ResultClass_id', ''),
        ('ResultDeseaseType_id', ''),
        ('ResultDeseaseType_fedid', ''),
        ('EvnPS_PatientRefuse', '1'),
        ('DiagSetPhase_aid', ''),
        ('CmpCallCard_EmgTeamComm', ''),
        ('EvnPS_IsWaif', '1'),
        ('PrehospWaifArrive_id', ''),
        ('PrehospWaifReason_id', ''),
    ]

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data).json()
    return response


def create_service(connect, evn_ps_id: str):
    """Создаёт случай услуги"""

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
        'c': 'EvnSection',
        'm': 'getSectionPriemData',
    }

    data = {
        'EvnPS_id': evn_ps_id,
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data).json()
    return response


def save_service_case(
        connect,
        person_id: str,
        server_id: str,
        person_evn_id: str,
        case_pid: str,
        evn_ps_id: str,
        case_id: str,
        case_rid: str,
        med_staff_fact_id: str,
        case_date: str,  # дата в формате dd.mm.yyyy
        med_personal_id: str,
        case_time: str,  # время в формате hh:mm
):
    """Сохранение данных случая"""

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
        'c': 'EvnUsluga',
        'm': 'saveEvnUslugaCommon',
    }

    data = {
        'EvnUslugaCommon_pid': case_pid,
        'Lpu_uid': '',
        'PersonDisp_ids': '[null]',
        'EvnUslugaCommon_Price': '0',
        'EvnUslugaCommon_Summa': '0.00',
        'ignoreParentEvnDateCheck': '0',
        'accessType': '',
        'EvnClass_SysNick': 'EvnUslugaCommon',
        'EvnUslugaCommon_id': case_id,
        'EvnUslugaCommon_rid': case_rid,
        'Evn_id': evn_ps_id,
        'EvnDirection_id': '0',
        'MedPersonal_id': med_personal_id,
        'Morbus_id': '-1',
        'Person_id': person_id,
        'PersonEvn_id': person_evn_id,
        'Server_id': server_id,
        'EvnUslugaCommon_setDate': case_date,
        'EvnUslugaCommon_setTime': case_time,
        'EvnUslugaCommon_disDate': case_date,
        'EvnUslugaCommon_disTime': case_time,
        'UslugaPlace_id': '1',
        'LpuSection_uid': '380101000006023',
        'LpuSectionProfile_id': '380101000000344',
        'MedSpecOms_id': '',
        'MedStaffFact_id': med_staff_fact_id,
        'MedStaffFact_sid': '',
        'PayType_id': '380101000000021',
        'PayContract_id': '',
        'PolisDMS_id': '',
        'EvnPrescr_id': '',
        'UslugaCategory_id': '4',
        'UslugaComplex_id': '206696',  # id первичного осмотра травматолога (сюда подставлять id осмотров других специалистов)
        'UslugaMedType_id': '',
        'UslugaComplexTariff_id': '',
        'DiagSetClass_id': '',
        'Diag_id': '',
        'PersonDisp_id': '',
        'EvnUslugaCommon_Kolvo': '1',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data).json()
    return response


def create_template_case(connect, evn_ps_id: str, server_id: str, med_staff_fact_id: str):
    """Создаёт шаблон осмотра"""
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
        'c': 'EvnXml',
        'm': 'createEmpty',
    }

    data = {
        'Evn_id': evn_ps_id,
        'XmlType_id': '4',
        'EvnClass_id': '22',
        'EvnClass_SysNick': 'EvnUslugaCommon',
        'Server_id': server_id,
        'MedStaffFact_id': med_staff_fact_id,
        'XmlTemplate_id': '380101000599419',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data).json()
    return response


def upload_template(connect, evn_xml_id: str, chapter: str, text: str):
    """Заполнение разделов шаблона"""

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
        'c': 'EvnXml',
        'm': 'updateContent',
    }

    data = {
        'EvnXml_id': evn_xml_id,
        'name': chapter,  # название блока (жалобы). Нужен список всех имен разделов
        'value': f'<p>{text}</p>',
        'isHTML': '1',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data).json()
    return response


def generate_EDS(connect, registry_object_id: str, med_staff_fact_id: str):
    """Создаёт документ с электронной подписью"""
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
        'c': 'EMD',
        'm': 'generateEMDRegistry',
    }

    data = {
        'EMDRegistry_ObjectName': 'EvnXml',
        'EMDRegistry_ObjectID': registry_object_id,
        'MedStaffFact_id': med_staff_fact_id,
        'EMDCertificate_id': '21355',  # id сертификата врача, вероятнее всего у каждого врача свой.
        'isDocArray': 'false',
        'isPreview': '',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data).json()
    return response


def save_EDS(connect, registry_object_id: str, emd_version_id: str, med_staff_fact_id: str, signature_hash: str):
    """Сохранение ЭЦП (не вызывать! Доработать Signatures_SignedData)"""
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
        'c': 'EMD',
        'm': 'saveEMDSignatures',
    }

    data = {
        'EMDRegistry_ObjectName': 'EvnXml',
        'EMDRegistry_ObjectID': registry_object_id,
        'EMDDocumentTypeLocal_id': '100047',
        'EMDVersion_id': emd_version_id,
        'Signatures_Hash': signature_hash,
        'Signatures_SignedData': 'MIIa7wYJKoZIhvcNAQcCoIIa4DCCGtwCAQExDDAKBggqhQMHAQECAjALBgkqhkiG9w0BBwGgghat\TwL2QhD47nM09OMzYtsYVxrXEk/B\r\npbY=',
        'EMDCertificate_id': '21355',
        'EMDPersonRole_id': '1',
        'signType': 'cryptopro',
        'isMOSign': '',
        'MedStaffFact_id': med_staff_fact_id,
        'PersonWork_id': '',
        'LpuSection_id': '380101000006023',
        'MedService_id': '',
        'isDocArray': 'false',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data).json()
    return response


with open('doctors.json', 'r') as file:
    doctors = json.load(file)

chapters_list = ['complaint', 'anamnesmorbi', 'localstatus', 'research', 'diagnos', 'recommendations']

session = requests.Session()
session.proxies.update(proxies)

patients = read_xlsx('daily_report/Uslugi.xlsx')
for patient_info in patients:
    case_number = patient_info[0].split(' ')[0]
    content_data = create_content_for_ECP(get_case_content(case_number))
    if patient_info[7].split(' ')[0] == 'Преториус' or patient_info[7].split(' ')[0] == 'Дегтярев':
        try:
            doctor_surname = patient_info[7].split(' ')[0]
            login = doctors.get(doctor_surname).get('login')
            password = doctors.get(doctor_surname).get('password')
            med_personal_id = doctors.get(doctor_surname).get('MedPersonal_id')
            med_staff_fact_id = doctors.get(doctor_surname).get('MedStaffFact_id')

            authorization = entry(session, login=login, password=password)

            patient_surname = patient_info[2].split(' ')[0]
            patient_name = patient_info[2].split(' ')[1]
            patient_patronymic = patient_info[2].split(' ')[2]
            patient_birthday = patient_info[4]

            patient = search_patients_ext6(
                        session,
                        name=patient_name,
                        surname=patient_surname,
                        patronymic=patient_patronymic,
                        birthday=patient_birthday,
                    )

            person_id = patient[0].get('Person_id')
            person_evn_id = patient[0].get('PersonEvn_id')
            server_id = patient[0].get('Server_id')
            evn_num_card = get_evn_number(session).get('EvnPS_NumCard')

            case_inspection_time = patient_info[10]
            case_diag_id = search_diag_id(patient_info[12].split(' ')[0])
            inspection_date = content_data.get('date')

            emergency_card = save_EVN_for_emergency(
                session,
                med_personal_id=med_personal_id,
                person_id=person_id,
                person_evn_id=person_evn_id,
                server_id=server_id,
                evn_num_card=evn_num_card,
                inspection_date=inspection_date,
                inspection_time=case_inspection_time,
                trauma_type='6',  # поменять
                diag_id=case_diag_id,
            )

            evn_ps_id = emergency_card.get('EvnPS_id')
            evn_section_priem_id = emergency_card.get('EvnSectionPriem_id')

            service_case = create_service(
                session,
                evn_ps_id=evn_ps_id
            )
            evn_section_id = service_case[0].get('EvnSection_id')

            first_save_data_case = save_service_case(
                session,
                person_id=person_id,
                server_id=server_id,
                person_evn_id=person_evn_id,
                case_pid=evn_section_id,
                evn_ps_id=evn_ps_id,
                case_id='0',
                case_rid='0',
                med_staff_fact_id=med_staff_fact_id,
                med_personal_id=med_personal_id,
                case_date=inspection_date,
                case_time=case_inspection_time
            )

            evn_usluga_common_id = first_save_data_case.get('EvnUslugaCommon_id')
            evn_rid = first_save_data_case.get('Evn_rid')

            template_case_create = create_template_case(
                session,
                evn_ps_id=evn_usluga_common_id,
                server_id=server_id,
                med_staff_fact_id=med_staff_fact_id
            )
            evn_xml_id = template_case_create.get('EvnXml_id')

            for chapter in chapters_list:
                template_case = upload_template(
                    session,
                    evn_xml_id=evn_xml_id,
                    chapter=chapter,
                    text=content_data.get(chapter),
                )

            second_save_data_case = save_service_case(
                session,
                evn_ps_id=evn_ps_id,
                server_id=server_id,
                person_id=person_id,
                person_evn_id=person_evn_id,
                case_pid='',
                case_id=evn_usluga_common_id,
                case_rid=evn_section_id,
                med_staff_fact_id=med_staff_fact_id,
                case_date=inspection_date,
                med_personal_id=med_personal_id,
                case_time=case_inspection_time,
            )
            #
            # electronic_digital_signature = generate_EDS(
            #     session,
            #     registry_object_id=evn_xml_id,
            #     med_staff_fact_id=med_staff_fact_id
            # )
            # emd_version_id = electronic_digital_signature.get('toSign')[0].get('EMDVersion_id')
            # signature_hash = electronic_digital_signature.get('toSign')[0].get('hashBase64')
        except Exception as e:
            print(e)
session.close()
