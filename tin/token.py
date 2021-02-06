from .data.tokens import Tokens

def keyExists(key:str):
    if Tokens().keyExsists(key=key) == False:
        return {
            'succs': False,
            'error': 'invalid key',
        }
    return {
        'succs': True
    }
