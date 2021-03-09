from maptin.data.users import User as UserDatabaseTable
from maptin.utills.http import success, fail
from maptin.exception import MaptinException

from flask import request
from peewee import IntegrityError

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
            return success()
        return fail('vaildation has failed')

    def createUser(self, req: request):
        creds = req.get_json()

        if 'uname' not in creds.keys():
            raise MaptinException('uname is required in the request')

        if 'pword' not in creds.keys():
            raise MaptinException('uname is required in the request')

        try:
            if self.data.create(creds['uname'], creds['pword']):
                return success()
        except IntegrityError as Error:
            return fail('this email already exists')
