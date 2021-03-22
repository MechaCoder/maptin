#!/usr/bin/python3

from sys import version_info
import sys
# from maptin.utills.credentals import Credentials
from maptin.http.trove import trove
from maptin.utills.credentals import Credentials
from maptin.data.models import databaseUpdateTables


if __name__ == '__main__':
    
    if version_info.major != 3 or version_info.minor != 8:
        print('python 3.8 is required.')
        exit()

    Credentials().write() # will wirte standeard creds

    if input('atempt db upgrade? ') == 'y':
        databaseUpdateTables()

    
    if input('download assets? ') == 'y':
        trove()
        pass
    pass
    