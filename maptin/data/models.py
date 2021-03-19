from datetime import datetime
from peewee import Model, SqliteDatabase
from peewee import CharField, DateTimeField, IntegerField, BooleanField
from maptin.data.commons import makeUid
from maptin.utills.credentals import Credentials

# TODO change to use MySQL
maptinDatabase_object = SqliteDatabase(
    database=Credentials().getKey('ds')
)

class BaseModel(Model):

    class Meta:
        database = maptinDatabase_object


class User(BaseModel):
    common_name = CharField(max_length=32)
    contact_email = CharField(max_length=128, unique=True)
    password_salt = CharField(default=makeUid(128))
    password = CharField()
    date_created = DateTimeField(
        default=datetime.now()
    )


class Map(BaseModel):
    hex= CharField(max_length=128, unique=True)
    title = CharField(max_length=32, default='New Map')
    owner_id = IntegerField()
    map_background = CharField()
    map_soundtrack = CharField()
    map_width = IntegerField(default=3000)
    map_fog = BooleanField(default=False)


class VirtualToken(BaseModel):
    hex = CharField(max_length=16, unique=True)
    maphex = CharField(max_length=32)
    token_source = CharField()
    x = IntegerField()
    y = IntegerField()
    conseal = BooleanField(default=False)

class UserToken(BaseModel):
    userId = IntegerField()
    key = CharField(max_length=256, unique=True)

#atempts to create tables if they don't exist
maptinDatabase_object.create_tables([UserToken, User, Map, VirtualToken])

