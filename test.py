from unittest import main, TextTestRunner
import logging
from datetime import datetime

from tin.tests__init__ import TestCommons
from tin.data.tests_maps import TestMaps
from tin.data.tests_settings import TestSettings
from tin.data.tests_tokens import testTokens
from tin.data.tests_users import testDataUser
from tin.data.tests_vtokens import testvTokenData

logging.basicConfig(filename='log.log', level=logging.NOTSET, format="%(asctime)s ::: %(levelname)s:%(name)s:%(message)s")

if __name__ == '__main__':

    logging.info(msg='Unit tests run')

    with open('unittest.results.text', 'a') as f:
        ts = "\n \n timestamp: " + str(datetime.now()) + "\n"
        f.write(ts)
        outputString = TextTestRunner(f)
        main(testRunner=outputString)
