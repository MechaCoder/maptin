from tinydb.queries import Query
from tinydb_base.user import User

class DataUser(User): 

    def getIdByUname(self, uname:str):
        db = self.createObj()
        row = db.tbl.get(Query().username == uname)
        db.close()

        return row
