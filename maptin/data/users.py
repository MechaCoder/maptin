from .models import User as UserModel
from .models import maptinDatabase_object as db
from .commons import makePassword, makeUid, verfyPassword, vaildateEmail
from argon2.exceptions import VerifyMismatchError

class User:

    def create(self, email: str, password: str, commonName: str = ''):

        readysalted = makeUid(128)
        password = makePassword(password, readysalted)

        if vaildateEmail(email) is False:
            return False

        with db.atomic():
            UserModel.create(
                common_name = commonName,
                contact_email = email,
                password_salt = readysalted,
                password = password
            )
        
        return True

    def validate(self, email: str, password: str = ''):
        with db.atomic():
            
            for each in UserModel.select().where(UserModel.contact_email == email):
                try:
                    return verfyPassword(
                        planeText=password, 
                        salt=each.password_salt, 
                        hash=each.password
                    ) # returns true or raise
                except VerifyMismatchError:
                    return False # on password mismatch return False
        return False # if user is not found return False

    def getUserById(self, id: int):
        rList = []
        with db.atomic():
            for each in UserModel.select().where(UserModel.id == id):
                rList.append({
                    'name': each.common_name,
                    'email': each.contact_email,
                    'joined': each.date_created
                })
        return rList

    def getUserByEmail(self, email: str):

        rList = []
        with db.atomic():
            for each in UserModel.select().where(UserModel.contact_email == email):
                rList.append({
                    'name': each.common_name,
                    'email': each.contact_email,
                    'joined': each.date_created
                })
        return rList

    def getAll(self):
        rList = []
        with db.atomic():
            for each in UserModel.select():
                rList.append({
                    'name': each.common_name,
                    'email': each.contact_email,
                    'joined': each.date_created
                })
        return rList
