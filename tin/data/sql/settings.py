from .base import MysqlBase
from .exception import MySQL_SettingsException

from tin.data.commons import mkHex

class MySQL_Settings(MysqlBase):
    
    def __init__(self):
        super().__init__()
        self.tblName = 'settings'

        if self.tableExists() is False:
            return

        if self.RowExists('tag', 'sessionSysKey') is False:
            self.set('sessionSysKey', mkHex(4))

        if self.RowExists('tag', 'socketKey') is False:
            self.set('socketKey', mkHex(1024))


    def createTable(self):
        """ creates the table if the table dose not exist"""
        if self.tableExists():
            return False

        sql = f"""
            CREATE TABLE {self.tblName} (
                id int NOT NULL AUTO_INCREMENT,
                tag varchar(255) NOT NULL,
                val varchar(1024) NOT NULL,
                PRIMARY KEY (id)
            )
        """

        with self._creatDbObject() as conn:
            cur = conn.cursor()
            cur.execute(sql)
        return True

    def get(self, tag:str):

        
        sql = "SELECT val FROM settings WHERE tag = %s"
        valueString = (tag, )

        with self._creatDbObject() as conn:
            cur = conn.cursor()
            cur.execute(sql, valueString)
            result = cur.fetchall()

        if result == []:
            raise MySQL_SettingsException('setting not found')

        return result[0][0]

    def set(self, tag:str, val:str):

        try:
            self.get(tag) # if this meathod raises then an insert is required
            #update statement
            sql = f"UPDATE {self.tblName} SET val = %s WHERE tag = %s"
            values = (val, tag)            

        except MySQL_SettingsException:
            #insert statement

            sql = f"INSERT INTO {self.tblName} (tag, val) VALUES (%s, %s)"
            values = (tag, val)

        with self._creatDbObject() as conn:
            cur = conn.cursor()
            cur.execute(sql, values)
            conn.commit()

        return True

    def resetSessionSysKey(self):
        self.set('sessionSysKey', mkHex(4))
        print("Session key: {}".format(self.get('sessionSysKey')))

            
