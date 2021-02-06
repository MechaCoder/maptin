from os import listdir
from os.path import isfile
from .data.vTokens import vTokenData
from .map import Maps

from .commons import success, fail


class Vtoken(vTokenData): pass

def tokensList():
    path = 'static/a/tokens'
    data = []
    for f in listdir(path):
        data.append(
            '/' + path + '/'  + f
        )

    return {
        'succs': True,
        'data': data
        
    }

def mapsList():
    path = 'static/a/maps'
    data = []
    for f in listdir(path):
        data.append(
            '/' + path + '/'  + f
        )

    return {
        'succs': True,
        'data': data
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

def removeVtoken(hex:str):
    if Vtoken().deleteByHex(hex):
        return success()
    return fail()