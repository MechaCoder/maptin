from tin.data import vTokens
from .base import MysqlBase

from .settings import MySQL_Settings
from .maps import MySQL_Maps
from .users import MySQL_Users
from .tokens import MySQL_Tokens
from .vtokens import MySQL_Vtokens

class Builder(MysqlBase):

    def main(self):

        settings = MySQL_Settings()
        maps = MySQL_Maps()
        users = MySQL_Users()
        tokens = MySQL_Tokens()
        vTokens = MySQL_Vtokens()

        if self.connectionTest():
            print('database connection test succssful')

        if settings.createTable():
            print(f'{settings.tblName} has been created')

        if maps.createTable():
            print(f'{maps.tblName} has been created')            
        
        if users.createTable():
            print(f'{users.tblName} has been created')

        if tokens.createTable():
            print(f'{tokens.tblName} has been created')

        if vTokens.createTable():
            print(f'{vTokens.tblName} has been created')
        pass