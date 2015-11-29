import base64

__author__ = 'jonathan'


def encode(nr, string):
    i = 0
    while i < nr:
        if type(string) == str:
            string = string.encode('utf-8')
        string = base64.urlsafe_b64encode(string)
        i += 1
    return string


def decode(nr, string):
    i = 0
    while i < nr:
        string = base64.urlsafe_b64decode(string)
        i += 1
    return string.decode('utf-8')
