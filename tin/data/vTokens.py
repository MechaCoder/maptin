from tinydb.queries import Query
from tinydb_base import DatabaseBase
from .commons import mkHex, DataCommons

class vTokenData(DataCommons):

    def __init__(self, file: str = 'ds.vToken.json', table: str = 'tokens', requiredKeys = 'hex,mapHex,source,type,x:int,y:int,ts:float'):
        super().__init__(file=file, table=table, requiredKeys=requiredKeys)

    def create(self, mapHex, source, tokenType, x, y):

        hex = ''

        while True:
            hex = mkHex()
            if self.exists('hex', hex) == False:
                break

        row = {
            'hex': hex,
            'mapHex': mapHex,
            'source': source,
            'type': tokenType,
            'x': x,
            'y': y,
            'ts': self.now_ts()

        }
        return super().create(row)

    def readByMapHex(self, mapHex:str):
        db = self.createObj()
        rows = db.tbl.search(
            Query().mapHex == mapHex
        )
        db.close()
        return rows

    