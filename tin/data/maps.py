from tinydb.queries import Query
from .commons import DataCommons, mkHex

class Maps(DataCommons):

    def __init__(self, file: str = 'ds.json', table: str = 'maps', requiredKeys = 'hex,owner_id,title,map_source,map_soundtrack'):
        super().__init__(file=file, table=table, requiredKeys=requiredKeys)

    def create(self, owner_id:int, title:str, mapsource:str, soundtrack:str):
        hex = ''
        while True:
            hex = mkHex(16)
            if self.exists('hex', hex) == False:
                break

        row = {
            'hex': hex,
            'owner_id': owner_id,
            'title': title,
            'map_source': mapsource,
            'map_soundtrack': soundtrack
        }
        return super().create(row)
    
    def readByOwnerId(self, oid:int):
        db = self.createObj()
        rows = db.tbl.search(Query().owner_id == oid)
        db.close()

        return rows

    def readByHex(self, hex:str):
        db = self.createObj()
        row = db.tbl.get(Query().hex == hex)
        db.close()
        return row

    def updateByHex(self, hex: str, title: str, map: str, sound: str):
        db = self.createObj()
        db.tbl.update({
            'title': title,
            'map_source': map,
            'map_soundtrack': sound
        }, Query().hex == hex)
        db.close()
        return True

    def updateBgByHex(self, hex:str, bg:str):
        db = self.createObj()
        db.tbl.update(
            {'map_source': bg},
            Query().hex == hex
        )
        db.close()
        return True

    def deleteByHex(self, hex: str):
        db = self.createObj()
        ids = db.tbl.remove(Query().hex == hex)
        db.close()

        if ids != []:
            return True
        return False

    

