#!/usr/bin/python3

from sys import version_info
import sys
# from maptin.utills.credentals import Credentials
from maptin.http.trove import trove


if __name__ == '__main__':
    
    if version_info.major != 3 or version_info.minor != 8:
        print('python 3.8 is required.')
        exit()
    
    if input('download assets') == 'y':
        trove()
        # Credentials().write() # will wirte standeard creds
        pass
    pass
    