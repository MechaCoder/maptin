import os
from tinydb.queries import Query
from tinydb_base.user import User
from .exceptions import UserLimit

from .commons import Credentials


class DataUser(User):

    def __init__(self, file='ds.json', table='users',
                 requiredKeys='username,password'):
        super().__init__(file=file, table=table, requiredKeys=requiredKeys)
        self.fileName = Credentials().read()['ds']

    def makeUser(self, username: str, password: str):

        return super().makeUser(
            username,
            password
        )

    def getIdByUname(self, uname: str):
        db = self.createObj()
        row = db.tbl.get(Query().username == uname)
        db.close()

        return row
