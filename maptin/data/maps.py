from os.path import isfile, join

from peewee import Model

from .models import Map as MapModel
from .users import User
from .models import maptinDatabase_object as db
from .commons import makeUid, vaildateUrl, Document
from maptin.utills.credentals import Credentials

from .exceptions import DoseNotExist, DataInvaild

class Map:

    def _makeDocument(self, row):
        return Document({
            'hex': row.hex,
            'title': row.title,
            'owner_id': row.owner_id,
            'map_background': row.map_background,
            'map_soundtrack': row.map_soundtrack,
            'map_width': row.map_width,
            'map_fog': row.map_fog
        }, row.id)

    def _hexExists(self, hex: str):
        with db.atomic():
            qry = MapModel.select().where(MapModel.hex == hex)
        return qry.exists()

    def create(self, owner_id: int, map_background:str, map_soundtrack:str):

        hex_candate = ''
        while True:
            hex_candate = makeUid(16)
            if self._hexExists(hex_candate) is False:
                break

        obj = User().getUserById(owner_id)
        if len(obj) == 0:
            raise DoseNotExist('user.id dose not exist.')

        if vaildateUrl(map_soundtrack) is False:
            raise DataInvaild('the sound track url is not vaild')

        path2bg = join(
            Credentials().read()['root'], map_background[1:]
        )

        if isfile(path2bg) is False:
            raise DataInvaild('the background path is invaild')

        with db.atomic():
            MapModel.create(
                hex=hex_candate,
                owner_id=owner_id,
                map_background=map_background,
                map_soundtrack=map_soundtrack,
            )
        return hex_candate

    def readAll(self):
        rList = []
        with db.atomic():
            for each in MapModel.select():
                rList.append(self._makeDocument(each))
        return rList

    def readByOwnerId(self, owner_id: int):

        rList = []
        with db.atomic():
            for each in MapModel.select().where(MapModel.owner_id == owner_id):
                rList.append(
                    self._makeDocument(each)
                )
        return rList

    def readByHex(self, hex: str):

        if self._hexExists(hex) is False:
            raise DoseNotExist('The passed hex dose not exist')

        rList = []
        with db.atomic():
            for each in MapModel.select().where(MapModel.hex == hex):
                rList.append(
                    self._makeDocument(each)
                )
        return rList

    def updateByHex(self, hex: str, title: str, map_background: str, map_soundtrack: str, map_width: int, map_fog: bool):

        if self._hexExists(hex) is False:
            raise DoseNotExist('The passed hex dose not exist')

        if vaildateUrl(map_soundtrack) is False:
            raise DataInvaild('The soundtrack is invalid')

        path = Credentials().read()['root'] + map_background
        if isfile(path) is False:
            raise DataInvaild('the background path is invaild')

        with db.atomic():
            MapModel.update(
                title=title,
                map_background=map_background,
                map_soundtrack=map_soundtrack,
                map_width=map_width,
                map_fog=map_fog
            ).where(MapModel.hex == hex).execute()

        return True

    def updateBgByHex(self, hex: str, bg:str):

        if self._hexExists(hex) is False:
            raise DoseNotExist('The passed hex dose not exist')

        with db.atomic():
            qry = MapModel().update(
                map_background=bg
            ).where(MapModel.hex == hex)
            qry.execute()

        return False

    def deleteByHex(self, hex: str):

        if self._hexExists(hex) is False:
            raise DoseNotExist('The passed hex dose not exist')

        with db.atomic():
            delQry = MapModel().delete().where(
                MapModel.hex == hex
            )
            delQry.execute()

        return True
