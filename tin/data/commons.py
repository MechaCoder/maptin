from string import hexdigits
from random import choices
from re import search, fullmatch
from validators import url, ValidationFailure

from tinydb_base import DatabaseBase

def checkEmail(email: str):
    if fullmatch(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email):
        return True
    return False

def password_check(password):
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """

    # calculating the length
    length_error = len(password) < 8

    # searching for digits
    digit_error = search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None

    # overall result
    password_ok = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error )

    return {
        'password_ok' : password_ok,
        'length_error' : length_error,
        'digit_error' : digit_error,
        'uppercase_error' : uppercase_error,
        'lowercase_error' : lowercase_error,
        'symbol_error' : symbol_error,
    }
    

def mkHex(l:int = 8):
    s1 = choices(hexdigits, k=l)
    return ''.join(s1)

def vaildUrl(addr:str, _domain:str = ''):

    try:
        url(addr)
        addr_broken_down = addr.split('.')
        if len(addr_broken_down) < 2:
            return False
        add_domain = addr_broken_down[1]
        if _domain is '':
            return True
        
        if _domain == add_domain:
            return True
        return False
        

    except ValidationFailure:
        return False
    finally:
        return False



class DataCommons(DatabaseBase):

    def _mkHex(l:int = 8):
        s1 = choices(hexdigits, k=l)
        return ''.join(s1)