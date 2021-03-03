from tinydb.table import Document
from .base import MysqlBase
from .settings import MySQL_Settings

from tin.data.commons import mkHex

class MySQL_Tokens(MySQL_Settings):

    def __init__(self):
        super().__init__()
        self.tblName = 'tokens'

    def addKey(self, uname:str):

        key = ''
        while True:
            key = mkHex(128)
            if self.exists('val', key) is False:
                break

        self.set(uname, key)
        return key

    def getRowByKey(self, key):

        sql = f""" SELECT * FROM {self.tblName} WHERE val = %s """
        values = (key,)

        with self._creatDbObject() as conn:
            cur = conn.cursor()
            cur.execute(sql, values)
            results = cur.fetchall()

        row = results[0]
        return Document({
            'tag': row[1],
            'val': row[2]
        }, row[0])

    def keyExsists(self, key:str):
        return self.RowExists('val', key)

