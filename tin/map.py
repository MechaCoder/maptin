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
            row['map_source'] = 'static/world-map.gif'
        maps.append(row)
    return maps



    
