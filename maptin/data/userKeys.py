from peewee import IntegrityError

from .models import UserToken as UsertokenModel
from .models import maptinDatabase_object as db
from .commons import makeUid

class UserTokens:

    def _keyExists(self, key: str):
        with db.atomic():
            qry = UsertokenModel.select().where(UsertokenModel.key == key)
        return qry.exists() # bool

    def create(self, user_id: int):

        key = makeUid(256, True)
        while self._keyExists(key=key):
            key = makeUid(256, True)

        UsertokenModel.create(
            userId = user_id,
            key = key
        )

        return key

    def getIdByKey(self, key: str):
        
        keys = []
        with db.atomic():

            for row in UsertokenModel.select().where(UsertokenModel.key==key):
                keys.append(row.userId)

        return keys

    def removeByKey(self, key: str):
        
        with db.atomic():
            UsertokenModel.delete().where(UsertokenModel.key == key)
        return True
