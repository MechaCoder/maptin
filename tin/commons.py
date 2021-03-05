from datetime import datetime
from os import system
import sys
import unittest

from .data.commons import Credentials

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

    fileObj = open('debug.txt', 'a+')
    fileObj.write( f'{ datetime.now() } | {msg} \n' ) 
    fileObj.close()

    return True

def runUnittest():
    system('python test.py')
    return True