
def success(_data:dict = {}):
    return {
        'succ': True,
        'data': _data 
    }

def fail(_errMsg:str = 'there has been an error'):
    return {
        'succ': False,
        'err': _errMsg 
    }
