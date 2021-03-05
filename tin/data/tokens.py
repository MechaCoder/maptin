import os
from tinydb_base.getSet import GetSet, Factory, Query, futureTimeStamp
from .commons import mkHex, Credentials


class Tokens(GetSet):

    def __init__(self, file: str = 'ds.json', table: str = 'tokens'):
        super().__init__(file=file, table=table)
        self.fileName = Credentials().read()['ds']

    def addKey(self, uname: str):
        key = ''
        while True:  # loop ontill broken
            key = mkHex(128)
            if self.keyExsists(key) == False:  # if the key dose not exist
                break

        self.set(uname, key)
        return key

    def keyExsists(self, key: str):
        db = Factory(self.fileName, self.tableName)
        e = db.tbl.contains(Query().val == key)
        db.close()

        return e

    def getRowByKey(self, key):
        db = Factory(self.fileName, self.tableName)
        row = db.tbl.get(Query().val == key)
        db.close()

        return row
