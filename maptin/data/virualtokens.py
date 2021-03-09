from os.path import isfile
from .models import VirtualToken as VirtualTokenModels
from .models import maptinDatabase_object as db
from .commons import makeUid, vaildateUrl, Document

class VirtualToken:
    
    def _makeDocument(self, row):
        return Document({
            'hex': row.hex,
            'maphex': row.maphex,
            'token_source': row.token_source,
            'x': row.x,
            'y': row.y,
            'conseal': row.conseal
        }, row.id)

    def _hexExists(self, hex: str):
        with db.atomic():
            qry = VirtualTokenModels.select().where(VirtualTokenModels.hex == hex)
        return qry.exists()

    def create(self, token_source:str, maphex:str):

        hex_candate = ''
        while True:
            hex_candate = makeUid(16)
            if self._hexExists(hex_candate) is False:
                break

        with db.atomic():
            VirtualTokenModels.create(
                hex = hex_candate,
                maphex = maphex,
                token_source = token_source,
                x = 260,
                y = 260,
            )

        return True

    def getByMaphex(self, maphex: str):

        rList = []
        with db.atomic():
            for row in VirtualTokenModels.select().where(VirtualTokenModels.maphex == maphex):
                rList.append(self._makeDocument(row))
        return rList

    def updateByHex(self, hex: str, x: int, y: int):

        with db.atomic():
            VirtualTokenModels.update(
                x=x,
                y=y
            ).where(VirtualTokenModels.hex == hex)
        return True

    def deleteByHex(self, hex: str):

        with db.atomic():
            VirtualTokenModels.delete().where(
                VirtualTokenModels.hex == hex
            )

        return True

