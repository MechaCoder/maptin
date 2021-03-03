from mysql.connector import connect, Error
from tinydb.table import Document

from tin.data.commons import Credentials
from .exception import MySQLBaseExceptionCredsNotFound

class MysqlBase:
    
    def __init__(self):
        self.mysqlUname = ''
        self.mysqlPword = ''
        self.dBname = 'maptin'
        self.tblName = ''

        try:
            creds = Credentials().read()
            if 'mysqlUname' not in creds.keys():
                raise MySQLBaseExceptionCredsNotFound('mysqlUname not found')

            if 'mysqlPword' not in creds.keys():
                raise MySQLBaseExceptionCredsNotFound('mysqlPword not found')
            
            self.mysqlUname = creds['mysqlUname']
            self.mysqlPword = creds['mysqlPword']
            
        except FileNotFoundError as err:
            print(err)

    def _creatDbObject(self):
        return connect(host='localhost', user=self.mysqlUname, password=self.mysqlPword, database=self.dBname)
    
    def connectionTest(self):

        try:
            obj = self._creatDbObject()
            obj.cursor()
            obj.close()
            return True
        except Error as err:
            return False

    def tableExists(self):

        db = self._creatDbObject()
        cursor = db.cursor()

        cursor.execute("SHOW TABLES;")

        for tbl in cursor:
            if tbl[0] == self.tblName:
                return True
        return False

    def RowExists(self, col:str, val:str):

        sql = f"""
        SELECT * FROM 
            {self.tblName} 
        WHERE 
            {col} = %s
        """
        vals = (val,)

        with self._creatDbObject() as conn:
            cur = conn.cursor()

            cur.execute(sql, vals)

            result = cur.fetchall()

        if result == []:
            return False     
        return True

    def exists(self, col:str, val:str):
        return self.RowExists(col, val)

