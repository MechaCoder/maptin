from os.path import isfile

from .data.maps import Maps
from .data.tokens import Tokens

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
        mapsource='',
        soundtrack=''
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

def deleteMap(hex:str, key:str):
    tobj = Tokens()
    mobj = Maps()

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


