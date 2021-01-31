from tinydb_base.getSet import GetSet
from .commons import mkHex

class Tokens(GetSet):

    def __init__(self, file: str = 'ds.json', table: str = 'tokens'):
        super().__init__(file=file, table=table)

    def addKey(self, uname:str):
        key = mkHex(128)
        self.set(uname, 128)
        return key