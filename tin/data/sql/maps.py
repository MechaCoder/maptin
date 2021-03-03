from dns.flags import DO
from tinydb.table import Document
from tin.data.commons import mkHex
from .base import MysqlBase

class MySQL_Maps(MysqlBase):

    def __init__(self):
        super().__init__()
        self.tblName = 'maps'

    def createTable(self):

        if self.tableExists():
            return False

        sql = f"""
            CREATE TABLE {self.tblName} (
                `id` INT NOT NULL AUTO_INCREMENT,
                `hex` varchar(255) NOT NULL,
                `owner_id` INT NOT NULL,
                `title` varchar(255) NOT NULL,
                `map_source` varchar(255) NOT NULL,
                `map_soundtrack` varchar(255) NOT NULL,
                `width` INT NOT NULL,
                `fog` BOOLEAN NOT NULL,
                PRIMARY KEY (`id`)
            );
        """

        with self._creatDbObject() as conn:
            cur = conn.cursor()
            cur.execute(sql)

        return True

    def create(self, owner_id:int, title:str, mapsource:str, soundtrack:str, width:int, fog:bool = False):

        hex = ''
        while True:
            hex = mkHex(16)
            if self.RowExists('hex', hex) == False:
                break

        sql = f"""
            INSERT INTO {self.tblName} (
                hex, owner_id, title, map_source, map_soundtrack, width, fog
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s
            )
        """

        values = (hex , owner_id, title, mapsource, soundtrack, width, fog)

        with self._creatDbObject() as conn:
            cur = conn.cursor()
            cur.execute(sql, values)
            conn.commit()

        return True

    def readAll(self):
        sql = f""" SELECT * FROM {self.tblName} """

        with self._creatDbObject() as conn:
            cur = conn.cursor()
            cur.execute(sql)
            result = cur.fetchall()

        rList = []
        for e in result:
            obj = Document(
                {
                    'hex': e[1],
                    'owner_id': e[2],
                    'title': e[3],
                    'map_source': e[4],
                    'map_soundtrack': e[5],
                    'width': e[6],
                    'fog': e[7]
                },
                doc_id=e[0]
            )
            rList.append(obj)
        return rList

    def readByOwnerId(self, oid: int):

        sql = f"""
            SELECT * FROM {self.tblName} WHERE owner_id = %s
        """
        values = (oid, )

        with self._creatDbObject() as conn:
            cur = conn.cursor()
            cur.execute(sql, values)
            result = cur.fetchall()

        rList = []
        for e in result:
            obj = Document(
                {
                    'hex': e[1],
                    'owner_id': e[2],
                    'title': e[3],
                    'map_source': e[4],
                    'map_soundtrack': e[5],
                    'width': e[6],
                    'fog': e[7]

                },
                doc_id=e[0]
            )
            rList.append(obj)
        return rList

    def readByHex(self, hex:str):
        sql = f""" SELECT * FROM {self.tblName} WHERE hex = %s """
        values = (hex, )

        with self._creatDbObject() as conn:
            cur = conn.cursor()
            cur.execute(sql, values)
            results = cur.fetchall()

        rList = []
        for e in results:
            obj = Document(
                {
                    'hex': e[1],
                    'owner_id': e[2],
                    'title': e[3],
                    'map_source': e[4],
                    'map_soundtrack': e[5],
                    'width': e[6],
                    'fog': e[7]

                },
                doc_id=e[0]
            )
            rList.append(obj)
        return rList[0]

    def updateByHex(self, hex: str, title: str, map: str, sound: str, width: int, fog: bool):

        sql = f"""
        UPDATE {self.tblName} SET
            title = %s,
            map_source = %s,
            map_soundtrack = %s,
            width = %s,
            fog = %s
        WHERE hex = %s

        """
        values = (title, map, sound, width, fog, hex)

        with self._creatDbObject() as conn:
            cur = conn.cursor()
            cur.execute(sql, values)
            conn.commit()

        return True

    def updateBgByHex(self, hex:str, bg:str  ):

        sql = f"""
        UPDATE {self.tblName} SET
            map_source = %s
        WHERE hex = %s
        """
        values = (bg, hex)

        with self._creatDbObject() as conn:
            cur = conn.cursor()
            cur.execute(sql, values)
            conn.commit()

        return True

    def deleteByHex(self, hex:str):
        sql = f"""
        DELETE FROM {self.tblName} WHERE hex = %s
        """
        values = (hex, )

        with self._creatDbObject() as conn:
            cur = conn.cursor()
            cur.execute(sql, values)
            conn.commit()
        return True
