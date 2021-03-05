#!/usr/bin/python3

from tin.commons import Credentials
from tin.data.settings import Settings
from tin.http.trove import trove
from tin.data.sql import Builder
import sys

if __name__ == '__main__':

    

    Credentials().write() #will wirte standeard creds

    if input('do want to build a mysql database? (y)') == 'y':
        Builder().main()
    Settings() #will write the ds
    if input('do want to download assets? (y)') == 'y':
        trove() # will down load all maps