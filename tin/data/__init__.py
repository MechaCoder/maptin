from .users import DataUser as User
from .tokens import Tokens
from .maps import Maps


def checkOwnerByHexAndUsrKey(hex: str, key: str):
    mapsObj = Maps()
    tokensObj = Tokens()
    usersObj = User()

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
