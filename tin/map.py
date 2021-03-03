from os.path import isfile
from tin import user

from validators import url

from .data import checkOwnerByHexAndUsrKey, getMapsObject as Maps
from .data.commons import vaildUrl
from .data.tokens import Tokens
from .data.vTokens import vTokenData as Vtoken
from tin.commons import debug_file

from .commons import success, fail

def createMap(key):
    tobj = Tokens()
    if tobj.keyExsists(key) == False:
        return {
            'succs': False,
            'error': 'invalid key',
        }
    userRow = tobj.getRowByKey(key=key)
    Maps().create(
        owner_id=userRow.doc_id,
        title='New Map',
        mapsource='/static/world-map.gif',
        soundtrack='https://www.youtube.com/watch?v=zOvsyamoEDg',
        width=3000

    )
    return {
        'succs': True,
    }

def listMaps(key:str):
    tobj = Tokens()
    mobj = Maps()

    if tobj.keyExsists(key) == False:
        return {
            'succs': False,
            'error': 'invalid key',
        }

    userRow = tobj.getRowByKey(key=key)
    maps = []

    for map in mobj.readByOwnerId(userRow.doc_id):
        row = {}
        for key in map.keys():
            row[key] = map[key]
        if isfile(row['map_source'] == False) or row['map_source'] == '':
            row['map_source'] = '/static/world-map.gif'
        maps.append(row)

    return maps

def getByHex(hex:str):

    obj = Maps()
    if obj.exists('hex', hex) == False:
        return {
            'succs': False,
            'error': 'invalid hex',
        }

    mapRow =  obj.readByHex(hex)
    returnObj = {}
    for k in mapRow.keys():
        returnObj[k] = mapRow[k]

    returnObj['tokens'] = Vtoken().readByMapHex(hex)

    return {
            'succs': True,
            'data': returnObj,
        }

def updateByHex(hex:str, title:str, map:str, sound:str, width:int, usrKey:str, fog:bool):
    map = map.strip()
    mapTestVal = map
    if mapTestVal[0] == '/':
        mapTestVal = mapTestVal[1:]
    sound = sound.strip()
    # tokensObj = Tokens()
    mapsObj = Maps()

    if isfile(mapTestVal) == False:
        return {
            'succs': False,
            'error': 'map url is invalid',
        }

    if vaildUrl(sound, 'youtube') == False:
        return {
            'succs': False,
            'error': 'sound url is invalid',
        }

    row = mapsObj.readByHex(hex=hex)
    if row == None:
        return {
            'succs': False,
            'error': 'hex is invalid',
        }

    if checkOwnerByHexAndUsrKey(hex=hex, key=usrKey) == False:
        return {
            'succs': False,
            'error': 'the user key is not the owner',
        }

    if mapsObj.updateByHex(hex=hex, title=title, map=map, sound=sound, width=width, fog=fog):
        return {
            'succs': True,
        }
    return {
        'succs': False,
        'error': 'there has been an error'
    }

def upadateBgByHex(hex:str, bg:str):
    if Maps().updateBgByHex(hex, bg):
        return success()


def deleteMap(hex:str, key:str):
    tobj = Tokens()
    mobj = Maps()
    debug_file(type(mobj))

    if tobj.keyExsists(key) == False:
        return {
            'succs': False,
            'error': 'invalid key',
        }
    userRow = tobj.getRowByKey(key=key)
    if mobj.exists('hex', hex) == False:
        return {
            'succs': False,
            'error': 'invalid hex',
        }
    if mobj.deleteByHex(hex=hex):
        return {
            'succs': True,
            'error': 'map has been deleted',
        }
    return {
        'succs': False,
        'error': 'map could not be deleted'
    }
