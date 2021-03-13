from os.path import join
from os import listdir
from .credentals import Credentials
from maptin.data.maps import Map
from maptin.utills.http import success, fail

class Assets:

    def tokens(self):

        creds = Credentials().read()

        localPath = 'static/a/tokens/'
        imgs = []
        path = join(creds['root'], localPath)
        for img in listdir(path):
            thing = join(localPath, img)
            imgs.append(thing)

        return imgs

    def maps(self):
        creds = Credentials().read()

        localPath = 'static/a/maps/'
        imgs = []
        path = join(creds['root'], localPath)
        for img in listdir(path):
            thing = join(localPath, img)
            thing = '/' + thing
            imgs.append(thing)

        return imgs

def getMapAssets():
    d = {}
    for map in Map().readAll():
        if map['map_background'] not in d.keys():
            d[map['map_background']] = 1
            continue
        d[map['map_background']] = map['map_background'] + 1

    d = {d: v for d, v in sorted(d.items(), key=lambda item: item[1])}
    e = []
    for each in list(d.keys()):
        e.append( '/' + each )

    obj = {
        'all': Assets().maps(),
        'popular': e
    }

    return success(obj)
