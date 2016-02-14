import json
import os

import requests
from requests_toolbelt import SSLAdapter


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


def _make_call_to_kobra(payload):

    user = str(os.environ.get('KOBRA_USER'))
    password = str(os.environ.get('KOBRA_PASSWORD'))
    adapter = SSLAdapter('SSLv23')
    s = requests.Session()
    s.mount('https://', adapter)

    r = s.post("https://kobra.ks.liu.se/students/api", auth=(user, password), data=payload)
    if not r.status_code == requests.codes.ok:
        if r.status_code == 404:
            raise LiuNotFoundError
        else:
            raise LiuGetterError
    r.encoding = "iso-8859-1"
    result_dict = json.loads(r.text, encoding="iso-8859-1")

    return result_dict
