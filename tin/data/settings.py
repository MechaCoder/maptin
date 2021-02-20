from tinydb_base.getSet import GetSet

from .commons import mkHex

class Settings(GetSet):

    def __init__(self, file: str = 'ds.json', table: str = 'settings'):
        super().__init__(file=file, table=table)
        self.set('socketKey', mkHex(1024))
        self.set('sessionSysKey', mkHex())
    