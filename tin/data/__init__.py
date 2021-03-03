from .users import DataUser as User
from .tokens import Tokens
from .maps import Maps
from .settings import Settings

from .commons import Credentials
from .sql import MySQL_Settings, MySQL_Maps, MySQL_Users


def getSettingsObject():
    if 'mysqlUname' in Credentials().read().keys():
        return MySQL_Settings()
    return Settings()

def getMapsObject():
    if 'mysqlUname' in Credentials().read().keys():
        return MySQL_Maps()
    return Maps()

def getUsersObject():
    if 'mysqlUname' in Credentials().read().keys():
        return  MySQL_Users()
    return User()


def checkOwnerByHexAndUsrKey(hex: str, key: str):
    mapsObj = getMapsObject()
    tokensObj = Tokens()
    usersObj = getUsersObject()

    mapData = mapsObj.readByHex(hex=hex)
    if mapData is None:
        return False

    tokenData = tokensObj.getRowByKey(key=key)
    if tokenData is None:
        return False

    userData = usersObj.getIdByUname(tokenData['tag'])
    if userData is None:
        return False

    return userData.doc_id == mapData['owner_id']