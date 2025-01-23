from pprint import pprint
import urllib.parse
import requests

from settings import proxies
from single_digital_platform import entry


def get_full_person_info(connect, person_id: str) -> dict:
    """получает персональные данные по person_id"""

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'priority': 'u=1, i',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'Person',
        'm': 'getPersonEditWindow',
    }

    data = {
        'RegistryType_id': '',
        'person_id': person_id,
        'server_id': '0',
        'attrObjects': '[{"object":"PersonEditWindow","identField":"Person_id"}]',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data).json()
    return response


def check_snils(connect, person_id: str, snils: str) -> dict:
    """Проверяет не принадлежит ли номер СНИЛС кому-то уже"""

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'priority': 'u=1, i',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'Person',
        'm': 'checkSnilsDoubles',
    }

    data = {
        'Person_SNILS': snils,
        'Person_id': person_id,
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data).json()
    return response


def save_person_info(connect, old_values: str, new_values: str):
    """сохраняет персональные данные"""

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'priority': 'u=1, i',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'Person',
        'm': 'savePersonEditWindow',
    }

    data = f'oldValues={old_values}mode=edit&{new_values}'

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data)
    if response.status_code == 200:
        return "Done!"
    else:
        return "Failed!"


session = requests.Session()
session.proxies.update(proxies)

authorization = entry(session, login='daa87', password='Daa026')

person_info = get_full_person_info(session, '3419648')
pprint(person_info)

old_values = urllib.parse.urlencode(person_info[0], doseq=True)  # словарь в unicode строку
old_values = urllib.parse.quote(old_values, safe='')  # строку в utf-8 строку
pprint(old_values)

person_info[0]['Person_SNILS'] = '202-853-761-50'
person_info[0]['Person_SNILS_Hidden'] = '20285376150'

pprint(person_info)

new_values = urllib.parse.urlencode(person_info[0], doseq=True)
pprint(new_values)

pprint(check_snils(session, '3419648', '202-853-761-50'))
print(save_person_info(session, old_values, new_values))
# text = 'oldValues=DeputyPerson_Fio%3D%26BDZ_Guid%3D%26Polis_Guid%3D%26PersonMedWorker%3D%26PersonWithReward%3D%26PersonMedWorkerLpuNick%3D%26Person_IsInErz%3D%26Server_pid%3D38%26polisCloseCause%3D%26action%3Dsave%26Servers_ids%3D%255B101%255D%26Person_identDT%3D%26PersonIdentState_id%3D%26PersonRequestDataStatus_id%3D%26Lpu_name%3D%26LpuRegion_name%3D%26PersonCard_begDate%3D%26BDZ_id%3D%26Person_IsFedLgot%3D0%26Polis_CanAdded%3D0%26PersonEmployment_id%3D%26PersonEduLevel_id%3D%26isNeedFRMRSync%3D0%26Person_SurName%3D%25D0%25A1%25D0%25B5%25D0%25BD%25D0%25BE%25D1%2582%25D1%2580%25D1%2583%25D1%2581%25D0%25BE%25D0%25B2%26Person_FirName%3D%25D0%259C%25D0%25B8%25D1%2585%25D0%25B0%25D0%25B8%25D0%25BB%26Person_SecName%3D%25D0%2598%25D0%25B3%25D0%25BE%25D1%2580%25D0%25B5%25D0%25B2%25D0%25B8%25D1%2587%26Person_BirthDay%3D31.05.2014%26PersonPhone_VerifiedPhone%3D%26PersonPhone_Phone_Hidden%3D%26PersonPhone_Phone%3D(902)-566-85-55%26PersonSex_id%3D1%26Person_Comment%3D%26PersonState_IsSnils%3D%26Person_SNILS_Hidden%3D%26Person_SNILS%3D%26SocStatus_id%3D380101000000040%26DateSetSnilsStatus%3D%26EducationLevel_id%3D%26UAddress_Zip%3D664075%26UKLCountry_id%3D643%26UKLRGN_id%3D38%26UKLRGNSocr_id%3D%26UKLSubRGN_id%3D%26UKLSubRGNSocr_id%3D%26UKLCity_id%3D2869%26UKLCitySocr_id%3D%26UPersonSprTerrDop_id%3D%26UKLTown_id%3D%26UKLTownSocr_id%3D%26UKLStreet_id%3D293002%26UKLStreetSocr_id%3D%26UAddress_House%3D128%26UAddress_Corpus%3D%26UAddress_Flat%3D13%26UAddress_Room%3D%26UAddressSpecObject_id%3D%26UAddressSpecObject_Value%3D%26UAddress_Address%3D664075%252C%2520%25D0%25A0%25D0%259E%25D0%25A1%25D0%25A1%25D0%2598%25D0%25AF%252C%2520%25D0%2598%25D0%25A0%25D0%259A%25D0%25A3%25D0%25A2%25D0%25A1%25D0%259A%25D0%2590%25D0%25AF%2520%25D0%259E%25D0%2591%25D0%259B%252C%2520%25D0%2593%2520%25D0%2598%25D0%25A0%25D0%259A%25D0%25A3%25D0%25A2%25D0%25A1%25D0%259A%252C%2520%25D0%2594%25D0%2590%25D0%259B%25D0%25AC%25D0%259D%25D0%2595%25D0%2592%25D0%259E%25D0%25A1%25D0%25A2%25D0%259E%25D0%25A7%25D0%259D%25D0%2590%25D0%25AF%2520%25D0%25A3%25D0%259B%252C%2520%25D0%25B4.%2520128%252C%2520%25D0%25BA%25D0%25B2.%252013%26UAddress_AddressCacheObjectid%3D%26UAddress_HouseObjectGUID%3D%26U_address_not_found%3D0%26U_LocalityId%3D%26UAddress_AddressText%3D664075%252C%2520%25D0%25A0%25D0%259E%25D0%25A1%25D0%25A1%25D0%2598%25D0%25AF%252C%2520%25D0%2598%25D0%25A0%25D0%259A%25D0%25A3%25D0%25A2%25D0%25A1%25D0%259A%25D0%2590%25D0%25AF%2520%25D0%259E%25D0%2591%25D0%259B%252C%2520%25D0%2593%2520%25D0%2598%25D0%25A0%25D0%259A%25D0%25A3%25D0%25A2%25D0%25A1%25D0%259A%252C%2520%25D0%2594%25D0%2590%25D0%259B%25D0%25AC%25D0%259D%25D0%2595%25D0%2592%25D0%259E%25D0%25A1%25D0%25A2%25D0%259E%25D0%25A7%25D0%259D%25D0%2590%25D0%25AF%2520%25D0%25A3%25D0%259B%252C%2520%25D0%25B4.%2520128%252C%2520%25D0%25BA%25D0%25B2.%252013%26UAddress_begDate%3D%26PAddress_Zip%3D664075%26PKLCountry_id%3D643%26PKLRGN_id%3D38%26PKLRGNSocr_id%3D%26PKLSubRGN_id%3D%26PKLSubRGNSocr_id%3D%26PKLCity_id%3D2869%26PKLCitySocr_id%3D%26PPersonSprTerrDop_id%3D%26PKLTown_id%3D%26PKLTownSocr_id%3D%26PKLStreet_id%3D293002%26PKLStreetSocr_id%3D%26PAddress_House%3D128%26PAddress_Corpus%3D%26PAddress_Flat%3D13%26PAddress_Room%3D%26PAddressSpecObject_id%3D%26PAddressSpecObject_Value%3D%26PAddress_Address%3D664075%252C%2520%25D0%25A0%25D0%259E%25D0%25A1%25D0%25A1%25D0%2598%25D0%25AF%252C%2520%25D0%2598%25D0%25A0%25D0%259A%25D0%25A3%25D0%25A2%25D0%25A1%25D0%259A%25D0%2590%25D0%25AF%2520%25D0%259E%25D0%2591%25D0%259B%252C%2520%25D0%2593%2520%25D0%2598%25D0%25A0%25D0%259A%25D0%25A3%25D0%25A2%25D0%25A1%25D0%259A%252C%2520%25D0%2594%25D0%2590%25D0%259B%25D0%25AC%25D0%259D%25D0%2595%25D0%2592%25D0%259E%25D0%25A1%25D0%25A2%25D0%259E%25D0%25A7%25D0%259D%25D0%2590%25D0%25AF%2520%25D0%25A3%25D0%259B%252C%2520%25D0%25B4.%2520128%252C%2520%25D0%25BA%25D0%25B2.%252013%26PAddress_AddressCacheObjectid%3D%26PAddress_HouseObjectGUID%3D%26PersonChild_id%3D%26PAddress_AddressText%3D664075%252C%2520%25D0%25A0%25D0%259E%25D0%25A1%25D0%25A1%25D0%2598%25D0%25AF%252C%2520%25D0%2598%25D0%25A0%25D0%259A%25D0%25A3%25D0%25A2%25D0%25A1%25D0%259A%25D0%2590%25D0%25AF%2520%25D0%259E%25D0%2591%25D0%259B%252C%2520%25D0%2593%2520%25D0%2598%25D0%25A0%25D0%259A%25D0%25A3%25D0%25A2%25D0%25A1%25D0%259A%252C%2520%25D0%2594%25D0%2590%25D0%259B%25D0%25AC%25D0%259D%25D0%2595%25D0%2592%25D0%259E%25D0%25A1%25D0%25A2%25D0%259E%25D0%25A7%25D0%259D%25D0%2590%25D0%25AF%2520%25D0%25A3%25D0%259B%252C%2520%25D0%25B4.%2520128%252C%2520%25D0%25BA%25D0%25B2.%252013%26PAddress_begDate%3D%26BAddress_Zip%3D%26BKLCountry_id%3D%26BKLRGN_id%3D%26BKLRGNSocr_id%3D%26BKLSubRGN_id%3D%26BKLSubRGNSocr_id%3D%26BKLCity_id%3D%26BKLCitySocr_id%3D%26BPersonSprTerrDop_id%3D%26BKLTown_id%3D%26BKLTownSocr_id%3D%26BKLStreet_id%3D%26BKLStreetSocr_id%3D%26BAddress_House%3D%26BAddress_Corpus%3D%26BAddress_Flat%3D%26BAddress_Room%3D%26BAddressSpecObject_id%3D%26BAddressSpecObject_Value%3D%26BAddress_Address%3D%26BAddress_AddressCacheObjectid%3D%26BAddress_HouseObjectGUID%3D%26BAddress_AddressText%3D%26OMSSprTerr_id%3D380101000000038%26PolisType_id%3D4%26PolisFormType_id%3D%26Federal_Num%3D3894589718000206%26Polis_FormNum%3D%26OrgSMO_id%3D380101000000013%26Polis_begDate%3D02.09.2014%26Polis_endDate%3D%26Person_syncDT%3D%26rzn_comment%3D%26Person_Lpu_id%3D%26Person_Lpu%3D%26Person_Lpu_Region%3D%26DocumentType_id%3D3%26Document_Ser%3DIII-%25D0%25A1%25D0%25A2%26Document_Num%3D599841%26OrgDep_id%3D%26OrgDep_Text%3D%26Document_begDate%3D07.06.2014%26OrgDep_Code%3D%26KLCountry_id%3D643%26LegalStatusVZN_id%3D%26PersonLatinFIO_Auto%3DSENOTRUSOV%2520MI%25D0%25A5AIL%2520IGOREVICH%26PersonLatinFIO_SurName%3D%26PersonLatinFIO_FirName%3D%26PersonLatinFIO_SecName%3D%26Org_id%3D380101000007831%26OrgUnion_id%3D%26Post_id%3D%26Employment_id%3D%26OnkoCard_Num%3D%26OnkoCard_DateBeg%3D%26OnkoOccupationClass_id%3D%26Person_deadDT%3D%26Person_closeDT%3D%26ResidPlace_id%3D%26PersonSprTerrDop_id%3D%26PersonChild_IsBadLiving%3D%26PersonChild_IsSleepAlone%3D%26PersonChild_IsNoMedical%3D%26PersonChild_IsSaunaVisited%3D%26PersonChild_IsMotherOVDRegistered%3D%26PersonChild_IsLeftWithStrangers%3D%26PersonChild_IsManyChild%3D%26PersonChild_IsBad%3D%26PersonChild_IsIncomplete%3D%26PersonChild_IsTutor%3D%26PersonChild_IsMigrant%3D%26PersonChild_IsOftenMigrant%3D%26PersonChildDetails_IsPoor%3D%26PersonChild_IsNoParentalRightsBefore%3D%26PersonChild_IsOtherSocials%3D%26PersonChildDetails_IsNoParent%3D%26PersonChildDetails_IsArmedConflictVictim%3D%26PersonChildDetails_IsEcologyDisasterVictim%3D%26PersonChildDetails_IsDisasterVictim%3D%26PersonChildDetails_IsExtremeConditions%3D%26PersonChildDetails_IsViolenceVictim%3D%26PersonChildDetails_IsDeviamtSchool%3D%26PersonChildDetails_IsNeedSpecialEducation%3D%26PersonChildDetails_IsBehavioralProblems%3D%26PersonChildDetails_IsCircumstancesVictim%3D%26HealthKind_id%3D%26PersonChild_IsYoungMother%3D%26PersonChild_CountChild%3D%26PersonChild_IsInvalid%3D%26HealthAbnorm_id%3D%26HealthAbnormVital_id%3D%26Diag_id%3D%26DeputyType_id%3D0%26DeputyKind_id%3D%26DeputyOrg_id%3D%26DeputyPerson_id%3D%26DocumentAuthority_id%3D%26DocumentDeputy_Ser%3D%26DocumentDeputy_Num%3D%26DocumentDeputy_Issue%3D%26DocumentDeputy_begDate%3D%26PersonSocCardNum_SocCardNum%3D%26PersonRefuse_IsRefuse%3D%26Person_IsNotINN%3D1%26PersonInn_Inn%3D%26PersonInfo_isLocatedSocServiceOrg%3D%26PersonFamilyStatus_IsMarried%3D%26FamilyStatus_id%3D%26PersonChildExist_IsChild%3D%26PersonCarExist_IsCar%3D%26Ethnos_id%3D%26NationalityStatus_IsTwoNation%3Dfalse%26Person_IsUnknown%3Dfalse%26Person_IsAnonym%3Dfalse&mode=edit&Server_id=0&PostNew=&OrgUnionNew=&Polis_Ser=&Polis_Num=&Person_id=2662783&identParams=&DeputyPerson_Fio=&BDZ_Guid=&Polis_Guid=&PersonMedWorker=&PersonWithReward=&PersonMedWorkerLpuNick=&Person_IsInErz=&Server_pid=38&polisCloseCause=&action=save&Servers_ids=%5B101%5D&Person_identDT=&PersonIdentState_id=&PersonRequestDataStatus_id=&Lpu_name=&LpuRegion_name=&PersonCard_begDate=&BDZ_id=&Person_IsFedLgot=0&Polis_CanAdded=0&PersonEmployment_id=&PersonEduLevel_id=&isNeedFRMRSync=0&Person_SurName=%D0%A1%D0%B5%D0%BD%D0%BE%D1%82%D1%80%D1%83%D1%81%D0%BE%D0%B2&Person_FirName=%D0%9C%D0%B8%D1%85%D0%B0%D0%B8%D0%BB&Person_SecName=%D0%98%D0%B3%D0%BE%D1%80%D0%B5%D0%B2%D0%B8%D1%87&Person_BirthDay=31.05.2014&PersonPhone_VerifiedPhone=&PersonPhone_Phone_Hidden=&PersonPhone_Phone=(902)-566-85-55&PersonSex_id=1&Person_Comment=&PersonState_IsSnils=&Person_SNILS_Hidden=18203544748&Person_SNILS=182-035-447-48&SocStatus_id=380101000000040&DateSetSnilsStatus=&EducationLevel_id=&UAddress_Zip=664075&UKLCountry_id=643&UKLRGN_id=38&UKLRGNSocr_id=&UKLSubRGN_id=&UKLSubRGNSocr_id=&UKLCity_id=2869&UKLCitySocr_id=&UPersonSprTerrDop_id=&UKLTown_id=&UKLTownSocr_id=&UKLStreet_id=293002&UKLStreetSocr_id=&UAddress_House=128&UAddress_Corpus=&UAddress_Flat=13&UAddress_Room=&UAddressSpecObject_id=&UAddressSpecObject_Value=&UAddress_Address=664075%2C%20%D0%A0%D0%9E%D0%A1%D0%A1%D0%98%D0%AF%2C%20%D0%98%D0%A0%D0%9A%D0%A3%D0%A2%D0%A1%D0%9A%D0%90%D0%AF%20%D0%9E%D0%91%D0%9B%2C%20%D0%93%20%D0%98%D0%A0%D0%9A%D0%A3%D0%A2%D0%A1%D0%9A%2C%20%D0%94%D0%90%D0%9B%D0%AC%D0%9D%D0%95%D0%92%D0%9E%D0%A1%D0%A2%D0%9E%D0%A7%D0%9D%D0%90%D0%AF%20%D0%A3%D0%9B%2C%20%D0%B4.%20128%2C%20%D0%BA%D0%B2.%2013&UAddress_AddressCacheObjectid=&UAddress_HouseObjectGUID=&U_address_not_found=0&U_LocalityId=&UAddress_AddressText=664075%2C%20%D0%A0%D0%9E%D0%A1%D0%A1%D0%98%D0%AF%2C%20%D0%98%D0%A0%D0%9A%D0%A3%D0%A2%D0%A1%D0%9A%D0%90%D0%AF%20%D0%9E%D0%91%D0%9B%2C%20%D0%93%20%D0%98%D0%A0%D0%9A%D0%A3%D0%A2%D0%A1%D0%9A%2C%20%D0%94%D0%90%D0%9B%D0%AC%D0%9D%D0%95%D0%92%D0%9E%D0%A1%D0%A2%D0%9E%D0%A7%D0%9D%D0%90%D0%AF%20%D0%A3%D0%9B%2C%20%D0%B4.%20128%2C%20%D0%BA%D0%B2.%2013&UAddress_begDate=&PAddress_Zip=664075&PKLCountry_id=643&PKLRGN_id=38&PKLRGNSocr_id=&PKLSubRGN_id=&PKLSubRGNSocr_id=&PKLCity_id=2869&PKLCitySocr_id=&PPersonSprTerrDop_id=&PKLTown_id=&PKLTownSocr_id=&PKLStreet_id=293002&PKLStreetSocr_id=&PAddress_House=128&PAddress_Corpus=&PAddress_Flat=13&PAddress_Room=&PAddressSpecObject_id=&PAddressSpecObject_Value=&PAddress_Address=664075%2C%20%D0%A0%D0%9E%D0%A1%D0%A1%D0%98%D0%AF%2C%20%D0%98%D0%A0%D0%9A%D0%A3%D0%A2%D0%A1%D0%9A%D0%90%D0%AF%20%D0%9E%D0%91%D0%9B%2C%20%D0%93%20%D0%98%D0%A0%D0%9A%D0%A3%D0%A2%D0%A1%D0%9A%2C%20%D0%94%D0%90%D0%9B%D0%AC%D0%9D%D0%95%D0%92%D0%9E%D0%A1%D0%A2%D0%9E%D0%A7%D0%9D%D0%90%D0%AF%20%D0%A3%D0%9B%2C%20%D0%B4.%20128%2C%20%D0%BA%D0%B2.%2013&PAddress_AddressCacheObjectid=&PAddress_HouseObjectGUID=&PersonChild_id=&PAddress_AddressText=664075%2C%20%D0%A0%D0%9E%D0%A1%D0%A1%D0%98%D0%AF%2C%20%D0%98%D0%A0%D0%9A%D0%A3%D0%A2%D0%A1%D0%9A%D0%90%D0%AF%20%D0%9E%D0%91%D0%9B%2C%20%D0%93%20%D0%98%D0%A0%D0%9A%D0%A3%D0%A2%D0%A1%D0%9A%2C%20%D0%94%D0%90%D0%9B%D0%AC%D0%9D%D0%95%D0%92%D0%9E%D0%A1%D0%A2%D0%9E%D0%A7%D0%9D%D0%90%D0%AF%20%D0%A3%D0%9B%2C%20%D0%B4.%20128%2C%20%D0%BA%D0%B2.%2013&PAddress_begDate=&BAddress_Zip=&BKLCountry_id=&BKLRGN_id=&BKLRGNSocr_id=&BKLSubRGN_id=&BKLSubRGNSocr_id=&BKLCity_id=&BKLCitySocr_id=&BPersonSprTerrDop_id=&BKLTown_id=&BKLTownSocr_id=&BKLStreet_id=&BKLStreetSocr_id=&BAddress_House=&BAddress_Corpus=&BAddress_Flat=&BAddress_Room=&BAddressSpecObject_id=&BAddressSpecObject_Value=&BAddress_Address=&BAddress_AddressCacheObjectid=&BAddress_HouseObjectGUID=&BAddress_AddressText=&OMSSprTerr_id=380101000000038&PolisType_id=4&PolisFormType_id=&Federal_Num=3894589718000206&Polis_FormNum=&OrgSMO_id=380101000000013&Polis_begDate=02.09.2014&Polis_endDate=&Person_syncDT=&rzn_comment=&Person_Lpu_id=&Person_Lpu=&Person_Lpu_Region=&DocumentType_id=3&Document_Ser=III-%D0%A1%D0%A2&Document_Num=599841&OrgDep_id=&OrgDep_Text=&Document_begDate=07.06.2014&OrgDep_Code=&KLCountry_id=643&LegalStatusVZN_id=&PersonLatinFIO_Auto=SENOTRUSOV%20MI%D0%A5AIL%20IGOREVICH&PersonLatinFIO_SurName=&PersonLatinFIO_FirName=&PersonLatinFIO_SecName=&Org_id=380101000007831&OrgUnion_id=&Post_id=&Employment_id=&OnkoCard_Num=&OnkoCard_DateBeg=&OnkoOccupationClass_id=&Person_deadDT=&Person_closeDT=&ResidPlace_id=&PersonSprTerrDop_id=&PersonChild_IsBadLiving=&PersonChild_IsSleepAlone=&PersonChild_IsNoMedical=&PersonChild_IsSaunaVisited=&PersonChild_IsMotherOVDRegistered=&PersonChild_IsLeftWithStrangers=&PersonChild_IsManyChild=&PersonChild_IsBad=&PersonChild_IsIncomplete=&PersonChild_IsTutor=&PersonChild_IsMigrant=&PersonChild_IsOftenMigrant=&PersonChildDetails_IsPoor=&PersonChild_IsNoParentalRightsBefore=&PersonChild_IsOtherSocials=&PersonChildDetails_IsNoParent=&PersonChildDetails_IsArmedConflictVictim=&PersonChildDetails_IsEcologyDisasterVictim=&PersonChildDetails_IsDisasterVictim=&PersonChildDetails_IsExtremeConditions=&PersonChildDetails_IsViolenceVictim=&PersonChildDetails_IsDeviamtSchool=&PersonChildDetails_IsNeedSpecialEducation=&PersonChildDetails_IsBehavioralProblems=&PersonChildDetails_IsCircumstancesVictim=&HealthKind_id=&PersonChild_IsYoungMother=&PersonChild_CountChild=&PersonChild_IsInvalid=&HealthAbnorm_id=&HealthAbnormVital_id=&Diag_id=&DeputyType_id=0&DeputyKind_id=&DeputyOrg_id=&DeputyPerson_id=&DocumentAuthority_id=&DocumentDeputy_Ser=&DocumentDeputy_Num=&DocumentDeputy_Issue=&DocumentDeputy_begDate=&PersonSocCardNum_SocCardNum=&PersonRefuse_IsRefuse=&Person_IsNotINN=1&PersonInn_Inn=&PersonInfo_isLocatedSocServiceOrg=&PersonFamilyStatus_IsMarried=&FamilyStatus_id=&PersonChildExist_IsChild=&PersonCarExist_IsCar=&Ethnos_id='