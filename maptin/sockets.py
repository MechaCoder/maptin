from maptin.utills.http import fail, success
from .virtualtokens import VirtualTokenDatabaseTable as VTDBT
from .map import MapDatabaseTable as MDBT

class Sockets:

    def mapVirtualTokens(self, mapHex:str):
        obj = {'mapHex': mapHex}

        #check that the map exists
        if len(MDBT().readByHex(mapHex)) == 0:
            return fail('map dose not exists')

        obj['tokens'] = VTDBT().getByMaphex(maphex=mapHex)
        
        return success(obj)

    def updateVirtualTokens(self, hex: str, x: int, y:int):
        
        if VTDBT().updateByHex(hex, x, y):
            return({
                'hex': hex,
                'x': x,
                'y': y
            })