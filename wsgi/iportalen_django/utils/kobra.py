import json
import os

import requests
# from requests_toolbelt import SSLAdapter


class LiuNotFoundError(Exception):
    pass


class LiuGetterError(Exception):
    pass


def get_user_by_liu_id(liu_id):
    return _make_call_to_kobra({'liu_id': liu_id})


def get_user_by_p_nr(pnr):
    return _make_call_to_kobra({'personal_number': pnr})


def get_user_by_rfid(rfid):
    return _make_call_to_kobra({'rfid_number': rfid})


def _convert_new_to_old(new_kobra):
    return {'email': new_kobra['email'],
            'last_name': new_kobra['name'].split(' ', 1)[1],
            'first_name': new_kobra['name'].split(' ', 1)[0],
            'rfid_number': None,
            'personal_number': None}


def _make_call_to_kobra(payload):
    p = None
    liuid=None
    if 'liu_id' in payload:
        p = payload['liu_id']
        liuid = p
    elif 'rfid_number' in payload:
        p = payload['rfid_number']
    if p is None:
        raise LiuGetterError

    url = "https://kobra.karservice.se/api/v1/students/{}/".format(p)

    payload = ""
    token = str(os.environ.get('KOBRA_TOKEN'))
    headers = {
        'authorization': "Token {}".format(token),
        'content-type': "application/json",
        'cache-control': "no-cache",
    }

    response = requests.request("GET", url, data=payload, headers=headers)

    person = json.loads(response.text, encoding="iso-8859-1")
    if 'detail' in person:
        print(person['detail'])
        if 'Invalid token' in person['detail']:
            raise LiuGetterError(person['detail'])
        raise LiuNotFoundError(person['detail'])
    if person['email'] == "None" and liuid:
        person['email'] = "{liuid}@student.liu.se".format(liuid=liuid)
    return _convert_new_to_old(person)


# def _make_call_to_old_kobra(payload):
#
#     user = str(os.environ.get('KOBRA_USER'))
#     password = str(os.environ.get('KOBRA_PASSWORD'))
#     adapter = SSLAdapter('SSLv23')
#     s = requests.Session()
#     s.mount('https://', adapter)
#
#     r = s.post("https://kobra.ks.liu.se/students/api", auth=(user, password), data=payload)
#     if not r.status_code == requests.codes.ok:
#         if r.status_code == 404:
#             raise LiuNotFoundError
#         else:
#             raise LiuGetterError
#     r.encoding = "iso-8859-1"
#     result_dict = json.loads(r.text, encoding="iso-8859-1")
#
#     return result_dict

if __name__ == "__main__":
    print(get_user_by_liu_id("jonan099"))
