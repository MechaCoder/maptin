from tinydb.queries import Query
from tinydb_base.user import User
from .exceptions import UserLimit



class DataUser(User):

    def __init__(self, file='ds.json', table='users', requiredKeys='username,password'):
        super().__init__(file=file, table=table, requiredKeys=requiredKeys)

    def makeUser(self, username: str, password: str):
        
        db = self.createObj()
        num = len(db.tbl.all())
        print(num)
        db.close()

        if num > 10:
            raise UserLimit('the user limit has been reached')

        return super().makeUser(
            username, 
            password
        )

    def getIdByUname(self, uname:str):
        db = self.createObj()
        row = db.tbl.get(Query().username == uname)
        db.close()

        return row
