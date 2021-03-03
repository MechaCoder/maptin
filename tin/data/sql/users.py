from .base import MysqlBase
from .exception import MySQL_SettingsException
from os import urandom

from tin.data.commons import mkHex
from tinydb_base.user import mkpassword

class MySQL_Users(MysqlBase):

    def __init__(self):
        super().__init__()
        self.tblName = 'users'

    def createTable(self):

        if self.tableExists():
            return False

        sql = f"""
        CREATE TABLE `{self.tblName}` (
        	`username` varchar(255) NOT NULL,
        	`password` varchar(255) NOT NULL,
        	`id` INT NOT NULL AUTO_INCREMENT,
        	PRIMARY KEY (`id`)
        );
        """
        with self._creatDbObject() as conn:
            cur = conn.cursor()
            cur.execute(sql)

        return True

    def makeUser(self, username: str, password: str):

        sql = f"""
        INSERT INTO {self.tblName} (
            username, password
        ) VALUES (
            %s, %s
        )
        """
        pw = mkpassword(password, urandom(32))
        values = (username, pw)

        with self._creatDbObject() as conn:
            cur = conn.cursor()
            cur.execute(sql, values)
            conn.commit()

        return True

    def getIdByUname(self, uname):

        sql = f"""
        SELECT * FROM {self.tblName} WHERE username = %s
        """
        values = (uname,)

        with self._creatDbObject() as conn:
            cur = conn.cursor()
            cur.execute(sql, values)
            results = cur.fetchall()  

    def authUser(self, username: str, password: str) -> bool:

        sql = f"""
            SELECT password
            FROM {self.tblName} WHERE username = %s
        """
        values = (username, )

        with self._creatDbObject() as conn:
            cur = conn.cursor()
            cur.execute(sql, values)
            results = cur.fetchall()

        if results == []:
            return False

        salt = results[0][0][:64]
        salt = bytes.fromhex(salt)

        if mkpassword(password, salt) == results[0][0]:
            return True

        return False

        