from peewee import IntegrityError
from maptin.data.userKeys import UserTokens as UserTokensDatabaseTable
from maptin.utills.http import success, fail
from maptin.exception import MaptinException

class UserToken:

    def __init__(self) -> None:
        self.data = UserTokensDatabaseTable()

    def makeKey(self, uid:int):

        try:
            token = self.data.create(uid)
            return success({'token': token })
        except IntegrityError:
            return fail('user already has a token issue.')

    def checkToken(self, token:str):

        obj = self.data.getIdByKey(token)
        if len(obj) == 1:
            return success()
        return fail('user key is invaild.')

    def getId(self, token:str):
        return self.data.getIdByKey(token)
        

    def removeToken(self, token:str):
        return self.data.removeByKey(token)