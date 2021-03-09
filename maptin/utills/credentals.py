from os.path import join, realpath, isfile
from json import dumps, loads

class Credentials:
    
    def __init__(self):
        dirPath = realpath(__file__)
        fname = 'credentials.json'

        a = dirPath.split('/')[:-3]

        self.fPath = join('/'.join(a), fname)
        self.directory = '/'.join(a)

        if isfile(self.fPath) is False:
            self.write()

    def read(self):
        fileObj = open(self.fPath, 'r')
        contentString = fileObj.read()
        json = loads(contentString)
        fileObj.close()
        return json

    def write(self):
        
        if isfile(self.fPath):
            return False

        d = {
            'ds': join(self.directory, 'ds.json'),
            'log': join(self.directory, 'log.log'),
            'root': join(self.directory)
        }
        fileObj = open(self.fPath, 'w')
        fileObj.write(
            dumps(d, indent=4, sort_keys=True)
        )
        fileObj.close()
        return True

    def getKey(self, key:str):

        obj = self.read()
        return obj[key]
