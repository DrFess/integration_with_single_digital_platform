import json
from pprint import pprint

from requests import Session

from parse_l2 import authorization_l2
from settings import login_l2, password_l2


def get_chatID(connect: Session) -> dict:
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Origin': 'http://192.168.10.161',
        'Referer': 'http://192.168.10.161/ui/chambers',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    json_data = {
        'userId': 1951,
    }

    response = connect.post(
        'http://192.168.10.161/api/chats/get-dialog-id',
        headers=headers,
        json=json_data,
        verify=False,
    ).json()
    return response


def send_message(connect: Session):
    """Ошибка 500"""

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundarybKTVntMxHYlR5ElD',
        'DNT': '1',
        'Origin': 'http://192.168.10.161',
        'Referer': 'http://192.168.10.161/ui/chambers',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    files = {
        'form': '{"dialogId":722,"text":"333"}'
    }

    response = connect.post('http://192.168.10.161/api/chats/send-message',
                            files=files,
                            headers=headers,
                            verify=False)
    return response.text, response.status_code


session = Session()
print(authorization_l2(session, login=login_l2, password=password_l2))
print(session.cookies)
print(send_message(session))
# session.close()
