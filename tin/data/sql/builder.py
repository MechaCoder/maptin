from .base import MysqlBase
from .settings import MySQL_Settings
from .maps import MySQL_Maps

class Builder(MysqlBase):

    def main(self):

        settings = MySQL_Settings()
        maps = MySQL_Maps()

        if self.connectionTest():
            print('database connection test succssful')

        if settings.createTable():
            print(f'{settings.tblName} has been created')

        if maps.createTable():
            print(f'{maps.tblName} has been created')            
        pass
        