#!/usr/bin/python3

from tin.commons import Credentials
from tin.data.settings import Settings
from tin.http.trove import trove
import sys

if __name__ == '__main__':
    Credentials().write() #will wirte standeard creds
    Settings() #will write the ds
    trove() # will down load all maps