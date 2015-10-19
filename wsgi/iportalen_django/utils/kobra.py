__author__ = 'jonathan'
import json
from utils.security import decode
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
    ##############################################################################
    # This is by far the ugliest hack I ever written! But since Kobra is using
    # an unsupported ssl protocol and the whole API is a ugly hack. I'm going to
    # leave this fuck-up while i still have some sanity left.
    # Don't contact me when this breaks just rewrite it!
    # How it works:
    # It uses a flask server with some more permissions on another server to execute the request.
    # The flask server reverse checks the ip of iportalen-webgroup.rhcloud.com and only allows calls from that ip
    # Best regards Jonathan, Webmaster 2015-2016
    ##############################################################################
    #import requests
    for k in payload:
        key = k
        value = payload[k]

    import urllib3
    http = urllib3.PoolManager()
    r = http.request("GET", "http://tornet.isektionen.se:8443/{:}/{:}/".format(key, value))
    result_dict = json.loads(decode(25, r.data.decode('utf-8')), encoding="iso-8859-1")
    return result_dict

    # wget --quiet --method POST --header 'authorization: Basic aXNla3Rpb25lbi13ZWJiOjY4NDYzZTEwMzUzMzdhMTc3MDU4' --header 'cache-control: no-cache' --output-document - 'https://kobra.ks.liu.se/students/api?liu_id=jonan099'
