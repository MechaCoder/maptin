from .data.tokens import Tokens

def keyExists(self, key:str):
    if Tokens().keyExsists(key=key) == False:
        return {
            'succs': False,
            'error': 'invalid key',
        }