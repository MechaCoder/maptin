from unittest import main, TextTestRunner
import logging
from datetime import datetime

# from test.map import TestMap
from test.mapsTest import TestMap

TestGlobal = False

logging.basicConfig(
    filename='log.log',
    level=logging.NOTSET,
    format="%(asctime)s ::: %(levelname)s:%(name)s:%(message)s")

if __name__ == '__main__':

    # logging.info(msg='Unit tests run')
    main()

    # with open('unittest.results.text', 'w') as f:
    #     ts = "\n \n timestamp: " + str(datetime.now()) + "\n"
    #     f.write(ts)
    #     outputString = TextTestRunner(f)
    #     main(testRunner=outputString)
