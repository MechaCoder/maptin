#!/usr/bin/python3

from tin.commons import Credentials
from tin.data.settings import Settings

if __name__ == '__main__':
    Credentials().write()
    Settings()