from maptin.data.users import User as UserDatabaseTable
from maptin.data.userKeys import UserTokens
from maptin.utills.http import success, fail
from maptin.exception import MaptinException

from flask import request
from peewee import IntegrityError, OperationalError

class User:

    def __init__(self):
        self.data = UserDatabaseTable()

    def testUser(self, req: request):
        creds = req.get_json()

        if 'uname' not in creds.keys():
            raise MaptinException('uname is required in the request')

        if 'pword' not in creds.keys():
            raise MaptinException('uname is required in the request')

        if self.data.validate(email=creds['uname'], password=creds['pword']):
            
            user = self.data.getUserByEmail(creds['uname'])
            user = user[0]
            try:
                key = UserTokens().create(user['id'])
                return success({'key': key})
            except IntegrityError as error:
                return fail(str(error))
            except OperationalError as error:
                return fail(str(error))
            

        return fail('vaildation has failed')

    def createUser(self, req: request):
        creds = req.get_json()

        if 'uname' not in creds.keys():
            raise MaptinException('uname is required in the request')

        if 'pword' not in creds.keys():
            raise MaptinException('uname is required in the request')

        try:
            if self.data.create(creds['uname'], creds['pword']):
                user = self.data.getUserByEmail(creds['uname'])
                user = user[0]
                key = UserTokens().create(user['id'])
                return success({'key': key})
        except IntegrityError as error:
            return fail(str(error))
        except OperationalError as error:
            return fail(str(error))

    def updatePassword(self, userId:int):
        pass
