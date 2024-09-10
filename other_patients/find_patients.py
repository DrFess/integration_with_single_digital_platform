import gspread


def get_patients_from_other_departments() -> list:
    gs = gspread.service_account(filename='/Users/aleksejdegtarev/PycharmProjects/integration_with_single_digital_platform/jsonS/access.json')
    sh = gs.open_by_key('1feNhDOpE41gwPwuvtW_V5kZH2hFSt9qc8gZvmoH2UIE')
    worksheet = sh.get_worksheet_by_id(1881810333)

    return worksheet.get()


def get_patients_emergency_room() -> list:
    gs = gspread.service_account(filename='/Users/aleksejdegtarev/PycharmProjects/integration_with_single_digital_platform/jsonS/access.json')
    sh = gs.open_by_key('1feNhDOpE41gwPwuvtW_V5kZH2hFSt9qc8gZvmoH2UIE')
    worksheet = sh.get_worksheet_by_id(1184834133)

    return worksheet.get()


# print(get_patients_from_other_departments())
for item in get_patients_emergency_room()[1:]:
    print(item[12])
