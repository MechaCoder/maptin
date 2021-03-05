from json import dumps
from os import listdir
from os.path import isfile
from os.path import join
from tin.data.commons import Credentials
# from .data.vTokens import vTokenData
from .data import getVtokensObject as vTokenData
from .data import getVtokensObject as Vtoken
from .map import Maps

from .commons import success, fail

# class Vtoken(): pass

def getUsedMaps():
    maps = {}

    for map in Maps().readAll():
        
        if map['map_source'] not in maps.keys():
            maps[map['map_source']] = 1
            continue
        
        maps[map['map_source']] = maps[map['map_source']] + 1

    mapsSorted = []
    
    for map in {k: v for k, v in sorted(maps.items(), key=lambda item: item[1])}.keys():
        mapsSorted.append(map)
    mapsSorted.reverse()

    return mapsSorted

def tokensList():
    path = 'static/a/tokens'
    data = Vtoken().getPopluarty()
    imgPath = join(Credentials().read()['root'], path)
    
    for f in listdir(imgPath):
        p = '/' + path + '/'  + f

        if p in data:
            continue

        data.append(
            p
        )

    return {
        'succs': True,
        'data': data
        
    }

def mapsList():
    path = 'static/a/maps'
    data = []
    imgPath = join(Credentials().read()['root'], path)

    for f in listdir(imgPath):
        data.append(
            '/' + path + '/'  + f
        )

    return {
        'succs': True,
        'data': {'all': data, 'popular': getUsedMaps()}
    }

def createToken(mapHex:str, srcImg:str, x:float, y:float):

    m = Maps().exists('hex', mapHex)
    if m == False:
        return fail('mapHex is invalid')

    if isfile(srcImg[1:]) == False:
        return fail('that is not a vaild img')
    
    
    vid = Vtoken().create(
        mapHex=mapHex,
        source=srcImg,
        tokenType='token',
        x=x,
        y=y
    )

    return success({'id': vid})

def updateLocation(hex:str, x:int, y:int):

    updated = Vtoken().updateByHex(
        hex=hex,
        x=x,
        y=y
    )

    return success({'data': updated})


def updateConseal(hex:str, conseal:bool):
    obj = vTokenData().updateConsealByHex(hex, conseal)
    if obj == []:
        return fail()
    return success()

def removeVtoken(hex:str):
    if Vtoken().deleteByHex(hex):
        return success()
    return fail()


