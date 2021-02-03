from tinydb_base import DatabaseBase,
from .commons import mkHex, DataCommons

class vTokenData(DataCommons):

    def __init__(self, file: str = 'ds.vToken.json', table: str = 'tokens', requiredKeys = 'hex,mapHex,source,type,x,y,ts'):
        super().__init__(file=file, table=table, requiredKeys=requiredKeys)

    def create(self, mapHex, source, tokenType, x, y) -> int:

        hex = ''
        while True:
            hex = mkHex()
            if self.exists('hex', hex) == False:
                break

        if tokenType not in ['token', 'map']:
            raise Exception('invalid token type')

        row = {
            'hex': hex,
            'mapHex': mapHex,
            'source': source,
            'type': tokenType,
            'x': x,
            'y': y,
            'ts': self.now_ts()

        }
        return super().create(row)

    