__author__ = 'jonathan'
import json


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
    # This is by far the ugliest hack I ever written! But since Kobra is using   #
    # an unsupported ssl protocol and the whole API is a ugly hack. I'm going to #
    # leave this fuck-up while i still have some sanity left.                    #
    # Don't contact me when this breaks just rewrite it!                         #
    # Best regards Jonathan, Webmaster 2015-2016                                 #
    ##############################################################################
    key = "liu_id"
    value = ""
    for k in payload:
        key = k
        value = payload[k]
    from subprocess import Popen, PIPE

    p = Popen("wget --quiet \
  --method POST \
  --header 'authorization: Basic aXNla3Rpb25lbi13ZWJiOjY4NDYzZTEwMzUzMzdhMTc3MDU4' \
  --header 'cache-control: no-cache' \
  --header 'postman-token: 559e3b8e-8292-171e-46d0-53bc764339d3' \
  --output-document \
  - 'https://kobra.ks.liu.se/students/api?{0}={1}'".format(key, value), shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    result_dict = json.loads(output.decode('utf-8'), encoding="iso-8859-1")
    return result_dict

    # Below this line is the preferred way to make the call, but in python3.3 it's RETARDED!
    # user = "***REMOVED***"
    # password = "***REMOVED***"  # Very secret :)
    # s = requests.Session()
    # s.mount('https://', SSLAdapter(ssl.PROTOCOL_SSLv23))
    # # KOBRA IS TO FUCKING OLD AND A BAD FUCK-UP. This shit doesn't work.
    # r = s.post("https://kobra.ks.liu.se/students/api", auth=(user, password), data=payload, verify=False, )
    # if not r.status_code == requests.codes.ok:
    #     if r.status_code == 404:
    #         raise LiuNotFoundError
    #     else:
    #         raise LiuGetterError
    #
    # r.encoding = "iso-8859-1"
    # result_dict = json.loads(r.text, encoding="iso-8859-1")
    # return result_dict
