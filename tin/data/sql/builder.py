from .base import MysqlBase
from .settings import MySQL_Settings

class Builder(MysqlBase):

    def main(self):

        settings = MySQL_Settings()

        if self.connectionTest():
            print('database connection test succssful')

        if settings.createTable():
            print(f'{settings.tblName} has been created')
        pass
        