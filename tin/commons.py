from datetime import datetime

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

def debug_file(msg:str):

    print(msg)
    fileObj = open('debug.txt', 'a+')
    fileObj.write( f'{ datetime.now() } | {msg} \n' ) 
    fileObj.close()

    return True
