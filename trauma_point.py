from pprint import pprint
import json
import requests

from settings import proxies
from single_digital_platform import entry


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
    return response


def save_visit():

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'priority': 'u=1, i',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'EvnPL',
        'm': 'saveEvnVizitFromEMK',
    }

    data = {
        'ignoreCorrectPalliativeCareCheck': '1',
        'ignoreUslugaPayTypeCheck': '1',
        'ignoreUslugaToMesCheck': '1',
        'EvnVizitPL_IsTMK': '',
        'ignoreLpuSectionAge': '',
        'checkCVI': 'true',
        'ignoreDiagDeseaseTypeLink': '0',
        'diagDeseaseTypeLinkDate': '2024-06-30',
        'EvnVizitPL_id': '380101373118254',
        'form_saved': '0',
        'Person_id': '1453633',
        'EvnVizitPL_IsZNORemove': '',
        'lastZNO': '',
        'Server_id': '0',
        'PersonEvn_id': '380101025078840',
        'MedSpecClass_id': '79',
        'MedicalFormPersonDispPrescr_id': '',
        'IsDeleteSpecificCVI': '1',
        'EvnVizitPL_setDate': '30.06.2024',
        'EvnVizitPL_setTime': '16:21',
        'EvnVizitPL_IsPrimaryVizitAnnual': 'null',
        'LpuSection_id': '380101000015788',
        'MedStaffFact_id': '380101000010384',
        'MedStaffFact_id2': 'null',
        'MedStaffFact_id3': 'null',
        'MedStaffFact_sid': 'null',
        'TreatmentClass_id': '2',
        'VizitActiveType_id': 'null',
        'ServiceType_id': '6',
        'VizitClass_id': '1',
        'VizitType_id': '380101000000063',
        'MedOffice_id': 'null',
        'RiskLevel_id': 'null',
        'WellnessCenterAgeGroups_id': 'null',
        'Mes_id': 'null',
        'Eye_id': 'null',
        'MedicalCareKind_id': '6',
        'MesRegion_id': 'null',
        'UslugaComplex_uid': 'null',
        'DispClass_id': 'null',
        'EvnPLDisp_id': '',
        'PersonDisp_id': '',
        'LpuSectionProfile_id': '380101000000301',
        'PayType_id': '380101000000021',
        'PayContract_id': 'null',
        'PolisDMS_id': 'null',
        'ProfGoal_id': 'null',
        'PregnancyEvnVizitPL_Period': '',
        'Diag_id': '12978',
        'EvnInfectNotify_id': '',
        'Diag11_Code': 'null',
        'HeartFailureStage_54': 'null',
        'HeartFailureClass_55': 'null',
        'StenocardiaFuncClass_id': 'null',
        'PulmonaryHypertensionFuncClass_id': 'null',
        'OnkoLesionSide_id': 'null',
        'DeseaseType_id': '3',
        'DiagSetPhase_id': '1',
        'PainIntensity_id': 'null',
        'TumorStage_id': 'null',
        'ClinicalDiagnosis_140': '',
        'EvnVizitPL_IsZNO': '1',
        'RankinScale_id': 'null',
        'Diag_agid': 'null',
        'Diag_spid': 'null',
        'Diag_oid': 'null',
        'EvnVizitPL_BiopsyDate': '',
        'HealthKind_id': 'null',
        'RehabScale_id': 'null',
        'EvnVizitPL_IsRecoveryPotential': '1',
        'RehabType_id': 'null',
    }

    response = requests.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data).json()
    return response


session = requests.Session()
session.proxies.update(proxies)

authorization = entry(session, login='gimdkb_pretoriustl', password='Ptl026')

pprint(search_patients_ext6(
    session,
    surname='Молев',
    name='Тимофей',
    patronymic='Никитич',
    birthday='28.05.2011'
))

session.close()
