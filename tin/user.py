from json import dumps
from tinydb_base import exceptions
from .data.users import DataUser
from .data.tokens import Tokens
from .data.exceptions import UserLimit
from .data.commons import checkEmail, password_check

from tinydb_base.exceptions import UsernameExists

def authUser(uname: str, pword: str):

    if checkEmail(uname) == False:
        return {
            'succs': False,
            'error': 'Invalid email',
        }
    
    pw = password_check(pword)
    if pw['password_ok'] == False:
        return {
            'succs': False,
            'error': 'password is not strong enough',
            'data': pw
        }


    obj = DataUser()
    if obj.authUser(username=uname, password=pword) == False:
        return {
            'succs': False,
            'error': 'Authentication Failed',
        }
    return {
        'sucss': True,
        'key': Tokens().addKey(uname)
    }

def createUser(uname: str, pword: str):
    if checkEmail(uname) == False:
        return {
            'succs': False,
            'error': 'Invalid email',
        }
    
    pw = password_check(pword)
    if pw['password_ok'] == False:
        return {
            'succs': False,
            'error': 'password is not strong enough',
            'data': pw
        }

    try:
        obj = DataUser()
        resp = obj.makeUser(username=uname, password=pword)
        return {
            'sucss': True,
            'key': Tokens().addKey(uname)
        }
    except UsernameExists:
        return {
            'succs': False,
            'error': 'email already regersted',
        }
    except UserLimit:
        return {
            'succs': False,
            'error': 'user limit has been reached',
        }
    except Exception as err:
        return {
            'succs': False,
            'error': str(err),
        }

    
