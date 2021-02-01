from tinydb.queries import Query
from .commons import DataCommons, mkHex

class Maps(DataCommons):

    def __init__(self, file: str = 'ds.json', table: str = 'maps', requiredKeys = 'hex,owner_id,title,map_source,map_soundtrack'):
        super().__init__(file=file, table=table, requiredKeys=requiredKeys)

    def create(self, owner_id:int, title:str, mapsource:str, soundtrack:str):
        row = {
            'hex': mkHex(16),
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
    

