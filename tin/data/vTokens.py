from tinydb.queries import Query
from tinydb_base import DatabaseBase
from .commons import mkHex, DataCommons
from .exceptions import TokenLimit


class vTokenData(DataCommons):

    def __init__(self, file: str = 'ds.json', table: str = 'vtokens',
                 requiredKeys='hex,mapHex,source,type,x:int,y:int,ts:float'):
        super().__init__(file=file, table=table, requiredKeys=requiredKeys)

    def create(self, mapHex, source, tokenType, x, y):

        db = self.createObj()
        num = db.tbl.count(Query().mapHex == mapHex)
        db.close()

        if num > 100:
            raise TokenLimit('token limit has been reached for this map')

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

    def readByMapHex(self, mapHex: str):
        db = self.createObj()
        rows = db.tbl.search(
            Query().mapHex == mapHex
        )
        db.close()
        return rows

    def updateByHex(self, hex: str, x: int, y: int):
        db = self.createObj()
        rows_updated = db.tbl.update(
            {'x': x, 'y': y},
            Query().hex == hex
        )
        db.close()
        return rows_updated

    def deleteByHex(self, hex: str):

        if self.exists('hex', hex) == False:
            return False

        db = self.createObj()
        db.tbl.remove(Query().hex == hex)
        db.close()
        return True

    def getPopluarty(self):

        srcs = {}
        for row in self.readAll():
            if row['source'] not in srcs.keys():
                srcs[row['source']] = 1
                continue
            srcs[row['source']] = srcs[row['source']] + 1

        sortedDict = {
            srcs: v for srcs,
            v in sorted(
                srcs.items(),
                key=lambda item: item[1])}
        rObj = list(sortedDict.keys())
        rObj.reverse()

        return rObj
