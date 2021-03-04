from tin.commons import debug_file
from tin.data import sql
from tinydb.table import Document
from .base import MysqlBase
from tin.data.commons import mkHex



class MySQL_Vtokens(MysqlBase):

    def __init__(self):
        super().__init__()
        self.tblName = 'vtokens'

    def createTable(self):

        if self.tableExists():
            return False

        sql = f"""
        CREATE TABLE `{self.tblName}` (
            `ID` INT NOT NULL AUTO_INCREMENT,
            `hex` varchar(8) NOT NULL UNIQUE,
            `maphex` varchar(255) NOT NULL,
            `source` varchar(255) NOT NULL,
            `type` varchar(255) NOT NULL,
            `x` INT NOT NULL,
            `y` INT NOT NULL,
            `conseal` INT NOT NULL,
            PRIMARY KEY (`ID`)
        );
        """

        with self._creatDbObject() as conn:
            cur = conn.cursor()
            cur.execute(sql)

        return True

    def create(self, mapHex, source, tokenType, x, y):
        hex = ''
        while True:
            hex = mkHex()
            if self.RowExists('hex', hex) is False:
                break

        sql = f"""
            INSERT INTO {self.tblName} (
                hex, maphex, source, type, x, y, conseal
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s
            )
        """
        values = (hex, mapHex, source, tokenType, x, y, False)

        with self._creatDbObject() as conn:
            cur = conn.cursor()
            cur.execute(sql, values) 
            conn.commit()
        
        return True

    def readByMapHex(self, mapHex: str):
        sql = f"""
        SELECT * FROM {self.tblName} WHERE `maphex` = %s
        """
        values = (mapHex,)
        with self._creatDbObject() as conn:
            cur = conn.cursor()
            cur.execute(sql, values)
            result = cur.fetchall()

        rList = []
        for e in result:
            obj = Document({
                'hex': e[1],
                'mapHex': e[2],
                'source': e[3],
                'type': e[4],
                'x': e[5],
                'y': e[6],
                'conseal': e[7]
            }, e[0])
            rList.append(obj)
        return rList

    def updateByHex(self, hex:str, x:int, y:int):

        sql = f"""
        UPDATE {self.tblName} SET
            x = %s,
            y = %s
        WHERE hex = %s
        """
        values = (x, y, hex)

        with self._creatDbObject() as conn:
            cur = conn.cursor()
            cur.execute(sql, values)
            conn.commit()

        return True

    def updateConsealByHex(self, hex, conseal):

        sql = f"""
        UPDATE {self.tblName} SET
            conseal = %s
        WHERE hex = %s
        """
        values = (conseal, hex)

        with self._creatDbObject() as conn:
            cur = conn.cursor()
            cur.execute(sql, values)
            conn.commit()


        return True

    def deleteByHex(self, hex: str):

        sql = f"""
        DELETE FROM {self.tblName} WHERE hex = %s
        """
        values = (hex,)

        with self._creatDbObject() as conn:
            cur = conn.cursor()
            cur.execute(sql, values)
            conn.commit()

        return True


    def getPopluarty(self):

        sql = f""" SELECT source FROM {self.tblName} """
        with self._creatDbObject() as conn:
            cur = conn.cursor()
            cur.execute(sql)
            results = cur.fetchall()
        
        rObject = {}
        for row in results:
            if row[0] not in rObject.keys():
                rObject[ row[0] ] = 1
                continue
            rObject[row[0]] = rObject[row[0]] + 1
        rObject = {rObject: v for rObject, v in sorted(rObject.items(), key=lambda item: item[1])}
        rObject = list(rObject.keys())
        rObject.reverse()

        return rObject




