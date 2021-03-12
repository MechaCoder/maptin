
def success(_data:dict = {}):
    return {
        'succ': True,
        'data': _data 
    }

def fail(_errMsg:str = 'there has been an error'):
    if isinstance(_errMsg, str) is False:
        _errMsg = str(_errMsg)

    return {
        'succ': False,
        'err': _errMsg 
    }
